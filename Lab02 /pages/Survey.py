# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).
from pathlib import Path
import csv

DATA_FILE = Path(__file__).resolve().parent.parent / "data.csv"

st.set_page_config(
    page_title="Survey",
    page_icon="📝",)

st.title("Study Habits Survey")
st.write(
    "Help us understand where students prefer to study!"
)

with st.form("study_survey"):

    st.subheader("Survey Question")

    study_location = st.text_input(
        "What is your favorite place to study?"
    )

    submitted = st.form_submit_button("Submit Response")

    if submitted:

        if study_location.strip():

            file_exists = DATA_FILE.exists() and DATA_FILE.stat().st_size > 0

            with open(DATA_FILE, "a", newline="") as file:

                writer = csv.writer(file)

                if not file_exists:
                    writer.writerow(["category", "values"])

                writer.writerow([study_location.strip().title(), ""])

            st.success("Thank you! Your response has been recorded.")

        else:
            st.warning("Please enter a response before submitting.")



# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if DATA_FILE.exists() and DATA_FILE.stat().st_size > 0:
    current_data_df = pd.read_csv(DATA_FILE)
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
