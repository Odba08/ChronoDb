from models import GameState, TurnoIAResponse, TurnoClienteResponse, RecentTurn, ActionOption

def clamp(value: int, min_val: int, max_val: int) -> int:
    """Asegura que un número no se pase de sus límites."""
    return max(min_val, min(value, max_val))

# ESTRUCTURA MAESTRA DE LOS 3 ACTOS DE LA NOVELA (ARQUÍMEDES // LIBRO I)
ACTS_DATA = {
    1: {
        "act_number": 1,
        "title": "Acto I: La Academia",
        "theme": "La Academia Militar (Tono: The Will of the Many, Classroom of the Elite, Red Rising). Jerarquías feroces, competición táctica y psicológica entre cadetes. Oscar mantiene perfil bajo analizando fríamente el entorno. Sufre flashbacks involuntarios de las líneas temporales de Ares y despierta un poder latente no comprendido relacionado con el tiempo.",
        "climax_threshold": 18,
    },
    2: {
        "act_number": 2,
        "title": "Acto II: La Investigación y los Laberintos",
        "theme": "Investigación clandestina en los laberintos ocultos bajo la academia (muy a lo The Will of the Many). Alianzas y rivalidades forjadas en el Acto I (dentro o fuera de la academia). Entrada paulatina en los secretos prohibidos.",
        "climax_threshold": 20,
    },
    3: {
        "act_number": 3,
        "title": "Acto III: El Clímax Causal",
        "theme": "Clímax final en todo lo alto. Secretos revelados de la civilización perdida y los viajes en el tiempo. Ares consigue capturar a Virginia y Oscar se encuentra cara a cara consigo mismo.",
        "climax_threshold": 22,
    }
}

def get_climax_phase(turns_in_act: int, climax_threshold: int) -> tuple[str, str]:
    """
    Calcula la fase dramática y la cercanía al clímax dentro del Acto:
    - Inmersión Analítica: Prosa extensa, atmósfera, psicología de Oscar y Virginia.
    - Tensión Creciente: Anomalías, sospechas, dilemas crecientes.
    - Clímax del Acto: Máxima intensidad dramática y gran encrucijada.
    """
    if turns_in_act < int(climax_threshold * 0.45):
        return ("inmersion_analitica", "Inmersión Analítica")
    elif turns_in_act < int(climax_threshold * 0.85):
        return ("tension_creciente", "Tensión Creciente")
    else:
        return ("climax_inminente", "Clímax del Acto")

