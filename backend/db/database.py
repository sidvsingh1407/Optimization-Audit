import sqlite3
import os

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
DB_PATH = os.path.join(DB_DIR, "audit_system.db")

def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Graph Entities Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS graph_entities (
        entity_id TEXT PRIMARY KEY,
        audit_id TEXT NOT NULL,
        entity_type TEXT NOT NULL,
        entity_name TEXT NOT NULL,
        metadata_json TEXT
    )
    ''')

    # Graph Relationships Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS graph_relationships (
        relationship_id TEXT PRIMARY KEY,
        audit_id TEXT NOT NULL,
        source_entity_id TEXT NOT NULL,
        target_entity_id TEXT NOT NULL,
        relationship_type TEXT NOT NULL,
        relationship_strength REAL DEFAULT 1.0,
        metadata_json TEXT,
        FOREIGN KEY(source_entity_id) REFERENCES graph_entities(entity_id),
        FOREIGN KEY(target_entity_id) REFERENCES graph_entities(entity_id)
    )
    ''')

    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_PATH)

if __name__ == "__main__":
    init_db()
