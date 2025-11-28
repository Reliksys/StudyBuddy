import streamlit as st
import calendar
import cards
import db

db.init_db()

page = st.sidebar.radio("Меню", ["Дедлайны", "Карточки"])

st.title("Есть ли коннект с базой данных")

name = st.text_input("Название задачи")
if st.button("Сохранить задачу"):
    db.add_task(name, "2025-12-10", 5, "2026-12-01")
    st.success("Сохранено!")

st.write("---")
st.write("Список задач в базе:")
tasks = db.get_all_tasks()
st.write(tasks)