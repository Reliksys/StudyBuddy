from datetime import timedelta
import streamlit as st
import pandas as pd
import db

def run():
    title = st.text_input("Название задачи")
    deadline = st.date_input("Дата, к которой задача должна быть выполнена")

    difficulty = st.slider("Сложность задачи", min_value=1, max_value=5, value=1, step=1)
    start_date = deadline - timedelta(days=difficulty*2)
    if st.button("Добавить"):
        if title:
            db.create_task(title, str(deadline), difficulty, start_date)
            st.success("Задача добавлена")
            st.rerun()
        else:
            st.warning("Нет названия задачи. Введите.")
    tasks = db.get_all_tasks()
    if not tasks:
        st.info("Пока задач нет. Отдыхай!")
    else:
        df = pd.DataFrame(tasks, columns=['ID', 'Задача', 'Дедлайн', 'Сложность', 'Начать'])

        st.dataframe(
            df.drop(columns=['ID']), 
            use_container_width=True, 
            hide_index=True
        )