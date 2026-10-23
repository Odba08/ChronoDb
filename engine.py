from models import GameState, TurnoIAResponse, TurnoClienteResponse, RecentTurn, ActionOption

def clamp(value: int, min_val: int, max_val: int) -> int:
    """Asegura que un número no se pase de sus límites."""
    return max(min_val, min(value, max_val))

CHAPTER_TITLES = {
    1: "Capítulo 1: El Umbral de la Academia",
    2: "Capítulo 2: Los Simuladores de Vacío",
    3: "Capítulo 3: La Jerarquía de las Sombras",
    4: "Capítulo 4: Las Ruinas Ciclópeas Subterráneas",
    5: "Capítulo 5: El Secreto del Reactor Geller",
    6: "Capítulo 6: La Fuga de los Ecos",
    7: "Capítulo 7: La Alianza de las Cenizas",
    8: "Capítulo 8: La Fractura Ontológica",
    9: "Capítulo 9: El Retorno al Umbral (El Despertar Consciente)",
    10: "Capítulo 10: La Voluntad de las Cenizas",
    11: "Capítulo 11: Las Profundidades del Abismo",
    12: "Capítulo 12: El Archivo Olvidado de Ares",
    13: "Capítulo 13: El Susurro de los Ancestros",
    14: "Capítulo 14: La Señal de la Flota Fantasma",
    15: "Capítulo 15: La Puerta de los Ecos"
}

def get_chapter_title(chapter_num: int, ai_title: str = None) -> str:
    if ai_title and len(ai_title.strip()) > 3 and "Capítulo" in ai_title:
        return ai_title.strip()
    return CHAPTER_TITLES.get(chapter_num, f"Capítulo {chapter_num}: La Convergencia de los Ecos")

def get_act_title(chapter_num: int) -> str:
    if chapter_num <= 10:
        return "Acto I: La Puerta de Hierro y Ceniza"
    elif chapter_num <= 25:
        return "Acto II: El Velo de la Historia Oficial"
    elif chapter_num <= 40:
        return "Acto III: La Encrucijada de la Causalidad"
    else:
        return "Acto IV: La Convergencia de los Ecos"

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

        # 4. GOBERNADOR DE RITMO Y PROGRESIÓN DE CAPÍTULOS
        turno_actual = state.turn_number
        state.turn_number += 1
        
        # Detectar si el jugador acaba de responder a una encrucijada
        # (Es decir, su elección NO fue la simple continuación de lectura y el turno anterior fue encrucijada)
        prev_was_crossroad = getattr(state, "last_is_crossroad", False)
        chose_real_option = player_choice.strip().lower() not in ("continuar leyendo...", "continuar", "avanzar página narrativa")
        turns_in_cap = getattr(state, "turns_in_chapter", 1)

        if (prev_was_crossroad or chose_real_option) and turns_in_cap >= 3:
            # ¡El clímax del capítulo anterior fue resuelto por el jugador!
            # Avanzamos al siguiente capítulo automáticamente
            state.chapter_number = getattr(state, "chapter_number", 1) + 1
            state.turns_in_chapter = 1  # Comienza el nuevo capítulo
        else:
            # Seguimos avanzando la narración dentro del capítulo actual
            state.turns_in_chapter = turns_in_cap + 1

        # Actualizar títulos de acto y capítulo
        state.act_title = get_act_title(state.chapter_number)
        state.chapter_title = get_chapter_title(state.chapter_number, getattr(ai_response, "chapter_title", None))

        # DECISIÓN DE ENCRUCIJADA:
        # Si llevamos 3 o más avances en el capítulo actual, ¡ES OBLIGATORIO DAR ELECCIONES AL LECTOR!
        current_turns_in_cap = state.turns_in_chapter
        raw_crossroad = getattr(ai_response, "is_crossroad", False)

        if current_turns_in_cap >= 3:
            # Clímax del capítulo: Ofrecer 3-4 opciones estratégicas reales
            is_crossroad = True
            
            # Filtrar si la IA devolvió opciones válidas que no sean "continuar leyendo"
            valid_ai_options = [
                opt for opt in getattr(ai_response, "options", []) 
                if opt.label.strip().lower() not in ("continuar leyendo...", "continuar")
            ]
            
            if len(valid_ai_options) >= 2:
                final_options = valid_ai_options
            else:
                # Opciones tácticas de contingencia perfectamente adaptadas al clímax
                final_options = [
                    ActionOption(
                        label="Actuar con determinación táctica y confrontar la situación",
                        approach="agresivo",
                        risk_level="medio"
                    ),
                    ActionOption(
                        label="Buscar una ruta alterna en sigilo y coordinar una maniobra con Virginia",
                        approach="sigilo",
                        risk_level="bajo"
                    ),
                    ActionOption(
                        label="Analizar los patrones del reactor y descifrar la anomalía temporal",
                        approach="analitico",
                        risk_level="medio"
                    )
                ]
        else:
            # Avance fluido de lectura: la prosa se desenvuelve sin interrupción
            is_crossroad = False
            final_options = [
                ActionOption(
                    label="Continuar leyendo...",
                    approach="analitico",
                    risk_level="bajo"
                )
            ]

        # 5. PERSISTIR ÚLTIMA PANTALLA EN EL ESTADO (Para reanudar al instante)
        state.last_narrative = ai_response.narrative
        state.last_options = final_options
        state.last_is_crossroad = is_crossroad
        state.last_scene_tempo = getattr(ai_response, "scene_tempo", "tension_latente")
        state.last_art_prompt = ai_response.art_prompt
        state.is_game_over = is_game_over
        state.game_over_reason = game_over_reason

        # 6. EMPAQUETAR PARA LA PANTALLA (DTO de salida)
        return TurnoClienteResponse(
            session_id=state.session_id,
            turn_number=turno_actual,
            chapter_number=getattr(state, "chapter_number", 1),
            chapter_title=getattr(state, "chapter_title", f"Capítulo {getattr(state, 'chapter_number', 1)}: El Umbral de la Academia"),
            act_title=getattr(state, "act_title", "Acto I: La Puerta de Hierro y Ceniza"),
            narrative=ai_response.narrative,
            health=state.health,
            entropy=state.entropy,
            virginia=state.virginia,
            inventory=state.inventory,
            lore_ledger=state.lore_ledger,
            confirmed_facts=getattr(state, "confirmed_facts", []),
            open_threads=getattr(state, "open_threads", []),
            active_branch=getattr(state, "active_branch", "Cadete de la Academia"),
            secret_route_unlocked=getattr(state, "secret_route_unlocked", False),
            is_crossroad=is_crossroad,
            options=final_options,
            is_game_over=is_game_over,
            game_over_reason=game_over_reason,
            scene_tempo=getattr(ai_response, "scene_tempo", "tension_latente"),
            art_prompt=ai_response.art_prompt
        )
