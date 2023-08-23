import pandas as pd
import streamlit as st
from textblob import TextBlob
import matplotlib.pyplot as plt
import os
import seaborn as sns
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from pathlib import Path 
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import os
import plotly.express as px
import plotly.graph_objects as go
# import streamlit_lottie as stlottie
import pyotp
import otp
import app


# def generate_otp(secret_key):
#     totp = pyotp.TOTP(secret_key)
#     return totp.now()

 

def perform_sentiment_analysis(df):
    # Drop rows with NaN values
    df.dropna(subset=['cleaned_sentiment'], inplace=True)

    # # Apply sentiment analysis
    # df['Sentiment'] = df['cleaned_sentiment'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    
    # return df
    # Apply sentiment analysis
    sentiment_analyzer = SentimentIntensityAnalyzer()
    df['Sentiment'] = df['cleaned_sentiment'].apply(lambda x: sentiment_analyzer.polarity_scores(str(x))['compound'])
    df['Sentiment'] = df['Sentiment'].apply(lambda score: 'Negative' if score < 0 else 'Neutral' if score == 0 else 'Positive')




def main():
               
    st.title("COVID-19 Vaccine Dashboard")
    st.write("Welcome to the COVID-19 Vaccine Dashboard. Stay informed about the latest updates and statistics.")
    
# Load sample data (replace with your own data)
    data = pd.read_csv("Kenya.csv")
    
   
     # Assume you have loaded the CSV file into a DataFrame called 'data'
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        cleaned_data = perform_sentiment_analysis(data)   



    # Create a multi-page app
    pages = {
            "Vaccine Data": display_vaccine_data,
            "Charts": display_charts,
            "Sentiment Analysis": display_sentiment,
            "Pie Chart": display_pie_chart,
            "Bar Chart": display_bar_chart,
            # "Line Graph": display_line_graph,
            
            
            "About": display_about,
            "User Reviews": display_reviews,
            
        }
        
    page = st.sidebar.radio("NAVIGATION", tuple(pages.keys()))
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
        
     

# def display_sentiment(data):
#     st.header("Sentiment Analysis")
#     st.dataframe(data)
def display_sentiment(data):
    st.header("Sentiment Analysis")
    st.write("Below is the sentiment analysis:")
    st.dataframe(data[['cleaned_sentiment', 'Sentiment']])

    # Visualize sentiment pie chart
    st.subheader("Sentiment Distribution")
    fig = visualize_pie_chart(data)
    st.pyplot(fig)

    # Display sentiment polarity counts
    sentiment_counts = data['Sentiment'].value_counts()
    st.subheader("Sentiment Polarity Counts")
    st.write(sentiment_counts)

    # # Line Graph: Sentiment Analysis Over Time
    # st.subheader("Sentiment Analysis Over Time")
    # fig_line = visualize_sentiment_over_time(data)
    # st.plotly_chart(fig_line)

def visualize_sentiment_over_time(data):
    # Group by date and calculate the average sentiment
    sentiment_over_time = data.groupby('Date')['Sentiment'].mean().reset_index()

    # Create line graph using Plotly
    fig = go.Figure(data=go.Scatter(x=sentiment_over_time['Date'], y=sentiment_over_time['Sentiment'], mode='lines'))
    fig.update_layout(title='Sentiment Analysis Over Time', xaxis_title='Date', yaxis_title='Sentiment')
    return fig


def display_pie_chart(data):
    st.header("Pie Chart")
    fig = visualize_pie_chart(data)
    st.pyplot(fig)

def display_bar_chart(data):
    st.header("Bar Chart")
    fig = visualize_bar_chart(data)
    st.pyplot(fig)

def display_line_graph(data):
    st.header("Line Graph")
    fig = visualize_line_graph(data)
    st.pyplot(fig)
    
