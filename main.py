import sqlite3
import streamlit as st

def initialize_db():
    conn = sqlite3.connect("my_database.db")
    cursor = conn.cursor()
    
    # Create the `users` table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()
    
# Database connection
def get_db_connection():
    conn = sqlite3.connect("my_database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Streamlit app
def main():
    # Initialize the database and table
    initialize_db()

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Try to fetch data from the `users` table
    try:
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        st.subheader("Current Data")
        for row in rows:
            st.write(row)
    except sqlite3.OperationalError as e:
        st.error(f"Database error: {e}")

    # Add new data
    st.subheader("Add New User")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    if st.button("Add User"):
        if name and age:
            cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
            conn.commit()
            st.success("User added successfully!")
        else:
            st.error("Please provide valid inputs.")

    conn.close()

if __name__ == "__main__":
    main()
