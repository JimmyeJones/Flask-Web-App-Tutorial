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
    # Initialize the database
    initialize_db()

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch data from the users table
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    # Convert sqlite3.Row to dictionary for display
    st.subheader("Current Data")
    formatted_rows = [dict(row) for row in rows]  # Convert each row to a dictionary
    for row in formatted_rows:
        st.write(row)

    # Add new data
    st.subheader("Add New User")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    if st.button("Add User"):
        if name and age:
            cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
            conn.commit()
            st.success("User added successfully!")
            st.experimental_rerun()  # Optional: Only if supported
        else:
            st.error("Please provide valid inputs.")

    conn.close()


if __name__ == "__main__":
    main()
