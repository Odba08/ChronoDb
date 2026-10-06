from typing import List, Literal, Optional
from pydantic import BaseModel, Field, model_validator

# ---------------------------------------------------------
# 1. LO QUE LA IA NOS DEVUELVE (EL BARDO)
# ---------------------------------------------------------

class ActionOption(BaseModel):
    label: str = Field(description="El texto corto que aparecerá en el botón del iPad")
    # Enmienda 7: Nombres limpios para los arquetipos
    approach: Literal["agresivo", "sigilo", "analitico", "desesperado"]
    risk_level: Literal["bajo", "medio", "critico"]

class StateDelta(BaseModel):
    # Enmienda 5: Límites de cordura para los deltas (la IA no puede curar/matar de golpe)
    health_delta: int = Field(ge=-50, le=50, description="Cambio de salud propuesto")
    entropy_delta: int = Field(ge=-50, le=50, description="Cambio de entropía propuesto")
    virginia_relationship_delta: int = Field(ge=-2, le=2, description="Impacto en la confianza de Virginia")
    acquired_items: List[str] = Field(default_factory=list)
    lost_items: List[str] = Field(default_factory=list)
    new_milestone: Optional[str] = Field(default=None, max_length=150, description="Hito inmutable si se descubrió una revelación clave")

class TurnoIAResponse(BaseModel):
    narrative: str = Field(description="La prosa visceral y táctica del turno")
    state_delta: StateDelta
    options: List[ActionOption] = Field(min_length=3, max_length=4)
    art_prompt: Optional[str] = Field(None, description="Prompt en inglés para FLUX, solo si cambia la escena drásticamente")
    scene_tempo: Literal["frenetico", "tension_latente", "calma_narrativa"]
    # Enmienda 1: El Validador Mágico que fuerza opciones diferentes
    @model_validator(mode='after')
    def check_unique_approaches(self) -> 'TurnoIAResponse':
        approaches = [opt.approach for opt in self.options]
        if len(set(approaches)) != len(approaches):
            raise ValueError("Las opciones tácticas deben tener enfoques (approaches) estrictamente únicos.")
        return self

# ---------------------------------------------------------
# 2. EL ESTADO INTERNO DEL JUEGO (EL ÁRBITRO)
# ---------------------------------------------------------

class VirginiaState(BaseModel):
    # Enmienda 4: Estado de Virginia controlado, no libre
    status: Literal["hostil", "tensa", "neutral", "leal"] = "neutral"
    intensity: int = Field(ge=1, le=10, default=5)
    notes: str = Field(default="", description="Justificación breve de por qué está así")

class RecentTurn(BaseModel):
    turn_number: int
    player_choice: str
    summary: str

class GameState(BaseModel):
    # Enmienda 6: Identificadores claros para logs
    session_id: str
    turn_number: int = 1
    
    # Límites absolutos de supervivencia
    health: int = Field(ge=0, le=100, default=100)
    entropy: int = Field(ge=0, le=100, default=0)
    
    virginia: VirginiaState = Field(default_factory=VirginiaState)
    inventory: List[str] = Field(default_factory=list)
    flags: dict[str, bool] = Field(default_factory=dict)
    
    # Enmienda 2 y 3: La Memoria
    lore_ledger: List[str] = Field(default_factory=list, max_length=10) # Memoria Larga
    recent_turns: List[RecentTurn] = Field(default_factory=list, max_length=3) # Memoria Corta

# ---------------------------------------------------------
# 3. LO QUE LE MANDAMOS AL IPAD (LA PANTALLA)
# ---------------------------------------------------------

class TurnoClienteResponse(BaseModel):
    turn_number: int
    narrative: str
    health: int
    entropy: int
    options: List[ActionOption]
    is_game_over: bool
    game_over_reason: Optional[str] = None
    scene_tempo: Optional[Literal["frenetico", "tension_latente", "calma_narrativa"]] = "tension_latente"
    art_prompt: Optional[str] = None