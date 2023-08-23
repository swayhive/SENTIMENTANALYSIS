import streamlit as st

def login_form(username):
    st.subheader("Log In")
    entered_username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log In"):
        if entered_username == username:
            # Perform login logic here
            st.success("You have successfully logged in!")
        else:
            st.error("Invalid username or password!")
