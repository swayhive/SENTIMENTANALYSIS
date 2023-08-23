import streamlit as st
import pyotp

def generate_otp(secret_key):
    totp = pyotp.TOTP(secret_key)
    return totp.now()

def main():
    st.title("OTP Login")

    # Generate a secret key for OTP
    secret_key = pyotp.random_base32()

    # Display the secret key to the user
    st.write("Secret Key:", secret_key)

    # User login form
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Generate OTP button
    if st.button("Generate OTP"):
        otp = generate_otp(secret_key)
        st.success("Generated OTP: " + otp)

        # OTP verification
        entered_otp = st.text_input("Enter OTP")
        if entered_otp == otp:
            st.success("OTP verification successful. You are now logged in.")
        else:
            st.error("Invalid OTP. Please try again.")

if __name__ == '__main__':
    main()
