from datetime import datetime
import pandas as pd

import streamlit as st

from src.pipelines.voice_pipeline import process_bulk_audio

from src.database.config import supabase

from src.components.dialogue_attendance_results import show_attendance_results

@st.dialog("Voice Attendance")

def voice_attendance_dialogue(selected_subject_id):
    st.write("Record audio of students saying \"I'm present\" or similar phrases to mark attendance. Then AI will recognize the students.")
    
    audio_data = None

    audio_data = st.audio_input("Record classroom audio for attendance")

    if st.button("Analyze Audio", width="stretch", type="primary", icon=":material/mic:"):
        with st.spinner("Analyzing and Processing audio for attendance..."):
            enrolled_res = supabase.table("subject_students").select("*, students(*)").eq("subject_id", selected_subject_id).execute()

            enrolled_students = enrolled_res.data

            if not enrolled_students:
                st.warning("No students are enrolled in this subject yet. Please enroll students first to use voice attendance.")
                return
            
            candidate_dict = {
                s["students"]["student_id"] : s["students"]["voice_embedding"]
                for s in enrolled_students if s["students"].get("voice_embedding")
            }
    
            if not candidate_dict:
                st.error("No enrolled students have voice embeddings yet. Please ask students to record their voice samples first.")
                return
            
            audio_bytes = audio_data.read()

            detected_scores = process_bulk_audio(audio_bytes, candidate_dict)

            results, attendance_to_log = [], []

            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            for node in enrolled_students:
                student = node["students"]
                scores = detected_scores.get(student["student_id"], 0.0)
                is_present = bool(scores) > 0

                results.append({
                    "Name": student["name"],
                    "ID" : student["student_id"],
                    "Status": "✅Present" if is_present else "❌Absent",
                    "Score": scores if is_present else "N/A"
                })

                attendance_to_log.append({
                    "student_id": student["student_id"],
                    "subject_id": selected_subject_id,
                    "timestamp": current_timestamp,
                    "is_present": bool(is_present)
                })

            st.session_state.voice_attendance_results = (pd.DataFrame(results), attendance_to_log)


    if st.session_state.get("voice_attendance_results"):
        st.divider()

        df_results, logs = st.session_state.voice_attendance_results

        show_attendance_results(df_results, logs)


        
        
