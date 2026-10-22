import os
import sys
import time
import argparse
from main import start_game, play_turn, TurnRequest, load_game
from database import get_story_passages
from epub_builder import create_epub

def generate_offline_book(session_id: str = "novela_completa_offline", target_chapters: int = 15, author: str = "Oscar Bueno"):
    print(f"=== GENERADOR DE NOVELA COMPLETA: ARQUÍMEDES ===")
    print(f"ID de Sesión: {session_id} | Capítulos objetivo: {target_chapters}")
    
    # 1. Iniciar partida canónica
    print("\n[1/3] Escribiendo el Capítulo 1 canónico...")
    res = start_game(session_id=session_id, reiniciar=True)
    print(f"✓ {res.chapter_title}")
    
    current_chapter = res.chapter_number
    turn_count = 1
    
    # 2. Bucle de avance autónomo
    while current_chapter <= target_chapters:
        # Si es encrucijada, elegir según psicología de Oscar
        if res.is_crossroad and res.options:
            # Priorizamos decisiones analíticas o de sigilo para descubrir el enigma
            eleccion = res.options[0].label
            for opt in res.options:
                if opt.approach in ("analitico", "sigilo"):
                    eleccion = opt.label
                    break
            print(f"\n[Encrucijada - Cap {current_chapter}] Oscar decide: '{eleccion[:65]}...'")
        else:
            eleccion = res.options[0].label if res.options else "Continuar leyendo..."
            print(f".", end="", flush=True)

        req = TurnRequest(session_id=session_id, player_choice=eleccion)
        try:
            res = play_turn(req)
            turn_count += 1
            current_chapter = res.chapter_number
            if res.is_game_over:
                print(f"\n[Fin de la trama] {res.game_over_reason}")
                break
        except Exception as e:
            print(f"\n[Reintento temporal ante demora de red: {e}]")
            time.sleep(2)

    # 3. Compilación a EPUB
    print(f"\n\n[3/3] Compilando obra completa en formato EPUB...")
    passages = get_story_passages(session_id)
    export_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
    os.makedirs(export_dir, exist_ok=True)
    output_epub = os.path.join(export_dir, f"{session_id}.epub")
    
    create_epub(
        passages=passages,
        output_path=output_epub,
        book_title="Arquímedes: La Voluntad de las Cenizas",
        author=author
    )
    print(f"\n¡NOVELA COMPILADA CON ÉXITO!\nArchivo EPUB disponible en:\n{output_epub}\n")
    return output_epub

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Genera una novela completa de Arquímedes en EPUB")
    parser.add_argument("--session_id", default="arquimedes_offline_v1", help="Identificador de la novela")
    parser.add_argument("--chapters", type=int, default=10, help="Número de capítulos a escribir")
    parser.add_argument("--author", default="Oscar Bueno", help="Nombre del autor")
    args = parser.parse_args()

    generate_offline_book(session_id=args.session_id, target_chapters=args.chapters, author=args.author)
