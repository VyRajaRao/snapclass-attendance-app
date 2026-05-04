import time
import streamlit as st

from src.database.db import enroll_student_to_subject
from src.database.config import supabase
from src.database.db import create_attendance
from PIL import Image

def show_attendance_results(df, logs):
        st.write("Please Review attendance before confirming...")
        st.dataframe(df, hide_index=True, width="stretch")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Discard", width="stretch"):
                st.session_state.attendance_images = []
                st.session_state.voice_attendance_results = None
                st.rerun()
        
        with col2:
            if st.button("Confirm and Save", type="primary", width="stretch"):
                try:
                    create_attendance(logs)
                    st.toast("Attendance taken successfully!")
                    st.session_state.attendance_images = []
                    st.session_state.voice_attendance_results = None
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving attendance: {str(e)}, Sync Failed")
                    st.rerun()

@st.dialog("Attendance Results")
def attendance_result_dialogue(df, logs):
     show_attendance_results(df, logs)

    
            


    

        
        
