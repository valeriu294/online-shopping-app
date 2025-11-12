import sqlite3

def inspect_database():
    """Inspect the database to find actual table names and structures"""
    try:
        conn = sqlite3.connect('orinoco.db')
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("Tables in the database:")
        print("=" * 50)
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")
            
            # Get column information for each table
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print("Columns:")
            for col in columns:
                col_id, col_name, col_type, not_null, default_val, pk = col
                pk_indicator = " (PRIMARY KEY)" if pk else ""
                null_indicator = " NOT NULL" if not_null else ""
                print(f"  - {col_name}: {col_type}{pk_indicator}{null_indicator}")
            
            # Show sample data (first 3 rows)
            try:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                sample_data = cursor.fetchall()
                if sample_data:
                    print("Sample data (first 3 rows):")
                    for i, row in enumerate(sample_data, 1):
                        print(f"  Row {i}: {row}")
                else:
                    print("No data in this table")
            except Exception as e:
                print(f"Could not fetch sample data: {e}")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_database()