import streamlit as st
import logic_cal
import logic_cards
import db
st.set_page_config(page_title="StudyBuddy")
db.init_db()

def main():
    st.title("StudyBuddy")
    menu = ["Дедлайны", "Карточки"]
    choice = st.sidebar.selectbox("Меню", menu)

    if choice == "Дедлайны":
        logic_cal.run()
        
    elif choice == "Карточки":
        logic_cards.run()

if __name__ == '__main__':
    main()