import os
import time
import json
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Cargar variables de entorno desde .env en la misma carpeta del script
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(env_path)

# NUEVO SDK DE GOOGLE
from google import genai
from google.genai import types

from models import GameState, TurnoIAResponse, TurnoClienteResponse, ActionOption
from engine import GameEngine
from prompts import build_system_prompt, build_user_prompt
from story_architect import generate_book_outline
from database import init_db, save_game, load_game, list_games, load_outline, delete_game, record_passage, get_story_passages
from epub_builder import create_epub
from fastapi.responses import FileResponse

# 1. INICIALIZAR EL SERVIDOR Y LA BASE DE DATOS
app = FastAPI(title="Ares Chronos API - Novel Engine")
init_db()  # Crea el archivo partidas.db y migra columnas si no existen

# Habilitar CORS para permitir conexión desde el iPad o cualquier dispositivo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. CONFIGURAR GEMINI (Nuevo SDK)
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(
        retry_options=types.HttpRetryOptions(attempts=1)
    )
)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

# Reglas de generación estructurada
generation_config = types.GenerateContentConfig(
    system_instruction=build_system_prompt(),
    response_mime_type="application/json",
    response_schema=TurnoIAResponse,
    temperature=0.75
)

# 3. RUTAS DE LA API
class TurnRequest(BaseModel):
    session_id: str
    player_choice: str

def llamar_gemini_seguro(prompt: str) -> TurnoIAResponse:
    """Llama a Gemini con modelo de respaldo inmediato ante saturación de Google (503)."""
    modelos_candidatos = [
        GEMINI_MODEL,
        "gemini-3.5-flash",
        "gemini-3.6-flash",
        "gemini-3.5-flash-lite",
        "gemini-3.8-flash"
    ]
    modelos_a_probar = list(dict.fromkeys(modelos_candidatos))
    ultimo_error = None

    for modelo in modelos_a_probar:
        try:
            response = client.models.generate_content(
                model=modelo,
                contents=prompt,
                config=generation_config
            )
            raw_text = response.text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            elif raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            return TurnoIAResponse.model_validate_json(raw_text.strip())
        except Exception as e:
            ultimo_error = e
            print(f"[Arquímedes Engine] Fallback desde {modelo}: {e}", flush=True)

    # Si todos los modelos fallan, lanzamos un 503 limpio
    raise HTTPException(
        status_code=503,
        detail=f"Sobrecarga temporal de Google AI: {ultimo_error}. Toca reconectar en unos segundos."
    )

@app.get("/")
def read_root():
    return {
        "status": "online",
        "engine": "Arquímedes Novel Engine v1.0 (Documento Maestro Canónico)",
        "model": GEMINI_MODEL
    }

@app.get("/api/games")
def get_all_games():
    """Devuelve la lista de todas las novelas guardadas para el menú del iPad."""
    return list_games()

@app.post("/api/start", response_model=TurnoClienteResponse)
def start_game(session_id: str = "partida_001", reiniciar: bool = False):
    """Inicia una novela: establece el inicio canónico de Arquímedes y escribe el Capítulo 1."""
    estado_existente = load_game(session_id)
    if estado_existente and not reiniciar:
        raise HTTPException(
            status_code=400, 
            detail="Esta novela ya existe. Usa reiniciar=true para empezar de nuevo o /api/turn para continuarla."
        )

    # Estado Inicial Canónico según Documento Maestro
    estado_inicial = GameState(
        session_id=session_id,
        chapter_number=1,
        chapter_title="Capítulo 1: El Umbral de la Academia",
        act_number=1,
        act_title="Acto I: La Puerta de Hierro y Ceniza",
        confirmed_facts=[
            "Oscar ingresa como cadete ordinario en la Academia Militar para prepararse en la guerra contra el monarca Ares."
        ],
        open_threads=[
            "¿Qué oculta la historia oficial de la civilización perdida y el verdadero origen de Ares?",
            "¿Quién es la cadete Virginia y qué busca en esta institución?"
        ],
        active_branch="Cadete de la Academia"
    )
    
    # Inicio canónico siempre idéntico
    accion_inicial = (
        "Paso bajo el arco monumental de piedra negra de la Academia Militar. "
        "El viento de la meseta arrastra ceniza y los estandartes contra Ares azotan el cielo gris. "
        "Entre los cadetes que aguardan la primera prueba en el patio de armas, mis ojos se cruzan con una joven de porte letal: Virginia."
    )

    # 1. GENERAR LA ESCALETA MAESTRA SECRETA (El Guionista Ciego de Arquímedes)
    outline_json = None
    outline_dict = None
    try:
        print(f"[Arquímedes Engine] Diseñando escaleta de 4 actos para {session_id}...")
        outline = generate_book_outline(client, GEMINI_MODEL)
        outline_json = outline.model_dump_json()
        outline_dict = outline.model_dump()
        if outline.acts:
            estado_inicial.act_title = f"Acto {outline.acts[0].act_number}: {outline.acts[0].act_title}"
        print(f"[Arquímedes Engine] Escaleta estructurada con éxito: '{outline.book_title}'")
    except Exception as e:
        print(f"[Arquímedes Engine] Advertencia generando escaleta: {e}")

    # 2. ESCRIBIR EL PRIMER CAPÍTULO CANÓNICO
    prompt = build_user_prompt(estado_inicial, accion_inicial, outline_dict)
    ai_data = llamar_gemini_seguro(prompt)
    resultado = GameEngine.process_turn(estado_inicial, ai_data, accion_inicial)
    
    # 3. GUARDAR EN LA BASE DE DATOS
    save_game(estado_inicial, outline_json=outline_json)
    record_passage(
        session_id=session_id,
        turn_number=resultado.turn_number,
        act_title=resultado.act_title,
        chapter_number=resultado.chapter_number,
        chapter_title=resultado.chapter_title,
        narrative=resultado.narrative,
        player_choice=accion_inicial
    )
    
    return resultado

