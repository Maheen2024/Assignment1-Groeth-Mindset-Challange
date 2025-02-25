import streamlit as st
import pandas as pd
from io import BytesIO

# Sample career dataset
CAREER_DATA = {
    "Career": ["Software Engineer", "Data Scientist", "Graphic Designer", "Marketing Manager", "Mechanical Engineer"],
    "Skills": ["Programming, Problem-Solving", "Statistics, Machine Learning", "Creativity, Design Tools", "Communication, Strategy", "Engineering, CAD"],
    "Interests": ["Technology", "Data Analysis", "Art", "Business", "Machines"],
    "Values": ["Innovation", "Research", "Creativity", "Leadership", "Precision"]
}

df = pd.DataFrame(CAREER_DATA)

# Streamlit UI
st.title("Growth Mindset Challange")
st.write("""Growth Mindset Agentia refers to artificial intelligence designed to learn, adapt, and evolve continuously.
It embodies a growth mindset, embracing challenges, persisting through obstacles, and viewing failures as opportunities for growth.
 This agentia learns from data, experiences, and interactions, enabling it to improve performance, innovate, and make informed decisions.""")
st.title("🚀 Career Assessment App")
st.write("Enter your skills, interests, and values to get a career recommendation.")

if "selected_career" not in st.session_state:
    st.session_state.selected_career = ""
    st.session_state.skills = ""
    st.session_state.interests = ""
    st.session_state.values = ""
    st.session_state.recommended_careers = []

def update_inputs():
    selected_career = st.session_state.get("career_radio", "")
    if selected_career in df["Career"].values:
        career_data = df[df["Career"] == selected_career].iloc[0]
        st.session_state.selected_career = selected_career
        st.session_state.skills = career_data["Skills"]
        st.session_state.interests = career_data["Interests"]
        st.session_state.values = career_data["Values"]

def recommend_careers():
    skills_input = st.session_state.get("skills", "")
    interests_input = st.session_state.get("interests", "")
    values_input = st.session_state.get("values", "")
    
    matching_careers = df[
        df['Skills'].str.contains(skills_input, case=False, na=False) |
        df['Interests'].str.contains(interests_input, case=False, na=False) |
        df['Values'].str.contains(values_input, case=False, na=False)
    ]
    
    st.session_state.recommended_careers = matching_careers["Career"].tolist()
    if not st.session_state.recommended_careers:
        st.warning("No matching career found. Try adjusting your input.")

# Dynamic text input with career suggestions
skills = st.text_input("Enter your skills (comma-separated):", key="skills")
interests = st.text_input("Enter your interests (comma-separated):", key="interests")
values = st.text_input("Enter your values (comma-separated):", key="values")

if st.button("Get Career Recommendation"):
    recommend_careers()

if st.session_state.recommended_careers:
    selected_career = st.radio("Select a career:", st.session_state.recommended_careers, key="career_radio", on_change=update_inputs)

if st.session_state.selected_career:
    st.subheader(f"✅ Selected Career: {st.session_state.selected_career}")
    if st.button("Confirm Selection"):
        st.write(f"You have confirmed: {st.session_state.selected_career}")
        
        selected_career_data = df[df["Career"] == st.session_state.selected_career]

        # Save CSV to memory with proper encoding and delimiter
        csv_bytes = BytesIO()
        selected_career_data.to_csv(csv_bytes, index=False, sep=",", encoding="utf-8-sig")
        csv_bytes.seek(0)

        # Download button for CSV
        st.download_button(
            label="Download Career Data as CSV",
            data=csv_bytes,
            file_name="career_data.csv",
            mime="text/csv"
        )