class GameEngine:
    
    @staticmethod
    def process_turn(state: GameState, ai_response: TurnoIAResponse, player_choice: str) -> TurnoClienteResponse:
        """
        El Árbitro: Toma el estado actual, aplica el delta de la IA y devuelve la pantalla del iPad.
        """
        
        # 1. APLICAR MATEMÁTICAS (Topes estrictos)
        state.health = clamp(state.health + ai_response.state_delta.health_delta, 0, 100)
        state.entropy = clamp(state.entropy + ai_response.state_delta.entropy_delta, 0, 100)
        
        # Actualizar Virginia
        state.virginia.intensity = clamp(
            state.virginia.intensity + ai_response.state_delta.virginia_relationship_delta, 1, 10
        )
        if getattr(ai_response.state_delta, "virginia_notes_update", None):
            state.virginia.notes = ai_response.state_delta.virginia_notes_update.strip()
        
        # Actualizar Inventario
        for item in ai_response.state_delta.acquired_items:
            if item not in state.inventory:
                state.inventory.append(item)
                
        for item in ai_response.state_delta.lost_items:
            if item in state.inventory:
                state.inventory.remove(item)

        # Actualizar Sistema de Continuidad (Arquímedes)
        delta = ai_response.state_delta

        # new_lore: hechos nuevos confirmados por la escena
        for hecho in getattr(ai_response, "new_lore", []):
            h = hecho.strip()
            if h and h not in state.confirmed_facts:
                state.confirmed_facts.append(h)
                if len(state.confirmed_facts) > 15:
                    state.confirmed_facts.pop(0)
            if h and h not in state.lore_ledger:
                state.lore_ledger.append(h)
                if len(state.lore_ledger) > 10:
                    state.lore_ledger.pop(0)

        if getattr(delta, "new_open_thread", None):
            thread = delta.new_open_thread.strip()
            if thread and thread not in state.open_threads:
                state.open_threads.append(thread)
                if len(state.open_threads) > 10:
                    state.open_threads.pop(0)

        if getattr(delta, "resolved_thread", None):
            resolved = delta.resolved_thread.strip().lower()
            state.open_threads = [t for t in state.open_threads if resolved not in t.lower()]

        if getattr(delta, "branch_influence", None):
            state.active_branch = delta.branch_influence.strip()

        # Factor Secreto: Registro de Claves Cósmicas / Universales
        if getattr(delta, "secret_key_trigger", None):
            trigger = delta.secret_key_trigger.strip().lower()
            if trigger and trigger not in state.secret_keys:
                state.secret_keys.append(trigger)
                # Si se han acumulado al menos 3 claves sutiles de la combinación secreta, se desbloquea la ruta
                if len(state.secret_keys) >= 3:
                    state.secret_route_unlocked = True

        # 2. ACTUALIZAR MEMORIA A CORTO PLAZO (El contexto para el siguiente turno)
        resumen_turno = ai_response.summary.strip() if getattr(ai_response, "summary", "").strip() else (
            ai_response.narrative[:160] + "..." if len(ai_response.narrative) > 160 else ai_response.narrative
        )
        nuevo_turno = RecentTurn(
            turn_number=state.turn_number,
            player_choice=player_choice,
            summary=resumen_turno
        )
        state.recent_turns.append(nuevo_turno)
        
        # Regla FIFO: Si hay más de 3 turnos recordados, olvidamos el más viejo
        if len(state.recent_turns) > 3:
            state.recent_turns.pop(0)

        # 3. EVALUAR SUPERVIVENCIA (El código decide la muerte, no Gemini)
        is_game_over = False
        game_over_reason = None

        if state.health <= 0:
            is_game_over = True
            game_over_reason = "Tus heridas son fatales. El ciclo se ha cerrado sobre ti..."
        elif state.entropy >= 100:
            is_game_over = True
            game_over_reason = "Tu mente se fractura bajo la sobrecarga de la entropía causal. El flujo temporal colapsa sobre tu percepción y tus constantes vitales se desvanecen en un eco de realidades incompatibles."

        # 4. GOBERNADOR DRAMÁTICO POR ACTOS (Acto 1, Acto 2, Acto 3)
        turno_actual = state.turn_number
        state.turn_number += 1
        
        act_num = getattr(state, "act_number", 1)
        turns_in_act = getattr(state, "turns_in_act", 1)
        act_info = ACTS_DATA.get(act_num, ACTS_DATA[1])
        climax_threshold = act_info.get("climax_threshold", 16)
        
        # ¿El jugador acaba de tomar una decisión en la encrucijada del clímax?
        prev_was_crossroad = getattr(state, "last_is_crossroad", False)
        chose_real_option = player_choice.strip().lower() not in (
            "continuar leyendo...", "continuar", "avanzar página narrativa", "continuar leyendo"
        )

        # Si el jugador resolvió una encrucijada y ya estábamos en la fase de clímax del acto:
        if (prev_was_crossroad and chose_real_option) and turns_in_act >= int(climax_threshold * 0.85):
            # ¡Se consumó la encrucijada del clímax! Avanzamos al siguiente Acto de la historia
            if act_num < 3:
                state.act_number = act_num + 1
            state.turns_in_act = 1
            act_num = state.act_number
            act_info = ACTS_DATA.get(act_num, ACTS_DATA[3])
        else:
            state.turns_in_act = turns_in_act + 1

        state.act_title = act_info["title"]
        phase_key, phase_label = get_climax_phase(state.turns_in_act, act_info["climax_threshold"])
        state.climax_phase = phase_label

        # Título de escena / capítulo: se mantiene orgánico sin forzar números arbitrarios
        if hasattr(ai_response, "chapter_title") and ai_response.chapter_title and len(ai_response.chapter_title.strip()) > 3:
            state.chapter_title = ai_response.chapter_title.strip()
        elif not getattr(state, "chapter_title", None):
            state.chapter_title = f"{state.act_title} • Crónica {state.turns_in_act}"

        # 5. DECISIÓN DE ENCRUCIJADA:
        # A. Si la IA propuso orgánicamente una encrucijada legítima con opciones divergentes, la respetamos.
        # B. Si hemos alcanzado el umbral de clímax del acto (turns_in_act >= climax_threshold):
        #    Se activa la gran encrucijada del Acto.
        # C. En cualquier otro caso: Lectura inmersiva fluida con "Continuar leyendo...".
        raw_crossroad = getattr(ai_response, "is_crossroad", False)
        valid_ai_options = [
            opt for opt in getattr(ai_response, "options", []) 
            if opt.label.strip().lower() not in ("continuar leyendo...", "continuar", "avanzar página narrativa")
        ]

        if (raw_crossroad and len(valid_ai_options) >= 2) or state.turns_in_act >= climax_threshold:
            is_crossroad = True
            if len(valid_ai_options) >= 2:
                final_options = valid_ai_options
            else:
                final_options = [
                    ActionOption(
                        label="Actuar con determinación táctica y confrontar el clímax",
                        approach="agresivo",
                        risk_level="critico"
                    ),
                    ActionOption(
                        label="Coordinar una maniobra encubierta con Virginia y evaluar la anomalía",
                        approach="sigilo",
                        risk_level="medio"
                    ),
                    ActionOption(
                        label="Analizar los registros del reactor y descifrar la verdad ontológica",
                        approach="analitico",
                        risk_level="bajo"
                    )
                ]
        else:
            is_crossroad = False
            final_options = [
                ActionOption(
                    label="Continuar leyendo...",
                    approach="analitico",
                    risk_level="bajo"
                )
            ]

        # 6. PERSISTIR ÚLTIMA PANTALLA EN EL ESTADO
        state.last_narrative = ai_response.narrative
        state.last_options = final_options
        state.last_is_crossroad = is_crossroad
        state.last_scene_tempo = getattr(ai_response, "scene_tempo", "tension_latente")
        state.last_art_prompt = ai_response.art_prompt
        state.is_game_over = is_game_over
        state.game_over_reason = game_over_reason

        # 7. EMPAQUETAR PARA LA PANTALLA (DTO de salida)
        return TurnoClienteResponse(
            session_id=state.session_id,
            turn_number=turno_actual,
            chapter_number=getattr(state, "chapter_number", 1),
            chapter_title=getattr(state, "chapter_title", f"{state.act_title} • Crónica {state.turns_in_act}"),
            act_number=state.act_number,
            act_title=state.act_title,
            turns_in_act=state.turns_in_act,
            climax_phase=state.climax_phase,
            narrative=ai_response.narrative,
            health=state.health,
            entropy=state.entropy,
            virginia=state.virginia,
            inventory=state.inventory,
            lore_ledger=getattr(state, "lore_ledger", []),
            confirmed_facts=state.confirmed_facts,
            open_threads=state.open_threads,
            active_branch=state.active_branch,
            secret_route_unlocked=state.secret_route_unlocked,
            is_crossroad=is_crossroad,
            options=final_options,
            is_game_over=is_game_over,
            game_over_reason=game_over_reason,
            scene_tempo=getattr(ai_response, "scene_tempo", "tension_latente"),
            art_prompt=ai_response.art_prompt
        )
