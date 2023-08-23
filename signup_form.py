import streamlit as st

def signup_form():
    st.subheader("Sign Up")
    username = st.text_input("Username", key="signup_username")
    password = st.text_input("Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")

    if st.button("Sign Up"):
        if password == confirm_password:
            # Perform sign-up logic here
            st.success("You have successfully signed up!")
            return username  # Return the username for login
        else:
            st.error("Passwords do not match!")

    return None
