from typing import List, Literal, Optional
from pydantic import BaseModel, Field, model_validator

# ---------------------------------------------------------
# 1. LO QUE LA IA NOS DEVUELVE (EL BARDO)
# ---------------------------------------------------------

class ActionOption(BaseModel):
    label: str = Field(description="El texto que aparecerá en el botón del iPad")
    approach: Literal["agresivo", "sigilo", "analitico", "desesperado"]
    risk_level: Literal["bajo", "medio", "critico"]

class StateDelta(BaseModel):
    health_delta: int = Field(default=0, ge=-50, le=50, description="Cambio de salud propuesto")
    entropy_delta: int = Field(default=0, ge=-50, le=50, description="Cambio de entropía propuesto")
    virginia_relationship_delta: int = Field(default=0, ge=-2, le=2, description="Impacto en la confianza de Virginia")
    acquired_items: List[str] = Field(default_factory=list)
    lost_items: List[str] = Field(default_factory=list)
    virginia_notes_update: Optional[str] = Field(default=None, max_length=200, description="Actualización sobre la actitud, sospechas o convicciones de Virginia")
    new_open_thread: Optional[str] = Field(default=None, max_length=200, description="Nueva hipótesis o posibilidad abierta")
    resolved_thread: Optional[str] = Field(default=None, max_length=200, description="Hilo o sospecha que quedó confirmada o descartada")
    branch_influence: Optional[str] = Field(default=None, max_length=100, description="Inclinación de la trayectoria de Oscar")
    secret_key_trigger: Optional[str] = Field(default=None, max_length=100, description="Si la decisión activa sutilmente una de las claves de la Ruta Secreta Universal")

class TurnoIAResponse(BaseModel):
    chapter_title: Optional[str] = Field(default=None, description="Título literario de la escena o capítulo si cambia")
    narrative: str = Field(description="La escena completa en primera persona desde Oscar")
    is_crossroad: bool = Field(default=False, description="True si este momento es una encrucijada moral/táctica mayor. False si la historia debe continuar fluyendo naturalmente.")
    options: List[ActionOption] = Field(min_length=1, max_length=4, description="1 opción si es lectura fluida; 3 o 4 opciones únicas si es una encrucijada")
    state_delta: StateDelta = Field(default_factory=StateDelta, description="Cambios justificables en el estado")
    summary: str = Field(default="", description="Resumen breve y factual de lo sucedido")
    new_lore: List[str] = Field(default_factory=list, description="Hechos nuevos confirmados por la escena")
    art_prompt: Optional[str] = Field(None, description="Prompt visual en inglés para FLUX, solo si cambia la escena drásticamente")
    scene_tempo: Optional[Literal["frenetico", "tension_latente", "calma_narrativa"]] = "tension_latente"

    @model_validator(mode='after')
    def check_unique_approaches(self) -> 'TurnoIAResponse':
        if len(self.options) > 1:
            approaches = [opt.approach for opt in self.options]
            if len(set(approaches)) != len(approaches):
                raise ValueError("Las opciones tácticas deben tener enfoques (approaches) estrictamente únicos.")
        return self

# ---------------------------------------------------------
# 2. EL ESTADO INTERNO DEL JUEGO (EL ÁRBITRO)
# ---------------------------------------------------------

class VirginiaState(BaseModel):
    status: Literal["hostil", "tensa", "neutral", "leal"] = "neutral"
    intensity: int = Field(ge=1, le=10, default=5)
    notes: str = Field(default="Compañera de ingreso a la Academia", description="Justificación breve de su postura")
    current_agenda: str = Field(default="Sobrevivir a la prueba de admisión de la Academia", description="Iniciativa y objetivo propio de Virginia")

class RecentTurn(BaseModel):
    turn_number: int
    player_choice: str
    summary: str

class GameState(BaseModel):
    session_id: str
    turn_number: int = 1
    chapter_number: int = 1
    chapter_title: str = "Capítulo 1: El Umbral de la Academia"
    act_number: int = 1
    act_title: str = "Acto I: La Puerta de Hierro y Ceniza"
    turns_in_chapter: int = 1
    turns_in_act: int = 1  # Páginas/turnos desarrollados en el acto actual
    climax_phase: str = "Inmersión Analítica"  # "Inmersión Analítica" | "Tensión Creciente" | "Clímax del Acto"
    
    # Límites absolutos de supervivencia
    health: int = Field(ge=0, le=100, default=100)
    entropy: int = Field(ge=0, le=100, default=0)
    
    virginia: VirginiaState = Field(default_factory=VirginiaState)
    inventory: List[str] = Field(default_factory=list)
    flags: dict[str, bool] = Field(default_factory=dict)
    
    # Sistema de Continuidad (Documento Maestro Arquímedes)
    confirmed_facts: List[str] = Field(default_factory=list, description="Hechos inmutables ya establecidos en la historia")
    open_threads: List[str] = Field(default_factory=list, description="Posibilidades e hipótesis abiertas actualmente")
    active_branch: str = Field(default="Cadete de la Academia", description="Vector de trayectoria actual de Oscar")
    
    # Factor Secreto: Ruta Cósmica / Universal
    secret_keys: List[str] = Field(default_factory=list, description="Fragmentos de la clave secreta acumulados")
    secret_route_unlocked: bool = Field(default=False, description="True si se completó la combinación exacta de las 4 capas")

    # Memoria en 2 capas
    lore_ledger: List[str] = Field(default_factory=list, max_length=10)
    recent_turns: List[RecentTurn] = Field(default_factory=list, max_length=3)

    # Cache de la última pantalla para reanudación instantánea
    last_narrative: Optional[str] = None
    last_options: List[ActionOption] = Field(default_factory=list)
    last_is_crossroad: bool = False
    last_scene_tempo: Literal["frenetico", "tension_latente", "calma_narrativa"] = "tension_latente"
    last_art_prompt: Optional[str] = None
    is_game_over: bool = False
    game_over_reason: Optional[str] = None

# ---------------------------------------------------------
# 3. LO QUE LE MANDAMOS AL IPAD (LA PANTALLA)
# ---------------------------------------------------------

class TurnoClienteResponse(BaseModel):
    session_id: Optional[str] = None
    turn_number: int
    chapter_number: int = 1
    chapter_title: str = "Capítulo 1: El Umbral de la Academia"
    act_number: int = 1
    act_title: str = "Acto I: La Puerta de Hierro y Ceniza"
    turns_in_act: int = 1
    climax_phase: str = "Inmersión Analítica"
    narrative: str
    health: int
    entropy: int
    virginia: VirginiaState
    inventory: List[str]
    lore_ledger: List[str] = Field(default_factory=list)
    confirmed_facts: List[str] = Field(default_factory=list)
    open_threads: List[str] = Field(default_factory=list)
    active_branch: str = "Cadete de la Academia"
    secret_route_unlocked: bool = False
    is_crossroad: bool = False
    options: List[ActionOption]
    is_game_over: bool = False
    game_over_reason: Optional[str] = None
    scene_tempo: Optional[Literal["frenetico", "tension_latente", "calma_narrativa"]] = "tension_latente"
    art_prompt: Optional[str] = None
