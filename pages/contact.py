import streamlit as st

st.set_page_config(page_title='PlacementGuru', layout='wide')
with st.form("contact_form"):
    st.text_input("Name",max_chars=100)
    st.text_input("Email")
    st.number_input("Phone Number")
    st.text_area("Message")
    st.form_submit_button("Submit")

