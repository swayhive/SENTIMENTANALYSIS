import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from pathlib import Path 
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import os
from signup_form import signup_form
from login_form import login_form


# Download required NLTK resources
nltk.download('vader_lexicon')


# Load sample data (replace with your own data)
data = pd.read_csv("Kenya.csv")

def main():
    
    signup_username = signup_form()

    if signup_username is not None:
        login_form(signup_username)
    
    
    st.title("COVID-19 Vaccine Dashboard")
    st.write("Welcome to the COVID-19 Vaccine Dashboard. Stay informed about the latest updates and statistics.")

    # Create a dictionary of pages
    pages = {
        "Vaccine Data": display_vaccine_data,
        "Charts": display_charts,
        "About": display_about,
    }
    

    # Create a sidebar with page selection
    page = st.sidebar.radio("NAVIGATION", tuple(pages.keys()))

    # Display the selected page
    pages[page](data)
    

def display_vaccine_data(data):
    st.header("Vaccination Data")
    st.write("Below is the latest vaccination data:")
    st.dataframe(data)

def display_charts(data):
    st.header("Vaccination Charts")

    # Line Graph: Total Vaccinations Over Time
    st.subheader("Total Vaccinations Over Time")
    data['date'] = pd.to_datetime(data['date'])
    data = data.sort_values(by='date')
    fig1, ax1 = plt.subplots()
    for location in data['location'].unique():
        location_data = data[data['location'] == location]
        ax1.plot(location_data['date'], location_data['total_vaccinations'], label=location)
    plt.xlabel("Date")
    plt.ylabel("Total Vaccinations")
    plt.xticks(rotation=45)
    ax1.legend(loc='upper left')
    st.pyplot(fig1)

    # Pie Chart: Vaccination Distribution by Vaccine
    st.subheader("Vaccination Distribution by Vaccine")
    vaccine_counts = data['vaccine'].value_counts()
    fig2, ax2 = plt.subplots()
    ax2.pie(vaccine_counts, labels=vaccine_counts.index, autopct='%1.1f%%', startangle=90)
    ax2.axis('equal')
    st.pyplot(fig2)

    # Trend Graph: People Vaccinated and Fully Vaccinated Over Time
    st.subheader("People Vaccinated and Fully Vaccinated Over Time")
    fig3, ax3 = plt.subplots()
    ax3.plot(data['date'], data['people_vaccinated'], label='People Vaccinated')
    ax3.plot(data['date'], data['people_fully_vaccinated'], label='People Fully Vaccinated')
    plt.xlabel("Date")
    plt.ylabel("Number of People")
    plt.xticks(rotation=45)
    ax3.legend(loc='upper left')
    st.pyplot(fig3)

    # Bar Plot: Total Boosters by Location
    st.subheader("Total Boosters by Location")
    total_boosters = data.groupby("location")["total_boosters"].max().sort_values(ascending=False)
    fig4, ax4 = plt.subplots()
    ax4.bar(total_boosters.index, total_boosters.values)
    plt.xlabel("Location")
    plt.ylabel("Total Boosters")
    plt.xticks(rotation=90)
    st.pyplot(fig4)

def display_about(data):
    st.header("About")
    st.write("This is a COVID-19 Vaccine Dashboard built by Wayhive.")
    st.write("It provides information and visualizations about vaccination data.")
        
        
import sentiment 


if __name__ == "__main__":
    main()
