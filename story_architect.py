from typing import List, Optional
from pydantic import BaseModel, Field

class StoryAct(BaseModel):
    act_number: int
    act_title: str = Field(description="Título del acto")
    core_theme: str = Field(description="Atmósfera, tono e influencias centrales")
    narrative_focus: str = Field(description="Foco dramático y arco de evolución")

class BookOutline(BaseModel):
    book_title: str = Field(default="Arquímedes // Libro I: La Voluntad de las Cenizas", description="Título de la obra")
    acts: List[StoryAct] = Field(min_length=3, max_length=3)

def get_canonical_outline() -> BookOutline:
    """
    Estructura canónica de los 3 Grandes Actos de Arquímedes.
    Inspiraciones: The Will of the Many, Red Rising, Classroom of the Elite.
    Otorga total libertad creativa a la IA para dramatizar escenas y personajes orgánicamente.
    """
    return BookOutline(
        book_title="Arquímedes // Libro I: La Voluntad de las Cenizas",
        acts=[
            StoryAct(
                act_number=1,
                act_title="Acto I: La Academia",
                core_theme="La Academia Militar (Tono: The Will of the Many, Classroom of the Elite, Red Rising). Jerarquías implacables, pruebas de supervivencia y competición feroz entre cadetes. Oscar mantiene un perfil bajo analizando fríamente a compañeros e instructores. Sufre flashbacks involuntarios de las líneas temporales que Ares ha vivido y despierta un poder latente que aún no comprende relacionado con la percepción del tiempo.",
                narrative_focus="Supervivencia en el escalafón, cálculo psicológico, dinámicas con Virginia y cadetes rivales, y primeros destellos de su poder temporal."
            ),
            StoryAct(
                act_number=2,
                act_title="Acto II: La Investigación y los Laberintos",
                core_theme="Investigación y misterio progresivo (muy a lo The Will of the Many cuando descubren los laberintos ocultos). Infiltración paulatina en los secretos prohibidos bajo la academia. Conexión y alianzas con amigos y rivales forjados en el Acto I (dentro o fuera de la academia).",
                narrative_focus="Exploración clandestina de pasadizos y laberintos, tecnología prohibida, revelación de contradicciones históricas y consolidación del vínculo con Virginia."
            ),
            StoryAct(
                act_number=3,
                act_title="Acto III: El Clímax Causal",
                core_theme="Clímax final en todo lo alto. Revelación de la civilización perdida y los viajes en el tiempo. Ares consigue capturar a Virginia. Oscar se encuentra cara a cara frente a sí mismo. Desenlace épico y trascendental.",
                narrative_focus="Punto de convergencia ontológica, enfrentamiento directo con las consecuencias del tiempo y resolución de la trayectoria del Libro I."
            )
        ]
    )

def generate_book_outline(client=None, model: str = "") -> BookOutline:
    """Devuelve la escaleta de 3 Actos para orientar la narrativa de la IA."""
    return get_canonical_outline()