@app.post("/api/turn", response_model=TurnoClienteResponse)
def play_turn(req: TurnRequest):
    """Avanza la novela: lee la escaleta secreta, procesa la decisión y escribe la siguiente escena."""
    estado = load_game(req.session_id)
    if not estado:
        raise HTTPException(status_code=404, detail="El bucle temporal (sesión) no existe.")
        
    # Recuperar la escaleta de esta novela
    outline_dict = None
    outline_raw = load_outline(req.session_id)
    if outline_raw:
        try:
            outline_dict = json.loads(outline_raw)
        except Exception:
            pass

    prompt = build_user_prompt(estado, req.player_choice, outline_dict)
    ai_data = llamar_gemini_seguro(prompt)
    
    resultado = GameEngine.process_turn(estado, ai_data, req.player_choice)
    save_game(estado)
    record_passage(
        session_id=req.session_id,
        turn_number=resultado.turn_number,
        act_title=resultado.act_title,
        chapter_number=resultado.chapter_number,
        chapter_title=resultado.chapter_title,
        narrative=resultado.narrative,
        player_choice=req.player_choice
    )
    
    return resultado

@app.get("/api/game/{session_id}", response_model=TurnoClienteResponse)
def get_game(session_id: str):
    """Devuelve el turno actual de la partida para reanudar sin consumir llamadas a Gemini."""
    estado = load_game(session_id)
    if not estado:
        raise HTTPException(status_code=404, detail="Partida no encontrada")
    
    # Soporte retroactivo para sesiones anteriores
    narrativa = estado.last_narrative
    if not narrativa:
        if estado.recent_turns:
            narrativa = f"[REANUDANDO BUCLE TEMPORAL]\n\nÚltimo suceso registrado: {estado.recent_turns[-1].summary}"
        else:
            narrativa = "El bucle temporal espera tu retorno. Elige cómo avanzar..."

    opciones = estado.last_options
    if not opciones:
        opciones = [
            ActionOption(
                label="Continuar la marcha por el conducto en sombras...",
                approach="analitico",
                risk_level="bajo"
            )
        ]

    return TurnoClienteResponse(
        session_id=estado.session_id,
        turn_number=max(1, estado.turn_number - 1),
        chapter_number=getattr(estado, "chapter_number", 1),
        chapter_title=getattr(estado, "chapter_title", "Capítulo 1: El Umbral de la Academia"),
        act_title=getattr(estado, "act_title", "Acto I: La Puerta de Hierro y Ceniza"),
        narrative=narrativa,
        health=estado.health,
        entropy=estado.entropy,
        virginia=estado.virginia,
        inventory=estado.inventory,
        lore_ledger=estado.lore_ledger,
        confirmed_facts=getattr(estado, "confirmed_facts", []),
        open_threads=getattr(estado, "open_threads", []),
        active_branch=getattr(estado, "active_branch", "Cadete de la Academia"),
        is_crossroad=getattr(estado, "last_is_crossroad", False),
        options=opciones,
        is_game_over=getattr(estado, "is_game_over", estado.health <= 0 or estado.entropy >= 100),
        game_over_reason=getattr(estado, "game_over_reason", None),
        scene_tempo=getattr(estado, "last_scene_tempo", "tension_latente"),
        art_prompt=getattr(estado, "last_art_prompt", None)
    )

@app.delete("/api/game/{session_id}")
def remove_game(session_id: str):
    """Elimina una partida guardada."""
    success = delete_game(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Partida no encontrada para eliminar")
    return {"status": "deleted", "session_id": session_id}

@app.get("/api/game/{session_id}/export/epub")
def export_game_epub(session_id: str):
    """Compila y entrega la novela completa en formato EPUB estándar para Apple Books o Kindle."""
    passages = get_story_passages(session_id)
    if not passages:
        # Si no hay pasajes históricos grabados en story_passages, intentar rescatar la última narrativa
        estado = load_game(session_id)
        if estado and estado.last_narrative:
            passages = [{
                "turn_number": estado.turn_number,
                "act_title": estado.act_title,
                "chapter_number": estado.chapter_number,
                "chapter_title": estado.chapter_title,
                "narrative": estado.last_narrative,
                "player_choice": "Inicio de la lectura"
            }]
        else:
            raise HTTPException(status_code=404, detail="No hay escenas registradas para compilar esta novela.")

    export_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
    os.makedirs(export_dir, exist_ok=True)
    filename = f"{session_id}.epub"
    file_path = os.path.join(export_dir, filename)

    create_epub(
        passages=passages,
        output_path=file_path,
        book_title="Arquímedes: La Voluntad de las Cenizas",
        author="Oscar Bueno"
    )

    return FileResponse(
        path=file_path,
        filename=f"Arquimedes_La_Voluntad_de_las_Cenizas_{session_id}.epub",
        media_type="application/epub+zip"
    )
