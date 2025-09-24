# cgpa_tracker_streamlit.py

import streamlit as st

# --- Grade Mapping ---
grade_points = {
    "A": 10,
    "B": 8,
    "C": 6,
    "D": 4,
    "F": 0
}
 
st.title("📊 CGPA Tracker")

# --- Subject Entry ---
st.header("➕ Add a Subject")
name = st.text_input("Subject Name")
credit = st.number_input("Credits", min_value=1, max_value=10, step=1)
grade = st.selectbox("Grade", ["A", "B", "C", "D", "F"])
study_hours = st.number_input("Study hours per week", min_value=0, max_value=50, step=1)

# Initialize session state to store subjects
if "subjects" not in st.session_state:
    st.session_state.subjects = []

# Add subject button
if st.button("Add Subject"):
    subject = {
        "Name": name,
        "Credit": credit,
        "Grade": grade,
        "Time": study_hours
    }
    st.session_state.subjects.append(subject)
    st.success(f"✅ {name} added!")

# Show current subjects
if st.session_state.subjects:
    st.header("📋 Current Subjects")
    st.table(st.session_state.subjects)

    # --- CGPA Calculation ---
    total_credits = 0
    total_points = 0

    for sub in st.session_state.subjects:
        credit = sub["Credit"]
        grade = sub["Grade"]

        total_credits += credit
        total_points += grade_points[grade] * credit

    if total_credits > 0:
        cgpa = total_points / total_credits
        st.subheader(f"📊 Your CGPA: {round(cgpa, 2)}")

    # --- Suggested Study Hours ---
    st.header("📖 Suggested Study Hours")
    for sub in st.session_state.subjects:
        base_hours = sub["Credit"] * 2
        if sub["Grade"] in ["C", "D", "F"]:
            base_hours += 2
        st.write(f"**{sub['Name']}** → {base_hours} hrs/week")

    # --- Prediction ---
    st.header("🔮 Predict Future CGPA")
    extra_hours = st.slider("Extra study hours per week", 0, 20, 2)
    improvement = (extra_hours / 2) * 0.2   # simple rule
    predicted_cgpa = min(10, cgpa + improvement)
    st.info(f"If you study +{extra_hours} hrs/week → Predicted CGPA ≈ **{round(predicted_cgpa, 2)}**")
