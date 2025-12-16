import sqlite3
import os

class DBManager:
    def __init__(self, db_name="store.db"):
        # Determine paths relative to this file location
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_name)
        self.schema_path = os.path.join(base_dir, 'schema.sql')

    def get_connection(self):
        """Opens and returns a database connection."""
        conn = sqlite3.connect(self.db_path)
        # This line enables accessing columns by name instead of index (Very Important)
        conn.row_factory = sqlite3.Row
        return conn

    def init_schema(self):
        """Reads schema.sql file and executes it to build tables."""
        print(f"⚙️  Initializing database at: {self.db_path}...")
        
        if not os.path.exists(self.schema_path):
            print(f"❌ Error: schema.sql not found at {self.schema_path}")
            return

        try:
            with open(self.schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()

            conn = self.get_connection()
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
    db = DBManager()
    # Uncomment the next line if you want to delete the old DB and start fresh
    # if os.path.exists(db.db_path): os.remove(db.db_path)
    db.init_schema()