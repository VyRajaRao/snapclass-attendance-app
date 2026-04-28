import streamlit as st


def footer_home():

    st.markdown(f"""
        <div style="display:flex; margin-top:2rem; gap:6px; justify-content:center; ">
            <p style="color:white; font-weight:bold">Created with ❤️ by Raja </p>
        </div>
    """, unsafe_allow_html=True)

def footer_dashboard():
    st.markdown(f"""
        <div style="display:flex; margin-top:2rem; gap:6px; justify-content:center; ">
            <p style="color:black; font-weight:bold">Created with ❤️ by Raja </p>
        </div>
    """, unsafe_allow_html=True)