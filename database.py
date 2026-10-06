import sqlite3
from datetime import datetime
from typing import List, Optional
from models import GameState

# El archivo físico de la base de datos
DB_FILE = "partidas.db"

def init_db():
    """Se ejecuta al iniciar el servidor para asegurar que la tabla existe."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                session_id TEXT PRIMARY KEY,
                last_updated TEXT,
                state_data TEXT
            )
        ''')
        conn.commit()

def save_game(state: GameState):
    """Guarda o sobreescribe la partida actual (Upsert seguro)."""
    state_json = state.model_dump_json()
    now = datetime.now().isoformat()
    
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO games (session_id, last_updated, state_data)
            VALUES (?, ?, ?)
            ON CONFLICT(session_id) DO UPDATE SET
                last_updated=excluded.last_updated,
                state_data=excluded.state_data
        ''', (state.session_id, now, state_json))
        conn.commit()

def load_game(session_id: str) -> Optional[GameState]:
    """Busca el JSON en la base de datos y lo vuelve a convertir en un objeto Pydantic."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT state_data FROM games WHERE session_id = ?', (session_id,))
        row = cursor.fetchone()
        
    if row:
        return GameState.model_validate_json(row[0])
    return None

def list_games() -> List[dict]:
    """Devuelve el listado de todas las partidas guardadas para el menú de cargar partida."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT session_id, last_updated, state_data FROM games ORDER BY last_updated DESC')
        rows = cursor.fetchall()

    result = []
    for row in rows:
        try:
            state = GameState.model_validate_json(row[2])
            result.append({
                "session_id": row[0],
                "last_updated": row[1],
                "turn_number": state.turn_number,
                "health": state.health,
                "entropy": state.entropy,
                "virginia_status": f"{state.virginia.status} ({state.virginia.intensity}/10)",
                "is_game_over": state.game_over
            })
        except Exception:
            result.append({
                "session_id": row[0],
                "last_updated": row[1]
            })
    return result