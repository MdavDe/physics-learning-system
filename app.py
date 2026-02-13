import streamlit as st
import sqlite3

conn = sqlite3.connect("physics.db", check_same_thread=False)
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                role TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_name TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assignment_name TEXT,
                topic TEXT,
                marks INTEGER)''')

conn.commit()

st.title("Physics Learning Management System")

menu = ["Home", "Add Topic", "Add Assignment", "View Assignments"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.subheader("Welcome to the Physics LMS")
    st.write("Manage physics topics and assignments.")

elif choice == "Add Topic":
    st.subheader("Add Physics Topic")
    topic = st.text_input("Topic Name")
    if st.button("Add Topic"):
        c.execute("INSERT INTO topics (topic_name) VALUES (?)", (topic,))
        conn.commit()
        st.success("Topic Added Successfully!")

elif choice == "Add Assignment":
    st.subheader("Add Assignment")
    assignment = st.text_input("Assignment Name")
    topic = st.text_input("Topic")
    marks = st.number_input("Marks", min_value=0, max_value=100)
    if st.button("Add Assignment"):
        c.execute("INSERT INTO assignments (assignment_name, topic, marks) VALUES (?,?,?)",
                  (assignment, topic, marks))
        conn.commit()
        st.success("Assignment Added!")

elif choice == "View Assignments":
    st.subheader("All Assignments")
    data = c.execute("SELECT * FROM assignments").fetchall()
    for row in data:
        st.write(f"Assignment: {row[1]} | Topic: {row[2]} | Marks: {row[3]}")
