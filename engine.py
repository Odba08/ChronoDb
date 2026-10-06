from models import GameState, TurnoIAResponse, TurnoClienteResponse, RecentTurn

def clamp(value: int, min_val: int, max_val: int) -> int:
    """Asegura que un número no se pase de sus límites."""
    return max(min_val, min(value, max_val))

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
        
        # Actualizar Inventario
        for item in ai_response.state_delta.acquired_items:
            if item not in state.inventory:
                state.inventory.append(item)
                
        for item in ai_response.state_delta.lost_items:
            if item in state.inventory:
                state.inventory.remove(item)

        # Actualizar Lore Ledger (Memoria a largo plazo)
        if ai_response.state_delta.new_milestone:
            milestone = ai_response.state_delta.new_milestone.strip()
            if milestone and milestone not in state.lore_ledger:
                state.lore_ledger.append(milestone)
                if len(state.lore_ledger) > 10:
                    state.lore_ledger.pop(0)

        # 2. ACTUALIZAR MEMORIA A CORTO PLAZO (El contexto para el siguiente turno)
        nuevo_turno = RecentTurn(
            turn_number=state.turn_number,
            player_choice=player_choice,
            # Guardamos solo un fragmento de la narrativa para no quemar tokens de memoria
            summary=ai_response.narrative[:150] + "..." if len(ai_response.narrative) > 150 else ai_response.narrative
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
            game_over_reason = "Tus heridas son fatales. El bucle se ha cerrado sobre ti..."
        elif state.entropy >= 100:
            is_game_over = True
            game_over_reason = "Tu mente se fractura. Un destello final te ciega: te ves a ti mismo con una armadura negra, pisando el cadáver de Virginia frente a un portal en ruinas. No entiendes nada, pero el dolor te apaga. El bucle colapsa (Sobrecarga temporal)."

        # 4. AVANZAR EL TIEMPO
        turno_actual = state.turn_number
        state.turn_number += 1

        # 5. EMPAQUETAR PARA LA PANTALLA (DTO de salida)
        return TurnoClienteResponse(
            turn_number=turno_actual,
            narrative=ai_response.narrative,
            health=state.health,
            entropy=state.entropy,
            options=ai_response.options,
            is_game_over=is_game_over,
            game_over_reason=game_over_reason,
            scene_tempo=getattr(ai_response, "scene_tempo", "tension_latente"),
            art_prompt=ai_response.art_prompt
        )