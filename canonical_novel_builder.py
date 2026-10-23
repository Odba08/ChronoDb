import os
import sys
from epub_builder import create_epub

def build_complete_canonical_novel():
    """
    Compila la edición de muestra canónica de Arquímedes // Libro I: La Voluntad de las Cenizas
    basada fielmente en la estructura de 3 Grandes Actos del autor:
    - Acto I: La Academia (The Will of the Many, Red Rising, Classroom of the Elite)
    - Acto II: La Investigación y los Laberintos
    - Acto III: El Clímax Causal
    """
    print("Iniciando compilación de la Obra: Arquímedes // Libro I: La Voluntad de las Cenizas...")
    
    passages = [
        {
            "chapter_number": 0,
            "chapter_title": "Prólogo: El Eco de la Ceniza",
            "act_title": "Acto I: La Academia",
            "narrative": """«Dame un punto de apoyo y moveré el mundo».

La frase de Arquímedes no era una metáfora para los eruditos de la vieja era; era una ecuación de palanca sobre la propia causalidad.

El aire de la meseta bajaba denso, cargado de partículas de ceniza que se adherían a la ropa y a la piel como una película grasienta. En el horizonte de basalto, los monolitos de la Academia Militar recortaban sus ángulos imposibles contra un cielo color plomo. Cientos de aspirantes aguardaban en silencio, con los ojos clavados en las inscripciones borradas de las murallas ciclópeas. Nadie entendía realmente lo que significaba estar allí; la propaganda imperial prometía gloria en la guerra contra el monarca Ares, pero el suelo vibraba con la frialdad de un matadero mecanizado.

Oscar respiró hondo, ralentizando el ritmo de su pulso por debajo de las sesenta pulsaciones. No destacaba entre la masa. Su estatura era media, su mirada deliberadamente neutra, sus gestos comedidos. En un entorno diseñado para triturar voluntades, el ego era un blanco fácil. Su objetivo no era brillar ni llamar la atención de los oficiales: era observar, calcular y sobrevivir sin dejar rastro de su verdadera capacidad."""
        },
        {
            "chapter_number": 1,
            "chapter_title": "Capítulo 1: El Umbral de la Academia",
            "act_title": "Acto I: La Academia",
            "narrative": """Paso bajo el arco monumental de piedra negra de la Academia Militar. El viento de la meseta arrastra ceniza y los estandartes contra Ares azotan el cielo gris. Entre los cadetes que aguardan la primera prueba en el patio de armas, mis ojos se cruzan con una joven de porte letal: Virginia.

No hay miedo en su postura. A diferencia del resto de los aspirantes, que miran a su alrededor con la inquietud de animales enjaulados, Virginia examina las salidas de emergencia, la ubicación de las cámaras perimétricas y las junturas del blindaje de los instructores. Sus ojos, afilados y desprovistos de compasión innecesaria, se posan en mí durante una fracción de segundo demasiado larga.

De pronto, un dolor punzante atraviesa la base de mi cráneo. Un destello de déjà vu brutal me sacude las sienes: no es un recuerdo ordinario, sino la sensación nítida de haber visto a Virginia caer en un pasillo en penumbra, empapada en sangre, mientras una figura colosal cubierta por una armadura dorada avanzaba entre los escombros. Ares. El nombre retumba en mi mente con el peso de mil vidas que nunca he vivido.

Parpadeo. La visión se disipa en un latido. El instructor al frente de la plaza da la orden de formación, y Virginia sigue en pie, observándome con una ceja ligeramente arqueada. Ella también ha notado que algo ha cambiado en el aire."""
        },
        {
            "chapter_number": 2,
            "chapter_title": "Capítulo 2: El Escalafón de Hierro",
            "act_title": "Acto I: La Academia",
            "narrative": """La jerarquía en la Academia no se establece con discursos, sino con sangre y pruebas tácticas implacables. Los cadetes son clasificados en rangos numéricos visibles en los terminales de cada dormitorio: los primeros escalones obtienen privilegios estratégicos; los últimos son descartados o enviados a las líneas de choque como carne de cañón.

Mi estrategia permanece inalterada: mantenerme exactamente en el percentil medio. Ni tan bajo como para arriesgar la purga, ni tan alto como para despertar las sospechas de los cadetes de élite o de los prefectos de disciplina.

Durante la primera prueba de reflejos y cálculo bajo presión balística en el polígono, un fragmento de proyectil desviado sale disparado hacia mi sien. Debería haberme impactado de lleno. Sin embargo, en el instante exacto del impacto, el tiempo parece condensarse en un fluido viscoso. Veo la trayectoria del fragmento con una nitidez imposible, girando sobre sí mismo micrómetro a micrómetro. Mi cuerpo se inclina dos centímetros hacia la izquierda antes de que mi mente racional pueda procesar la orden.

El proyectil corta el aire a milímetros de mi oreja y se incrusta en el mamparo trasero. A mi lado, dos cadetes respiran agitados creyendo que ha sido un golpe de suerte milagroso. Yo contemplo la palma de mi mano, donde un cosquilleo eléctrico se apaga lentamente. No ha sido suerte. Hay algo dentro de mí que percibe las ondas del tiempo antes de que colapsen en el presente."""
        }
    ]
    
    export_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
    os.makedirs(export_dir, exist_ok=True)
    file_path = os.path.join(export_dir, "Arquimedes_Libro_I_La_Voluntad_de_las_Cenizas_Completo.epub")
    
    create_epub(
        passages=passages,
        output_path=file_path,
        book_title="Arquímedes // Libro I: La Voluntad de las Cenizas",
        author="Oscar Bueno"
    )
    print(f"Obra canónica compilada con éxito en: {file_path}")

if __name__ == "__main__":
    build_complete_canonical_novel()
