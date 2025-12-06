from datetime import timedelta, datetime
import streamlit as st
import pandas as pd
import plotly.express as px
import db
import random
from typing import List, Dict

def run():
    st.header("📚 Карточки для повторения (Quizlet-style)")
    
    # Инициализация состояния сессии
    if 'current_card_index' not in st.session_state:
        st.session_state.current_card_index = 0
    if 'cards' not in st.session_state:
        st.session_state.cards = []
    if 'show_answer' not in st.session_state:
        st.session_state.show_answer = False
    if 'study_mode' not in st.session_state:
        st.session_state.study_mode = 'all'  # 'all', 'difficult', 'random'
    if 'difficult_cards' not in st.session_state:
        st.session_state.difficult_cards = []
    if 'card_stats' not in st.session_state:
        st.session_state.card_stats = {}
    
    # Боковая панель для управления карточками
    with st.sidebar:
        st.header("Управление карточками")
        
        # Добавление новой карточки
        with st.expander("➕ Добавить новую карточку", expanded=False):
            front = st.text_area("Вопрос / Передняя сторона", 
                                placeholder="Что такое ...?")
            back = st.text_area("Ответ / Задняя сторона", 
                               placeholder="Это ...")
            category = st.selectbox("Категория", 
                                   ["Программирование", "Математика", "История", 
                                    "Иностранный язык", "Наука", "Другое"])
            difficulty = st.slider("Сложность", 1, 5, 3)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Сохранить карточку", use_container_width=True):
                    if front and back:
                        db.create_card(front, back, category, difficulty)
                        st.success("Карточка сохранена!")
                        st.session_state.cards = db.get_all_cards()
                        st.rerun()
                    else:
                        st.error("Заполните обе стороны карточки!")
            
            with col2:
                if st.button("Предпросмотр", use_container_width=True):
                    if front:
                        st.info(f"Вопрос: {front[:50]}...")
        
        st.divider()
        
        # Настройки изучения
        st.subheader("⚙️ Настройки изучения")
        st.session_state.study_mode = st.radio(
            "Режим изучения",
            ["Все карточки", "Только сложные", "Случайный порядок", "По категориям"],
            index=0
        )
        
        # Выбор категории если выбран режим по категориям
        if st.session_state.study_mode == "По категориям":
            categories = db.get_categories()
            if categories:
                selected_category = st.selectbox("Выберите категорию", categories)
                st.session_state.selected_category = selected_category
        
        # Сброс прогресса
        if st.button("🔄 Сбросить прогресс", use_container_width=True):
            st.session_state.card_stats = {}
            st.session_state.difficult_cards = []
            st.success("Прогресс сброшен!")
    
    # Загрузка карточек из базы данных
    def load_cards():
        all_cards = db.get_all_cards()
        
        if st.session_state.study_mode == "Все карточки":
            return all_cards
        elif st.session_state.study_mode == "Только сложные":
            # Фильтруем карточки, отмеченные как сложные
            difficult_ids = [card[0] for card in all_cards if card[0] in st.session_state.difficult_cards]
            if difficult_ids:
                return db.get_cards_by_ids(difficult_ids)
            else:
                return all_cards[:5]  # Если нет сложных, показываем первые 5
        elif st.session_state.study_mode == "Случайный порядок":
            shuffled = all_cards.copy()
            random.shuffle(shuffled)
            return shuffled
        elif st.session_state.study_mode == "По категориям":
            if 'selected_category' in st.session_state:
                return db.get_cards_by_category(st.session_state.selected_category)
            else:
                return all_cards
    
    # Основной интерфейс карточек
    st.session_state.cards = load_cards()
    
    if st.session_state.cards:
        # Показываем прогресс
        total_cards = len(st.session_state.cards)
        current_idx = st.session_state.current_card_index
        
        # Прогресс бар
        progress = (current_idx + 1) / total_cards if total_cards > 0 else 0
        st.progress(progress)
        
        # Статистика
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Карточка", f"{current_idx + 1} / {total_cards}")
        with col2:
            difficult_count = len(st.session_state.difficult_cards)
            st.metric("Сложные", difficult_count)
        with col3:
            mastered = sum(1 for stat in st.session_state.card_stats.values() 
                          if stat.get('correct', 0) >= 3)
            st.metric("Выучено", mastered)
        
        st.divider()
        
        # Отображение текущей карточки
        current_card = st.session_state.cards[current_idx]
        card_id, front, back, category, difficulty, created_at = current_card
        
        # Стилизованная карточка
        card_container = st.container()
        
        with card_container:
            # Заголовок карточки
            col_header = st.columns([4, 1])
            with col_header[0]:
                st.subheader(f"📌 Карточка #{card_id}")
            with col_header[1]:
                difficulty_color = ["🟢", "🟡", "🟠", "🔴", "🟣"][difficulty - 1]
                st.markdown(f"{difficulty_color} Сложность: {difficulty}/5")
            
            # Тело карточки
            st.markdown("---")
            
            # Передняя сторона (вопрос)
            with st.container():
                st.markdown("### ❓ Вопрос:")
                card_front = st.container(border=True)
                with card_front:
                    st.markdown(f"<h3 style='text-align: center; padding: 20px;'>{front}</h3>", 
                               unsafe_allow_html=True)
            
            # Кнопка показа ответа
            if not st.session_state.show_answer:
                if st.button("👁️ Показать ответ", use_container_width=True, type="primary"):
                    st.session_state.show_answer = True
                    st.rerun()
            else:
                st.markdown("---")
                
                # Задняя сторона (ответ)
                with st.container():
                    st.markdown("### ✅ Ответ:")
                    card_back = st.container(border=True)
                    with card_back:
                        st.markdown(f"<h3 style='text-align: center; padding: 20px; color: #2e7d32;'>{back}</h3>", 
                                   unsafe_allow_html=True)
                
                # Кнопки оценки
                st.markdown("---")
                st.markdown("### 📊 Насколько хорошо вы знали ответ?")
                
                col_feedback = st.columns(4)
                
                with col_feedback[0]:
                    if st.button("🤔 Не знал", use_container_width=True, 
                                help="Совсем не знал ответ"):
                        mark_difficult(card_id, True)
                        update_card_stats(card_id, False)
                        next_card()
                
                with col_feedback[1]:
                    if st.button("📖 Почти", use_container_width=True, 
                                help="Почти угадал, но не точно"):
                        mark_difficult(card_id, False)
                        update_card_stats(card_id, True)
                        next_card()
                
                with col_feedback[2]:
                    if st.button("✅ Знаю", use_container_width=True, 
                                help="Знаю, но нужно повторить"):
                        mark_difficult(card_id, False)
                        update_card_stats(card_id, True)
                        next_card()
                
                with col_feedback[3]:
                    if st.button("🎯 Отлично", use_container_width=True, 
                                help="Отлично знаю материал"):
                        mark_difficult(card_id, False)
                        update_card_stats(card_id, True, perfect=True)
                        next_card()
                
                # Дополнительные действия
                col_actions = st.columns(3)
                with col_actions[0]:
                    if st.button("🔄 Повторить эту", use_container_width=True):
                        st.session_state.show_answer = False
                        st.rerun()
                
                with col_actions[1]:
                    if st.button("⏭️ Пропустить", use_container_width=True):
                        next_card()
                
                with col_actions[2]:
                    if st.button("✏️ Редактировать", use_container_width=True):
                        edit_card(card_id)
        
        # Навигация по карточкам
        st.divider()
        st.markdown("### 🔄 Навигация")
        
        nav_cols = st.columns([1, 2, 1])
        
        with nav_cols[0]:
            if st.button("⏮️ Предыдущая", use_container_width=True, 
                        disabled=current_idx == 0):
                st.session_state.current_card_index -= 1
                st.session_state.show_answer = False
                st.rerun()
        
        with nav_cols[1]:
            # Быстрая навигация
            selected_idx = st.selectbox(
                "Перейти к карточке",
                range(1, total_cards + 1),
                index=current_idx,
                label_visibility="collapsed"
            )
            if selected_idx - 1 != current_idx:
                st.session_state.current_card_index = selected_idx - 1
                st.session_state.show_answer = False
                st.rerun()
        
        with nav_cols[2]:
            if st.button("⏭️ Следующая", use_container_width=True, 
                        disabled=current_idx == total_cards - 1):
                next_card()
        
        # Статистика и аналитика
        st.divider()
        with st.expander("📈 Статистика изучения", expanded=False):
            if st.session_state.card_stats:
                stats_df = pd.DataFrame.from_dict(
                    st.session_state.card_stats, 
                    orient='index'
                ).reset_index()
                stats_df.columns = ['Card ID', 'Correct', 'Total', 'Last Review']
                
                # Визуализация прогресса
                fig = px.bar(
                    stats_df,
                    x='Card ID',
                    y='Correct',
                    title='Правильные ответы по карточкам',
                    color='Correct',
                    color_continuous_scale='Viridis'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Нет статистики для отображения")
        
        # Список всех карточек
        with st.expander("📋 Все карточки", expanded=False):
            all_cards_df = pd.DataFrame(
                st.session_state.cards,
                columns=['ID', 'Вопрос', 'Ответ', 'Категория', 'Сложность', 'Дата создания']
            )
            
            # Добавляем статус
            all_cards_df['Статус'] = all_cards_df['ID'].apply(
                lambda x: '🎯 Выучена' if st.session_state.card_stats.get(x, {}).get('correct', 0) >= 3 
                else '⚠️ Сложная' if x in st.session_state.difficult_cards 
                else '📖 В процессе'
            )
            
            st.dataframe(
                all_cards_df.drop(columns=['Ответ']),
                use_container_width=True,
                hide_index=True
            )
    
    else:
        # Нет карточек
        st.warning("📭 Нет карточек для изучения!")
        st.info("Добавьте карточки используя панель слева")
        
        # Быстрые примеры
        with st.expander("🎯 Примеры карточек для начала", expanded=True):
            examples = [
                ("Что такое Python?", "Язык программирования высокого уровня"),
                ("Столица Франции?", "Париж"),
                ("Формула воды?", "H₂O")
            ]
            
            for i, (question, answer) in enumerate(examples, 1):
                st.markdown(f"**{i}. {question}**")
                with st.expander("Показать ответ"):
                    st.success(answer)

def next_card():
    """Перейти к следующей карточке"""
    st.session_state.show_answer = False
    if st.session_state.current_card_index < len(st.session_state.cards) - 1:
        st.session_state.current_card_index += 1
    else:
        st.session_state.current_card_index = 0  # Зацикливание
    st.rerun()

def mark_difficult(card_id: int, is_difficult: bool):
    """Пометить карточку как сложную или убрать пометку"""
    if is_difficult and card_id not in st.session_state.difficult_cards:
        st.session_state.difficult_cards.append(card_id)
    elif not is_difficult and card_id in st.session_state.difficult_cards:
        st.session_state.difficult_cards.remove(card_id)

def update_card_stats(card_id: int, correct: bool, perfect: bool = False):
    """Обновить статистику по карточке"""
    if card_id not in st.session_state.card_stats:
        st.session_state.card_stats[card_id] = {
            'correct': 0,
            'total': 0,
            'last_review': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    
    stats = st.session_state.card_stats[card_id]
    stats['total'] += 1
    
    if correct:
        if perfect:
            stats['correct'] += 2  # Бонус за отличный ответ
        else:
            stats['correct'] += 1
    
    stats['last_review'] = datetime.now().strftime("%Y-%m-%d %H:%M")

def edit_card(card_id: int):
    """Редактировать карточку"""
    # Здесь можно добавить модальное окно или форму редактирования
    st.info(f"Редактирование карточки {card_id}")
    # В реальном приложении здесь будет форма редактирования
    # и вызов db.update_card(card_id, new_front, new_back, ...)
