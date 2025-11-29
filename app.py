import streamlit as st
import logic_cal
import logic_cards
import db
st.set_page_config(page_title="StudyBuddy")
db.init_db()

def main():
    st.title("StudyBuddy")
    menu = ["Календарь и Дедлайны", "Карточки"]
    choice = st.sidebar.selectbox("Меню", menu)

    if choice == "Календарь и Дедлайны":
        logic_cal.run()
        
    elif choice == "Карточки":
        logic_cards.show_flashcards_page()

if __name__ == '__main__':
    main()