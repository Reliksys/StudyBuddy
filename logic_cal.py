from datetime import timedelta, datetime
import streamlit as st
import pandas as pd
import plotly.express as px
import db

def run():
    st.header("Планировщик")
    
    with st.expander("Добавить новую задачу", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Название задачи / Предмет")
            deadline = st.date_input("Дедлайн")
        with col2:
            difficulty = st.slider("Сложность (1-5)", 1, 5, 3)
            priority = st.selectbox("Важность", ["Низкая", "Средняя", "Высокая"])
        days_needed = difficulty * 1.5
        if "Высокая" in priority:
            days_needed += 3
        elif "Средняя" in priority:
            days_needed += 1
            
        start_date = deadline - timedelta(days=int(days_needed))

        st.info(f"Учитывая сложность {difficulty} и важность '{priority}', начать нужно: **{start_date}**")

        if st.button("Добавить в план", use_container_width=True):
            if title:
                db.create_task(title, str(deadline), difficulty, priority, str(start_date))
                st.success("Сохранено!")
                st.rerun()
            else:
                st.error("Введите название!")

    st.divider()
    st.subheader("Временная шкала")
    
    tasks = db.get_all_tasks()
    
    if tasks:
        df = pd.DataFrame(tasks, columns=['ID', 'Задача', 'Дедлайн', 'Сложность', 'Приоритет', 'Старт', 'Статус'])
        df['Старт'] = pd.to_datetime(df['Старт'])
        df['Дедлайн'] = pd.to_datetime(df['Дедлайн'])

        fig = px.timeline(
            df, 
            x_start="Старт", 
            x_end="Дедлайн", 
            y="Задача", 
            color="Приоритет",
            color_discrete_map={"Высокая": "red", "Средняя": "orange", "Низкая": "green"}
        )
        fig.update_yaxes(autorange="reversed") 
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("Детальный список")
        def highlight_urgent(row):
            deadline_date = row['Дедлайн']
            days_left = (deadline_date - datetime.now()).days
            
            if days_left < 0:
                return ['background-color: #ffcccc'] * len(row)
            elif days_left < 3:
                return ['background-color: #fff4cc'] * len(row)
            else:
                return [''] * len(row)

        display_df = df.drop(columns=['ID'])
        st.dataframe(
            display_df.style.apply(highlight_urgent, axis=1),
            use_container_width=True
        )
    
    else:
        st.info("Задач нет. Добавьте первую сверху!")
    st.divider()
    st.subheader("Выполненные задачи")
    with st.expander("Пометить задачу выполненной", expanded=True):
        tasks = db.get_all_tasks()
        td = []
        for task in tasks:
            td.append(f"{task[0]} {task[1]}")
        id = st.selectbox("Пометить выполненной", td).split()[0]
        if st.button("Выполнено!"):
            db.done_task(id)
            st.rerun()
         
        
