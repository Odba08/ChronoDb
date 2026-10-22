from typing import List, Optional
from pydantic import BaseModel, Field

class StoryAct(BaseModel):
    act_number: int
    act_title: str = Field(description="Título evocador del acto")
    start_chapter: int
    end_chapter: int
    core_theme: str = Field(description="Atmósfera y temática central del acto")
    primary_conflict: str = Field(description="El conflicto principal o amenaza en la Academia")
    mandatory_pacing: str = Field(description="Regla de ritmo orientativo")

class BookOutline(BaseModel):
    book_title: str = Field(default="Arquímedes", description="Título de trabajo")
    acts: List[StoryAct] = Field(min_length=4, max_length=4)

def get_canonical_outline() -> BookOutline:
    """
    Devuelve la estructura pública de actos de Arquímedes.
    No contiene conspiraciones fijas ni agendas predeterminadas para no sesgar
    ni spoilear al modelo durante la narración de cada escena.
    """
    return BookOutline(
        book_title="Arquímedes",
        acts=[
            StoryAct(
                act_number=1,
                act_title="La Puerta de Hierro y Ceniza",
                start_chapter=1,
                end_chapter=10,
                core_theme="El ingreso a la Academia Militar, pruebas de selección física y neurológica con reliquias antiguas, jerarquías de cadetes y primer encuentro con Virginia.",
                primary_conflict="Sobrevivir a la hostilidad de la institución y a la presión de los instructores sin ser descartado.",
                mandatory_pacing="desarrollo_academico"
            ),
            StoryAct(
                act_number=2,
                act_title="El Velo de la Historia Oficial",
                start_chapter=11,
                end_chapter=25,
                core_theme="Contradicciones en la historia oficial de la guerra contra Ares, exploración de las ruinas ciclópeas bajo la academia, rivalidades y alianzas entre cadetes.",
                primary_conflict="Aparición de anomalías históricas y tecnologías prohibidas que cuestionan la verdad oficial.",
                mandatory_pacing="intriga_y_ruinas"
            ),
            StoryAct(
                act_number=3,
                act_title="La Encrucijada de la Causalidad",
                start_chapter=26,
                end_chapter=40,
                core_theme="Ecos temporales más intensos y puntos de bifurcación crítica donde las decisiones de Oscar ramifican la historia.",
                primary_conflict="Dilemas morales y estratégicos que separan a los cadetes y alteran el rumbo del conflicto.",
                mandatory_pacing="divergencia_critica"
            ),
            StoryAct(
                act_number=4,
                act_title="La Convergencia de los Ecos",
                start_chapter=41,
                end_chapter=50,
                core_theme="Clímax de la trayectoria forjada por Oscar y Virginia, resolución de las ramificaciones y preparación para el Libro 2.",
                primary_conflict="Enfrentamiento directo con las consecuencias acumuladas de las elecciones del lector.",
                mandatory_pacing="climax_causal"
            )
        ]
    )

def generate_book_outline(client=None, model: str = "") -> BookOutline:
    """Devuelve la escaleta canónica pública de Arquímedes sin spoilers."""
    return get_canonical_outline()
