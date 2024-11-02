# import lib
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import io

# Define functions for each page
def home_page():
    # Main Title and Intro
    st.title("📊 Welcome to Data Insights Pro")
    st.write("*A Comprehensive Data Analytics Platform for In-Depth Analysis*")
    
    # Mission Statement
    st.write("""
    Our mission is to empower you with deep insights into your data, enabling you to make data-driven decisions
    with confidence. Whether you're exploring raw data or creating advanced visualizations, *Data Insights Pro* 
    provides the tools you need for effective data analysis.
    """)
    
    # App Overview
    st.subheader("Key Features:")
    st.write("""
    - *Data Upload & Cleaning*: Easily upload your data in CSV or Excel format and get a quick overview of its structure.
    - *Analytics Overview*: Generate automatic visualizations like scatter plots, histograms, and summary statistics.
    - *Deep Insights*: Dive into your data with detailed metrics, custom visualizations, and advanced analytics.
    """)

    # Visual Break / Divider
    st.markdown("---")

    # Call to Action
    st.subheader("Getting Started")
    st.write("1. Navigate to the *Analytics Overview* page to upload your data and start exploring.")
    st.write("2. Use the *Deep Insights* page to perform detailed analysis and uncover patterns.")
    st.write("3. Return to the Home page anytime to revisit key functionalities and guidance.")

    # Add Footer or Contact Information
    st.markdown("---")
    st.write("*Need assistance?* Contact us at [support@datainsightspro.com](mailto:support@datainsightspro.com) for any questions or feedback.")
def analytics_page():
    st.title("Analytics Overview")
    st.write("Upload your data to generate scatter plots, histograms, and pairplots.")

    # Data upload
    data = st.file_uploader("Upload your data file", type=["csv", "xlsx"])

    if data is not None:
        # Load data
        if data.name.endswith('.csv'):
            df = pd.read_csv(data)
        else:
            df = pd.read_excel(data)
        
        st.write("Data Preview:")
        st.write(df.head())

        # Remove ₹ symbol and convert potential numeric columns to numeric type
        for column in df.columns:
            if df[column].dtype == 'object':  # Only apply to text columns
                df[column] = df[column].str.replace('₹', '', regex=True)  # Remove ₹ symbol
                df[column] = pd.to_numeric(df[column], errors='coerce')  # Convert to numeric

        # Convert "whole number" floats to integers, filling NaN values with 0 for conversion
        for column in df.select_dtypes(include=["float64"]).columns:
            if (df[column].fillna(0) == df[column].fillna(0).astype(int)).all():  # Check for whole numbers
                df[column] = df[column].fillna(0).astype(int)  # Fill NaN with 0 and convert to int

        # First try to use integer columns, then fallback to float columns if no integers are found
        numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns

        if len(numeric_columns) > 0:
            # Scatter plot using Plotly
            st.subheader("Scatter Plots")
            for i in range(len(numeric_columns)):
                for j in range(i + 1, len(numeric_columns)):
                    fig = px.scatter(df, x=numeric_columns[i], y=numeric_columns[j],
                                     title=f"Scatter Plot: {numeric_columns[i]} vs {numeric_columns[j]}")
                    st.plotly_chart(fig)

            # Histogram using Seaborn
            st.subheader("Histograms")
            for column in numeric_columns:
                plt.figure(figsize=(10, 4))
                sns.histplot(df[column], kde=True)
                plt.title(f"Histogram of {column}")
                st.pyplot(plt)
                plt.clf()

            # Pairplot using Seaborn
            st.subheader("Pairplot")
            sns.pairplot(df[numeric_columns])
            st.pyplot(plt)
        else:
            st.write("No numeric columns found in the dataset. Please upload a file with numeric data for analysis.")
    else:
        st.write("Please upload a CSV or Excel file to generate plots.")
def insights_page():
    st.title("Deep Insights")
    st.write("Uncover deeper insights with summary statistics and data structure information.")
    
    # Data upload
    data = st.file_uploader("Upload your data file", type=["csv", "xlsx"])
    
    if data is not None:
        # Load data
        if data.name.endswith('.csv'):
            df = pd.read_csv(data)
        else:
            df = pd.read_excel(data)
        
        st.write("Data Preview:")
        st.write(df.head())

        # Remove ₹ symbol from a specific column (e.g., 'Price') if exists
        if 'Price' in df.columns:
            df['Price'] = df['Price'].str.replace('₹', '', regex=True).astype(float)
            st.write("Removed ₹ symbol from 'Price' column.")

        # Display DataFrame info using StringIO to capture the output
        st.subheader("Data Structure Information")
        buffer = io.StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)  # Display info summary

        # Display descriptive statistics
        st.subheader("Descriptive Statistics")
        st.write(df.describe())
    else:
        st.write("Please upload a CSV or Excel file to generate insights.")

# Sidebar navigation with default to 'Home'
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ("Home", "Analytics Overview", "Deep Insights"), index=0)

# Display the selected page
if page == "Home":
    home_page()
elif page == "Analytics Overview":
    analytics_page()
elif page == "Deep Insights":
    insights_page()