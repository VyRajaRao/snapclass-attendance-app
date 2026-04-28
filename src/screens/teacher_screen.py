
import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard

from src.database.db import check_teacher_exists, create_teacher, teacher_login


def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif "teacher_login_type" not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()

def teacher_dashboard():
    teacher_data = st.session_state.teacher_data

    st.header(f"""
        Welcome, {teacher_data['name']}!
        """, text_alignment="center")
    

def login_teacher(username, password):
    if not username or not password:
        return False
    teacher = teacher_login(username, password)
    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False
    



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
        if st.button("Login Now", icon=":material/passkey:", shortcut="control+enter", width="stretch"):
            if login_teacher(teacher_username, teacher_password):
                st.toast("Welcome back!", icon="👋")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.")

    with button_col2:
        if st.button("Register Instead", type="primary",icon=":material/passkey:", width="stretch"):
            st.session_state.teacher_login_type = "register"
            st.rerun()

    footer_dashboard()


def register_teacher(teacher_username, teacher_name, teacher_password, teacher_password_confirm): 
    if not teacher_username or not teacher_name or not teacher_password or not teacher_password_confirm:
        return False, "Please fill in all the fields."

    if check_teacher_exists(teacher_username):
        return False, "Username already taken. Please choose a different one."

    if teacher_password != teacher_password_confirm:
        return False, "Passwords do not match."

    try:
        create_teacher(teacher_username, teacher_password, teacher_name)
        return True, "Registration successful! You can now log in."
    except Exception as e:
        return False, f"An Unexpected Error occurred during registration: {str(e)}"


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
        if st.button("Register Now", icon=":material/passkey:", shortcut="control+enter", width="stretch"):
            success, message = register_teacher(teacher_username, teacher_name, teacher_password, teacher_confirm_password)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)


    with button_col2:
        if st.button("Login Instead", type="primary",icon=":material/passkey:", width="stretch"):
            st.session_state.teacher_login_type = "login"
            st.rerun()

    footer_dashboard()