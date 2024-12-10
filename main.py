import sqlite3
import streamlit as st

# Database connection
def get_db_connection():
    conn = sqlite3.connect("my_database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Streamlit app
def main():
    st.title("SQLite with Streamlit")

    # Display existing data
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    st.subheader("Current Data")
    for row in rows:
        st.write(dict(row))

    # Add new data
    st.subheader("Add New User")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    if st.button("Add User"):
        if name and age:
            cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
            conn.commit()
            st.success("User added successfully!")
            st.experimental_rerun()
        else:
            st.error("Please provide valid inputs.")

    conn.close()

if __name__ == "__main__":
    main()
