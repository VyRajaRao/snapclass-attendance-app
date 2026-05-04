import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_background_home, style_base_layout


def home_screen():

    header_home()
    style_base_layout()
    style_background_home()
    
    col1, col2 = st.columns(2, gap="large" )

    with col1:
        st.header("I'm Student")
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=120)
        if st.button("Student Portal", type="primary", icon=':material/arrow_outward:', icon_position='right'):
            st.session_state["login_type"] = "student"
            st.rerun()
        
        
    with col2:
        st.header("I'm Teacher")
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=145)
        if st.button("Teacher Portal", type="primary", icon=':material/arrow_outward:', icon_position='right'):
            st.session_state["login_type"] = "teacher"
            st.rerun()
    footer_home()
    
    st.info(
        "**Note:** If text colors appear inverted or hard to read, please enable **Light Mode** in Device settings. \
        This is due to streamlit css conflicts with dark mode. We recommend using light mode for the best experience. \
        Thank you for your understanding!"
    )
