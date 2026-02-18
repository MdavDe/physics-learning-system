import streamlit as st
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ---------------- DATABASE ---------------- #
conn = sqlite3.connect("physics.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_name TEXT
)
''')
conn.commit()

# ---------------- UI ---------------- #
st.title("Physics Learning & Simulation System")

menu = ["Home", "Add Topic", "View Topics & Simulate"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- HOME ---------------- #
if choice == "Home":
    st.subheader("Welcome")
    st.write("This system allows teachers to add physics topics and generate simulations.")

# ---------------- ADD TOPIC ---------------- #
elif choice == "Add Topic":
    st.subheader("Add Physics Topic")
    topic = st.text_input("Enter Topic Name")

    if st.button("Add Topic"):
        cursor.execute("INSERT INTO topics (topic_name) VALUES (?)", (topic,))
        conn.commit()
        st.success("Topic Added Successfully!")

# ---------------- VIEW & SIMULATE ---------------- #
elif choice == "View Topics & Simulate":
    st.subheader("Select Topic for Simulation")

    topics = cursor.execute("SELECT topic_name FROM topics").fetchall()
    topic_list = [t[0] for t in topics]

    if topic_list:
        selected_topic = st.selectbox("Choose Topic", topic_list)

        # -------- NEWTON'S FIRST LAW -------- #
        import time

        if selected_topic.lower() == "newton's first law":
           st.write("Simulation: Object moving at constant velocity (Inertia)")

           friction = st.checkbox("Add Friction")

           position = 0
           velocity = 0.1

           plot_area = st.empty()

           for i in range(200):
            fig, ax = plt.subplots()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 1)

            ax.plot(position, 0.5, 'o', markersize=15)

            if friction:
             velocity *= 0.98  # gradual slowing
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

            time = np.linspace(0, 5, 100)
            position = 0.5 * acceleration * time**2

            fig, ax = plt.subplots()
            ax.plot(time, position)
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Position (m)")
            st.pyplot(fig)

        else:
            st.info("No simulation available for this topic yet.")

    else:
        st.warning("No topics added yet.")
