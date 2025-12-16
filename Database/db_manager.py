import sqlite3
import os

# Naming the database
db_name="TradeEngine.db"
# Determine paths relative to this file location
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, db_name)
schema_path = os.path.join(base_dir, 'schema.sql')

def get_connection():
    # Opens and returns a database connection.
    conn = sqlite3.connect(db_path)
    # This line enables accessing columns by name instead of index (Very Important)
    conn.row_factory = sqlite3.Row
    return conn

def init_schema():
    # Reads schema.sql file and executes it to build tables.
    print(f"⚙️  Initializing database at: {db_path}...")
    
    if not os.path.exists(schema_path):
        print(f"❌ Error: schema.sql not found at {schema_path}")
        return

    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        conn = get_connection()
        cursor = conn.cursor()
        # executescript runs the entire SQL script at once
        cursor.executescript(schema_sql)
        conn.commit()
        conn.close()
        print("✅ Database schema initialized successfully!")
        print("✅ All 5 tables created successfully.")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")

# This block is for testing running the file directly
if __name__ == "__main__":
    # Uncomment the next line if you want to delete the old DB and start fresh
    # if os.path.exists(db_path): os.remove(db_path)
    init_schema()