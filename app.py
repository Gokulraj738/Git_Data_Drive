# streamlit_app.py
from aifc import Error
import streamlit as st
import pandas as pd
import mysql.connector # type: ignore

# Connect to MySQL database
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

# Database connection parameters
host_name = 'localhost'  # e.g., 'localhost'
user_name = 'root'    # MySQL username
user_password = 'mysql' # MySQL password
db_name = 'github_data'         # Your database name

# Create a connection
connection = create_connection(host_name, user_name, user_password, db_name)

# Load data from MySQL database
query = "SELECT * FROM repositories;"
df = pd.read_sql(query, connection)

# Streamlit App
st.title("GitHub Repository Insights")

# Filter by Programming Language
languages = df['Programming_Language'].unique()
selected_language = st.selectbox("Select Programming Language", languages)

filtered_df = df[df['Programming_Language'] == selected_language]

# Display basic metrics
st.write(f"Total Repositories for {selected_language}: {filtered_df.shape[0]}")
st.write(f"Total Stars for {selected_language}: {filtered_df['Number_of_Stars'].sum()}")
st.write(f"Total Forks for {selected_language}: {filtered_df['Number_of_Forks'].sum()}")

# Top repositories by stars
st.subheader(f"Top 5 Starred Repositories in {selected_language}")
top_repos = filtered_df[['Repository_Name', 'Number_of_Stars', 'URL']].sort_values(by='Number_of_Stars', ascending=False).head(5)
st.table(top_repos)

# Visualize stars distribution
st.subheader("Stars Distribution")
st.bar_chart(filtered_df['Number_of_Stars'])

# Visualize forks distribution
st.subheader("Forks Distribution")
st.bar_chart(filtered_df['Number_of_Forks'])

# Link to the repository
st.subheader("Explore Repositories")
st.write(filtered_df[['Repository_Name', 'URL']].to_html(escape=False, index=False), unsafe_allow_html=True)
