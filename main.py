import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Cargar variables de entorno desde .env
load_dotenv()

# NUEVO SDK DE GOOGLE
from google import genai
from google.genai import types

from models import GameState, TurnoIAResponse, TurnoClienteResponse
from engine import GameEngine
from prompts import build_system_prompt, build_user_prompt

# NUEVAS IMPORTACIONES DE BASE DE DATOS
from database import init_db, save_game, load_game, list_games

# 1. INICIALIZAR EL SERVIDOR Y LA BASE DE DATOS
app = FastAPI(title="Arquimedes API")
init_db()  # Crea el archivo partidas.db si no existe

# Habilitar CORS para permitir conexión desde el iPad o cualquier navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. CONFIGURAR GEMINI (Nuevo SDK)
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-lite-latest")

# Reglas de generación estructurada
generation_config = types.GenerateContentConfig(
    system_instruction=build_system_prompt(),
    response_mime_type="application/json",
    response_schema=TurnoIAResponse,
    temperature=0.7
)

# 3. RUTAS DE LA API
class TurnRequest(BaseModel):
    session_id: str
    player_choice: str

def llamar_gemini_seguro(prompt: str) -> TurnoIAResponse:
    """Llama a Gemini y valida la respuesta con reintento si ocurre error de formato."""
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=generation_config
        )
        return TurnoIAResponse.model_validate_json(response.text)
    except Exception as e:
        print(f"[Arquimedes Engine] Reintentando generación tras advertencia: {e}")
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt + "\n\nAsegúrate de que cada opción tenga un approach estrictamente único.",
            config=generation_config
        )
        return TurnoIAResponse.model_validate_json(response.text)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "engine": "Arquimedes Backend v1.2 (Persistencia SQLite)",
        "model": GEMINI_MODEL
    }

@app.get("/api/games")
def get_all_games():
    """Devuelve la lista de todas las partidas guardadas para el menú de cargar partida."""
    return list_games()

@app.post("/api/start", response_model=TurnoClienteResponse)
def start_game(session_id: str = "partida_001", reiniciar: bool = False):
    """Inicia una partida nueva y la guarda en SQLite. Usa reiniciar=True para sobrescribir."""
    estado_existente = load_game(session_id)
    if estado_existente and not reiniciar:
        raise HTTPException(
            status_code=400, 
            detail="Esta partida ya existe. Usa ?reiniciar=true para empezar de nuevo o /api/turn para continuarla."
        )

    estado_inicial = GameState(session_id=session_id)
    accion_inicial = "Abro los ojos e intento orientarme en la zona de cuarentena."
    prompt = build_user_prompt(estado_inicial, accion_inicial)
    
    ai_data = llamar_gemini_seguro(prompt)
    resultado = GameEngine.process_turn(estado_inicial, ai_data, accion_inicial)
    
    # GUARDAR EN BASE DE DATOS
    save_game(estado_inicial)
    
    return resultado

@app.post("/api/turn", response_model=TurnoClienteResponse)
def play_turn(req: TurnRequest):
    """Carga la partida de SQLite, procesa la decisión y vuelve a guardar."""
    # 1. CARGAMOS LA PARTIDA DESDE LA DB
    estado = load_game(req.session_id)
    if not estado:
        raise HTTPException(status_code=404, detail="El bucle temporal (sesión) no existe.")
        
    prompt = build_user_prompt(estado, req.player_choice)
    ai_data = llamar_gemini_seguro(prompt)
    
    # 2. PROCESAMOS EL TURNO
    resultado = GameEngine.process_turn(estado, ai_data, req.player_choice)
    
    # 3. GUARDAMOS EL PROGRESO ACTUALIZADO
    save_game(estado)
    
    return resultado

@app.get("/api/game/{session_id}")
def get_game(session_id: str):
    """Devuelve el estado completo de una partida para cargar el menú en el frontend."""
    estado = load_game(session_id)
    if not estado:
        raise HTTPException(status_code=404, detail="Partida no encontrada")
    return estado