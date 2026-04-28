
import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard

from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_all_students, get_teacher_subjects
from src.components.dialogue_create_subject import create_subject_dialogue, share_subject_dialogue
from src.components.subject_card import subject_card

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
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')

    with c1:
        header_dashboard()

    with c2:
        st.header(f"""Welcome, {teacher_data['name']}""")
        if st.button("Go back to Home", type="secondary", key="login_back_btn", shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state['teacher_data']
            st.rerun()

    st.space()

    current_teacher_tab = st.session_state.get("current_teacher_tab", "take_attendance")

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == "take_attendance" else "tertiary"
        if st.button("Take Attendance", type=type1, width="stretch", icon=":material/ar_on_you:"):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == "manage_subjects" else "tertiary"
        if st.button("Manage Subjects", type=type2, width="stretch", icon=":material/book_ribbon:"):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()


    with tab3:  
        type3 = "primary" if st.session_state.current_teacher_tab == "attendance_records" else "tertiary" 
        if st.button("Attendance Records", type=type3, width="stretch", icon=":material/cards_stack:"):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()
    

def teacher_tab_take_attendance():
    st.header("Take AI Attendance")

def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data["teacher_id"]
    col1, col2 = st.columns(2)
    with col1:
        st.header("Manage Subjects", width="stretch")

    with col2:
        if st.button("Create new Subject", width="stretch"):
            create_subject_dialogue(teacher_id)

    # LIST ALL SUBJECTS OF THE TEACHER

    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("🧑‍🎓", "Students", sub["total_students"]),
                ("📅", "Classes Held", sub["total_classes"]),  
            ]
        def share_btn():
            if st.button(f"Share Code: {sub["name"]}", key=f"share_{sub["subject_code"]}", icon=":material/share:"):
                share_subject_dialogue(sub["name"], sub["subject_code"])
        st.space()

        subject_card(
            name = sub["name"],
            code = sub["subject_code"],
            section = sub["section"],
            stats = stats,
            footer_callback = share_btn
        )

    else:
        st.info("No subjects Found. Please create a subject to start taking attendance.")


def teacher_tab_attendance_records():
    st.header("Attendance Records")




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
            st.session_state['login_type'] = None
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