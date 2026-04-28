import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard


def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    if "teacher_login_type" not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')

    with c1:
        header_dashboard()

    with c2:
        if st.button("Go back to Home", type="secondary", key="login_back_btn", shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Login using password", text_alignment="center")
    st.space()
    st.space()

    teacher_username = st.text_input("Enter username", placeholder="raja rao", key="login_username")
    
    teacher_password = st.text_input("Enter password", placeholder="Enter password", type="password", key="login_password")

    st.divider() 

    button_col1, button_col2 = st.columns(2) 

    with button_col1:
        st.button("Login Now", icon=":material/passkey:", shortcut="control+enter", width="stretch")

    with button_col2:
        if st.button("Register Instead", type="primary",icon=":material/passkey:", width="stretch"):
            st.session_state.teacher_login_type = "register"
            st.rerun()

    footer_dashboard()

def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')

    with c1:
        header_dashboard()

    with c2:
        if st.button("Go back to Home", type="secondary", key="register_back_btn", shortcut="control+backspace"):
            st.session_state['login_state'] = "login"
            st.rerun()



    st.header("Register your teacher profile", text_alignment="center")

    st.space()


    teacher_username = st.text_input("Enter username", placeholder="raja rao", key="register_username")

    teacher_name = st.text_input("Enter name", placeholder="VY Raja Rao", key="register_name")

    teacher_password = st.text_input("Enter password", placeholder="Enter password", type="password", key="register_password")
    
    teacher_confirm_password = st.text_input("Enter password", placeholder="Re-enter password", type="password", key="register_confirm_password")

    st.divider() 

    button_col1, button_col2 = st.columns(2) 

    with button_col1:
        st.button("Register Now", icon=":material/passkey:", shortcut="control+enter", width="stretch")

    with button_col2:
        if st.button("Login Instead", type="primary",icon=":material/passkey:", width="stretch"):
            st.session_state.teacher_login_type = "login"
            st.rerun()

    footer_dashboard()