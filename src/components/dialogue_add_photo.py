import time
import streamlit as st

from src.database.db import enroll_student_to_subject
from src.database.config import supabase
from PIL import Image


@st.dialog("Capture or upload photos")
def add_photos_dialogue():

    st.write("Add classroom photos to scan for attendance")

    if "photo_tab" not in st.session_state:
        st.session_state.photo_tab = "camera"

    t1, t2 = st.columns(2)

    with t1:
        type_camera = "primary" if st.session_state.photo_tab == "camera" else "tertiary"
        if st.button("Camera", type=type_camera, width="stretch"):
            st.session_state.photo_tab = "camera"

    with t2:
        type_upload = "primary" if st.session_state.photo_tab == "upload" else "tertiary"
        if st.button("Upload photos", type=type_upload, width="stretch"):
            st.session_state.photo_tab = "upload"

    if st.session_state.photo_tab == "camera":
        cam_photo = st.camera_input("Take Snapshot", key="dialogue_cam")
        if cam_photo:
            st.session_state.attendance_images.append(Image.open(cam_photo))
            st.toast("Photo added from camera!")
            st.rerun()

    if st.session_state.photo_tab == "upload":
        uploaded_files = st.file_uploader("Choose image files Photos", accept_multiple_files=True, type=["jpg", "jpeg", "png"], key="dialogue_upload")

        if uploaded_files:
            for file in uploaded_files:
                st.session_state.attendance_images.append(Image.open(file))

            st.toast(f"Added {len(uploaded_files)} photo(s) from upload!")
            st.rerun()
        
    st.divider()

    if st.button("Done", type="primary", width="stretch"):
        st.rerun()

    

        
        
