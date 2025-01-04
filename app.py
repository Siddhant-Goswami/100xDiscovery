# frontend/app.py
import streamlit as st

st.set_page_config(
    page_title="100xEngineers Discovery Platform",
    layout="centered"
)

st.title("100xEngineers Discovery Platform")

st.markdown("""
Welcome to the 100xEngineers Discovery Platform!
Use the pages on the left to navigate through the app:
- **🔑 Login** 
- **✏️ Edit Profile**
- **🔍 Search**
- **👤 Profile View**
""")
