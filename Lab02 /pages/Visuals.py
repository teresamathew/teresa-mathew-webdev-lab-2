import json
from pathlib import Path

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

DATA_FILE = Path(__file__).resolve().parent.parent / "data.csv"


st.set_page_config(
    page_title="Books Read Dashboard",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Books Read Dashboard")
st.write(
    "Explore book-reading data across three years "
    "and compare reading genres."
)


data_path = Path(__file__).resolve().parent.parent / "data.json"

with open(data_path, "r", encoding="utf-8") as file:
    data = json.load(file)


years_data = data["years"]
years = list(years_data.keys())
genres = list(years_data[years[0]].keys())


genre_totals = {}

for genre in genres:
    total = 0

    for year in years:
        total += years_data[year][genre]

    genre_totals[genre] = total


st.header("1. Total Books Read by Genre")
st.write(
    "This static bar chart shows the total number of books "
    "recorded in each genre across 2023, 2024, and 2025."
)

fig1, ax1 = plt.subplots()

ax1.bar(
    list(genre_totals.keys()),
    list(genre_totals.values())
)

ax1.set_title("Total Books Read by Genre (2023–2025)")
ax1.set_xlabel("Book Genre")
ax1.set_ylabel("Number of Books")
ax1.tick_params(axis="x", rotation=25)

fig1.tight_layout()
st.pyplot(fig1)
plt.close(fig1)


st.header("2. Genre Distribution by Year")
st.write(
    "Select a year to see how the books recorded for that year "
    "are distributed among the genres."
)


if "selected_year" not in st.session_state:
    st.session_state.selected_year = years[0]


st.selectbox(
    "Choose a year:",
    options=years,
    key="selected_year"
)


selected_year = st.session_state.selected_year

selected_data = years_data[selected_year]

fig2, ax2 = plt.subplots()

ax2.pie(
    list(selected_data.values()),
    labels=list(selected_data.keys()),
    autopct="%1.1f%%",
    startangle=90
)

ax2.set_title(f"Genre Distribution in {selected_year}")
ax2.axis("equal")

st.pyplot(fig2)
plt.close(fig2)


total_books = sum(selected_data.values())

st.metric(
    label=f"Total Books Recorded in {selected_year}",
    value=total_books
)


st.header("Part 2: Survey Results")

if DATA_FILE.exists() and DATA_FILE.stat().st_size > 0:

    df = pd.read_csv(DATA_FILE)
    st.write("CSV column names:", list(df.columns))
    st.write("CSV contents:", df)

    if "Category" in df.columns:

        responses = df["Category"].dropna().astype(str).str.strip()

        responses = responses[responses != ""]

        if len(responses) > 0:

            st.write("Here are the results from our study habits survey!")

            st.subheader("Favorite Study Locations")

            location_counts = responses.value_counts()

            fig, ax = plt.subplots()

            ax.pie(
                location_counts.values,
                labels=location_counts.index,
                autopct="%1.1f%%"
            )

            ax.set_title("Favorite Study Locations")

            st.pyplot(fig)
            plt.close(fig)

            st.subheader("Explore Study Location Results")

            if "top_n_locations" not in st.session_state:
                st.session_state.top_n_locations = min(
                    3, len(location_counts)
                )

            top_n = st.slider(
                "How many study locations would you like to see?",
                min_value=1,
                max_value=len(location_counts),
                value=st.session_state.top_n_locations,
                key="top_n_locations"
            )

            dynamic_counts = location_counts.head(top_n)

            fig2, ax2 = plt.subplots()

            ax2.bar(
                dynamic_counts.index,
                dynamic_counts.values
            )

            ax2.set_title("Most Popular Study Locations")
            ax2.set_xlabel("Study Location")
            ax2.set_ylabel("Number of Responses")

            st.pyplot(fig2)
            plt.close(fig2)

        else:
            st.info("Your CSV has a category column, but it does not contain any survey responses.")

    else:
        st.error("Your CSV does not contain a column named 'category'.")

else:
    st.info("The data.csv file is empty or does not exist.")
