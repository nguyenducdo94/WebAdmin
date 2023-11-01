import mysql.connector

def connect_to_database():
    db_config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '',
        'database': 'webxemphim',
        'charset': 'utf8mb4',
        'use_pure': True 
    }

    conn = mysql.connector.connect(**db_config)
    return conn

def execute_query(query, commit=False):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute(query)

        if commit:
            conn.commit()
            return True
        else:
            results = cursor.fetchall()
            cursor.close()
            return results
    except Exception as e:
        print(f"Error executing query: {str(e)}")
        return False
    finally:
        close_connection(conn)
        cursor.close()

def close_connection(conn):
    conn.close()
