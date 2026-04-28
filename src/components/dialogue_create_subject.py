import streamlit as st
from src.database.db import create_subject


@st.dialog("Create New Subject")
def create_subject_dialogue(teacher_id):

    st.write("Enter the details of new subject")
    sub_id = st.text_input("Subject Code", placeholder="CS101")
    sub_name = st.text_input("Subject_name", placeholder="Introduction toComputer Science")
    sub_section = st.text_input("Section", placeholder="A")

    if st.button("Create Subject Now", type="primary", width="stretch"):
        if  sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id, sub_name, sub_section)
                st.toast("Subject created successfully!", icon="✅")
                st.rerun()
            except Exception as e:
                st.error(f"Error {str(e)}")

        else:
            st.warning("Please fill all the fields to create a subject.")

        
        

def share_subject_dialogue(sub_name, sub_code):
    st.dialog(f"Share {sub_name}").markdown(
        f"""
        <div style="display:flex; flex-direction:column; gap:12px; justify-items:center; align-items:center;">
            <p style="font-size:1.2rem; margin:0;">Share this code with your students to let them join the subject</p>
            <div style="background: #E0E3FF; color:#5865F2; padding:10px 16px; border-radius:5px; font-size:1.5rem; font-weight:bold;"> {sub_code} </div>
        </div>
        """,
        unsafe_allow_html=True
    )