def visualize_pie_chart(df):
    # Pie chart
    sentiment_counts = df['Sentiment'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    return fig

def visualize_bar_chart(df):
    # Bar chart
    sentiment_avg = df.groupby('Sentiment').size()
    fig, ax = plt.subplots()
    ax.bar(sentiment_avg.index, sentiment_avg.values)
    ax.set_xlabel('Sentiment')
    ax.set_ylabel('Count')
    return fig

def visualize_line_graph(data):
    # Convert the 'Sentiment' column to numeric type
    data['Sentiment'] = pd.to_numeric(data['Sentiment'], errors='coerce')
    
    # Group by date and calculate the average sentiment
    sentiment_over_time = data.groupby('Date')['Sentiment'].mean()
    
    # Reset the index to make 'Date' a column
    sentiment_over_time = sentiment_over_time.reset_index()
    
    # Visualize the line graph
    fig = px.line(sentiment_over_time, x='Date', y='Sentiment', title='Sentiment Analysis Over Time')
    
    return fig
    

def display_about(data):
    st.header("About")
    st.write("This is a COVID-19 Vaccine Dashboard built by Wayhive.")
    st.write("It provides information and visualizations about vaccination data.")
    st.write("COVID-19 is a highly contagious respiratory illness caused by the novel coronavirus SARS-CoV-2. It has caused a global pandemic, affecting millions of people worldwide.")
    st.write("Vaccines play a crucial role in combating the spread of COVID-19. They help protect individuals from severe illness, hospitalization, and death. Vaccination not only safeguards the vaccinated individual but also contributes to community protection through herd immunity.")
    st.write("As new variants of the virus emerge, booster vaccines are being recommended to provide additional protection against these variants and to enhance the immunity gained from the initial vaccine doses.")
    st.write("This COVID-19 Vaccine Dashboard provides insights into vaccination data, sentiment analysis, and visualizations to help monitor the progress of vaccination campaigns and understand public sentiment surrounding the vaccines.")
    
def process_review(review):
    # Add your logic here to process and store the user's review
    # This can include saving the review to a database, writing to a file, or performing any other desired actions
    # For this example, we'll simply print the review
    print("User Review:", review)
    
def display_reviews(data):
    st.header("User Reviews")
    st.write("Leave your review and thoughts:")
    
    # Get user input
    review = st.text_area("Write your review here", height=150)
    
    # Submit button
    if st.button("Submit"):
        # Process and store the review (you can customize this part as per your needs)
        process_review(review)
        st.success("Thank you for your review!")


    

    
# Run the main function
if __name__ == '__main__':
    main()

# import pandas as pd
# import streamlit as st
# from textblob import TextBlob
# import matplotlib.pyplot as plt
# import seaborn as sns
# import nltk
# from nltk.sentiment import SentimentIntensityAnalyzer
# from pathlib import Path 
# import yaml
# from yaml.loader import SafeLoader
# import streamlit_authenticator as stauth
# import os
# import plotly.express as px


# def perform_sentiment_analysis(df):
#     # Drop rows with NaN values
#     df.dropna(subset=['cleaned_sentiment'], inplace=True)

#     # Apply sentiment analysis
#     df['Sentiment'] = df['cleaned_sentiment'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    
#     return df


# def main():
#     st.title("COVID-19 Vaccine Dashboard")
#     st.write("Welcome to the COVID-19 Vaccine Dashboard. Stay informed about the latest updates and statistics.")
    
#     # Load sample data (replace with your own data)
#     data = pd.read_csv("Kenya.csv")
    
#     # Assume you have loaded the CSV file into a DataFrame called 'data'
#     uploaded_file = st.file_uploader("Upload CSV file", type="csv")
#     if uploaded_file is not None:
#         data = pd.read_csv(uploaded_file)
#         cleaned_data = perform_sentiment_analysis(data)

   
#      # Create a multi-page app
#     pages = {
#         "Vaccine Data": display_vaccine_data,
#         "Charts": display_charts,
#         "Sentiment Analysis": display_sentiment,
#         "Pie Chart": display_pie_chart,
#         "Bar Chart": display_bar_chart,
#         "Line Graph": display_line_graph,
#         "About": display_about,
#     }

#     page = st.sidebar.radio("NAVIGATION", tuple(pages.keys()))
#     pages[page](data)

# def display_vaccine_data(data):
#     st.header("Vaccination Data")
#     st.write("Below is the latest vaccination data:")
#     st.dataframe(data)


# def display_charts(data):
#     st.header("Vaccination Charts")

#     # Line Graph: Total Vaccinations Over Time
#     st.subheader("Total Vaccinations Over Time")
#     data['date'] = pd.to_datetime(data['date'])
#     data = data.sort_values(by='date')
#     fig1, ax1 = plt.subplots()
#     for location in data['location'].unique():
#         location_data = data[data['location'] == location]
#         ax1.plot(location_data['date'], location_data['total_vaccinations'], label=location)
#     plt.xlabel("Date")
#     plt.ylabel("Total Vaccinations")
#     plt.xticks(rotation=45)
#     ax1.legend(loc='upper left')
#     st.pyplot(fig1)

#     # Pie Chart: Vaccination Distribution by Vaccine
#     st.subheader("Vaccination Distribution by Vaccine")
#     vaccine_counts = data['vaccine'].value_counts()
#     fig2, ax2 = plt.subplots()
#     ax2.pie(vaccine_counts, labels=vaccine_counts.index, autopct='%1.1f%%', startangle=90)
#     ax2.axis('equal')
#     st.pyplot(fig2)

#     # Trend Graph: People Vaccinated and Fully Vaccinated Over Time
#     st.subheader("People Vaccinated and Fully Vaccinated Over Time")
#     fig3, ax3 = plt.subplots()
#     ax3.plot(data['date'], data['people_vaccinated'], label='People Vaccinated')
#     ax3.plot(data['date'], data['people_fully_vaccinated'], label='People Fully Vaccinated')
#     plt.xlabel("Date")
#     plt.ylabel("Number of People")
#     plt.xticks(rotation=45)
#     ax3.legend(loc='upper left')
#     st.pyplot(fig3)

#     # Bar Plot: Total Boosters by Location
#     st.subheader("Total Boosters by Location")
#     total_boosters = data.groupby("location")["total_boosters"].max().sort_values(ascending=False)
#     fig4, ax4 = plt.subplots()
#     ax4.bar(total_boosters.index, total_boosters.values)
#     plt.xlabel("Location")
#     plt.ylabel("Total Boosters")
#     plt.xticks(rotation=90)
#     st.pyplot(fig4)


# def display_sentiment(data):
#     st.header("Sentiment Analysis")
#     st.write("Below is the sentiment analysis:")
#     st.dataframe(data[['cleaned_sentiment', 'Sentiment']])

#     # Visualize sentiment pie chart
#     st.subheader("Sentiment Distribution")
#     fig = visualize_pie_chart(data)
#     st.pyplot(fig)



# def display_pie_chart(data):
#     st.header("Pie Chart")
#     fig = visualize_pie_chart(data)
#     st.pyplot(fig)


# def display_bar_chart(data):
#     st.header("Bar Chart")
#     fig = visualize_bar_chart(data)
#     st.pyplot(fig)


# def display_line_graph(data):
#     st.header("Line Graph")
#     fig = visualize_line_graph(data)
#     st.plotly_chart(fig)


# def visualize_pie_chart(df):
#     # Pie chart
#     sentiment_counts = df['Sentiment'].value_counts()
#     fig, ax = plt.subplots()
#     ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90)
#     ax.axis('equal')
#     return fig


# def visualize_bar_chart(df):
#     # Bar chart
#     sentiment_avg = df.groupby('Sentiment').size()
#     fig, ax = plt.subplots()
#     ax.bar(sentiment_avg.index, sentiment_avg.values)
#     ax.set_xlabel('Sentiment')
#     ax.set_ylabel('Count')
#     return fig


# def visualize_line_graph(data):
#     # Convert the 'Sentiment' column to numeric type
#     data['Sentiment'] = pd.to_numeric(data['Sentiment'], errors='coerce')

#     # Group by date and calculate the average sentiment
#     sentiment_over_time = data.groupby('date')['Sentiment'].mean().reset_index()

#     # Visualize the line graph
#     fig = px.line(sentiment_over_time, x='date', y='Sentiment', title='Sentiment Analysis Over Time')
#     return fig


# def display_about(data):
#     st.header("About")
#     st.write("This is a COVID-19 Vaccine Dashboard built by Wayhive.")
#     st.write("It provides information and visualizations about vaccination data.")
    



# # Run the main function
# if __name__ == '__main__':
#     main()


