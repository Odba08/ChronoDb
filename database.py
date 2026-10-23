import os
import sqlite3
from datetime import datetime
from typing import List, Optional
from models import GameState

# El archivo físico de la base de datos (configurable vía DB_PATH para servidores en la nube)
DB_FILE = os.getenv("DB_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "partidas.db"))

def get_connection():
    """Crea una conexión con timeout extendido para evitar bloqueos."""
    return sqlite3.connect(DB_FILE, timeout=30)

def init_db():
    """Se ejecuta al iniciar el servidor para asegurar que la tabla existe y está al día."""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Activar modo WAL (Write-Ahead Logging) para concurrencia y máxima robustez
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                session_id TEXT PRIMARY KEY,
                last_updated TEXT,
                state_data TEXT
            )
        ''')
        # Migración segura: Añadir columna outline_data si no existe aún
        cursor.execute("PRAGMA table_info(games)")
        columnas = [col[1] for col in cursor.fetchall()]
        if "outline_data" not in columnas:
            cursor.execute("ALTER TABLE games ADD COLUMN outline_data TEXT")
            
        # Tabla permanente para compilar y exportar el libro a EPUB
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS story_passages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                turn_number INTEGER,
                act_title TEXT,
                chapter_number INTEGER,
                chapter_title TEXT,
                narrative TEXT,
                player_choice TEXT,
                created_at TEXT
            )
        ''')
        conn.commit()

def record_passage(session_id: str, turn_number: int, act_title: str, chapter_number: int, chapter_title: str, narrative: str, player_choice: str):
    """Guarda cada escena redactada en orden cronológico para la compilación del libro."""
    now = datetime.now().isoformat()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO story_passages (session_id, turn_number, act_title, chapter_number, chapter_title, narrative, player_choice, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session_id, turn_number, act_title, chapter_number, chapter_title, narrative, player_choice, now))
        conn.commit()

def get_story_passages(session_id: str) -> List[dict]:
    """Recupera todas las escenas de la novela para exportar a EPUB."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT turn_number, act_title, chapter_number, chapter_title, narrative, player_choice, created_at
            FROM story_passages
            WHERE session_id = ?
            ORDER BY id ASC
        ''', (session_id,))
        rows = cursor.fetchall()
        return [
            {
                "turn_number": r[0],
                "act_title": r[1],
                "chapter_number": r[2],
                "chapter_title": r[3],
                "narrative": r[4],
                "player_choice": r[5],
                "created_at": r[6]
            }
            for r in rows
        ]

def save_game(state: GameState, outline_json: Optional[str] = None):
    """Guarda o sobreescribe la partida actual y su escaleta secreta de novela."""
    state_json = state.model_dump_json()
    now = datetime.now().isoformat()
    
    with get_connection() as conn:
        cursor = conn.cursor()
        if outline_json:
            cursor.execute('''
                INSERT INTO games (session_id, last_updated, state_data, outline_data)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(session_id) DO UPDATE SET
                    last_updated=excluded.last_updated,
                    state_data=excluded.state_data,
                    outline_data=excluded.outline_data
            ''', (state.session_id, now, state_json, outline_json))
        else:
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
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT state_data FROM games WHERE session_id = ?', (session_id,))
        row = cursor.fetchone()
        
    if row and row[0]:
        return GameState.model_validate_json(row[0])
    return None

def load_outline(session_id: str) -> Optional[str]:
    """Recupera la escaleta maestra secreta de la novela en formato JSON."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT outline_data FROM games WHERE session_id = ?', (session_id,))
        row = cursor.fetchone()
        
    if row and row[0]:
        return row[0]
    return None

def list_games() -> List[dict]:
    """Devuelve el listado de todas las partidas guardadas para el menú de cargar partida."""
    with get_connection() as conn:
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
                "chapter_number": getattr(state, "chapter_number", 1),
                "chapter_title": getattr(state, "chapter_title", "Capítulo 1"),
                "act_title": getattr(state, "act_title", "Acto I"),
                "health": state.health,
                "entropy": state.entropy,
                "virginia_status": f"{state.virginia.status} ({state.virginia.intensity}/10)",
                "active_branch": getattr(state, "active_branch", "Cadete de la Academia"),
                "is_game_over": state.health <= 0 or state.entropy >= 100
            })
        except Exception:
            result.append({
                "session_id": row[0],
                "last_updated": row[1]
            })
    return result

def delete_game(session_id: str) -> bool:
    """Elimina una partida, su escaleta y sus escenas registradas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM games WHERE session_id = ?', (session_id,))
        deleted_games = cursor.rowcount
        cursor.execute('DELETE FROM story_passages WHERE session_id = ?', (session_id,))
        conn.commit()
        return deleted_games > 0 or True  # Asegura que siempre se considere exitoso si no hubo excepción SQL
