import streamlit as st
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import time

# ---------------- DATABASE ---------------- #
conn = sqlite3.connect("physics.db", check_same_thread=False)
cursor = conn.cursor()

# Users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
''')

# Topics table
cursor.execute('''
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_name TEXT
)
''')

conn.commit()

# ---------------- SESSION STATE ---------------- #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# ---------------- AUTH FUNCTIONS ---------------- #
def login_user(username, password):
    user = cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    ).fetchone()
    return user

def register_user(username, password, role):
    try:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, password, role)
        )
        conn.commit()
        return True
    except:
        return False

# ---------------- UI ---------------- #
st.title("Physics Learning & Simulation System")

menu = ["Login", "Register"]
if not st.session_state.logged_in:
    choice = st.sidebar.selectbox("Menu", menu)

    # -------- REGISTER -------- #
    if choice == "Register":
        st.subheader("Create Account")
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["Student", "Teacher"])

        if st.button("Register"):
            if register_user(new_user, new_pass, role):
                st.success("Account created successfully!")
            else:
                st.error("Username already exists.")

    # -------- LOGIN -------- #
    elif choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = user[1]
                st.session_state.role = user[3]
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials.")

# ---------------- DASHBOARD ---------------- #
else:
    st.sidebar.write(f"Logged in as: {st.session_state.username}")
    st.sidebar.write(f"Role: {st.session_state.role}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # -------- TEACHER VIEW -------- #
    if st.session_state.role == "Teacher":
        st.header("Teacher Dashboard")

        topic = st.text_input("Add Physics Topic")
        if st.button("Add Topic"):
            cursor.execute("INSERT INTO topics (topic_name) VALUES (?)", (topic,))
            conn.commit()
            st.success("Topic Added!")

        st.subheader("All Topics")
        topics = cursor.execute("SELECT topic_name FROM topics").fetchall()
        for t in topics:
            st.write(t[0])

    # -------- STUDENT VIEW -------- #
    elif st.session_state.role == "Student":
        st.header("Student Dashboard")

        topics = cursor.execute("SELECT topic_name FROM topics").fetchall()
        topic_list = [t[0] for t in topics]

        if topic_list:
            selected_topic = st.selectbox("Choose Topic", topic_list)

            # -------- NEWTON'S FIRST LAW -------- #
            if selected_topic.lower() == "newton's first law":
                st.write("Simulation: Inertia")

                friction = st.checkbox("Add Friction")
                position = 0
                velocity = 0.1
                plot_area = st.empty()

                for i in range(150):
                    fig, ax = plt.subplots()
                    ax.set_xlim(0, 10)
                    ax.set_ylim(0, 1)
                    ax.plot(position, 0.5, 'o', markersize=15)

                    if friction:
                        velocity *= 0.98
                    position += velocity

                    plot_area.pyplot(fig)
                    time.sleep(0.03)

            # -------- NEWTON'S SECOND LAW -------- #
            elif selected_topic.lower() == "newton's second law":
                st.write("Simulation: F = ma")

                force = st.slider("Force (N)", 1, 20, 5)
                mass = st.slider("Mass (kg)", 1, 10, 2)

                acceleration = force / mass
                st.write(f"Acceleration = {acceleration:.2f} m/s²")

                time_vals = np.linspace(0, 5, 100)
                position = 0.5 * acceleration * time_vals**2

                fig, ax = plt.subplots()
                ax.plot(time_vals, position)
                ax.set_xlabel("Time (s)")
                ax.set_ylabel("Position (m)")
                st.pyplot(fig)

            else:
                st.info("No simulation available yet.")
        else:
            st.warning("No topics available yet.")


    else:
        st.warning("No topics added yet.")
