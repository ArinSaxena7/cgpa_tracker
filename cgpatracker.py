import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

grade_points = {
    "A+": 10, "A": 9, "B+": 8, "B": 7,
    "C+": 6, "C": 5, "D+": 4, "D": 3, "F": 0
}

st.title("📊 CGPA & Study Hours Analysis")
st.subheader("Minor Project by Arin Saxena")

n = st.number_input("Enter total subjects:", min_value=1, step=1)

subjects = []

for i in range(n):
    st.subheader(f"Subject {i+1}")
    name = st.text_input(f"Name of subject {i+1}", key=f"name{i}")
    credit = st.number_input(f"Credits for {name}", min_value=1, key=f"credit{i}")
    grade = st.selectbox(f"Grade for {name}", options=list(grade_points.keys()), key=f"grade{i}")
    study_hours = st.number_input(f"Study hours per week for {name}", min_value=0, key=f"hours{i}")
    
    if name:
        subjects.append({
            "Name": name,
            "Credit": credit,
            "Grade": grade,
            "Time": study_hours
        })

if st.button("Calculate CGPA & Generate Report") and subjects:
    total_credits = sum(sub["Credit"] for sub in subjects)
    total_points = sum(grade_points[sub["Grade"]] * sub["Credit"] for sub in subjects)
    cgpa = total_points / total_credits
    st.success(f"🎓 Your CGPA is: {cgpa:.2f}")

    st.subheader("📖 Suggested Study Hours per Week")
    for s in subjects:
        base_hours = s["Credit"]*2
        if s["Grade"] in ["C", "C+", "D", "D+", "F"]:
            base_hours += 2
            st.warning(f"{s['Name']}: Needs {base_hours} hrs/week (focus more here)")
        else:
            st.info(f"{s['Name']}: {base_hours} hrs/week is enough")

    # Plot chart
    x = [s["Credit"]*2 + (2 if s["Grade"] in ["C","C+","D","D+","F"] else 0) for s in subjects]
    y = [s["Grade"] for s in subjects]

    fig, ax = plt.subplots(figsize=(8,6))
    ax.barh(y, x, color="skyblue", edgecolor="black")
    ax.set_xlabel("Hours of Study")
    ax.set_ylabel("Grades")
    ax.set_title("Suggested Study Hours vs Grades")
    ax.invert_yaxis()
    st.pyplot(fig)

    # Generate PDF
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 800, "CGPA Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, 770, f"Your CGPA is: {cgpa:.2f}")

    # Table
    table_data = [["Subject", "Credits", "Grade", "Suggested Hours"]]
    for s in subjects:
        base_hours = s["Credit"]*2
        if s["Grade"] in ["C", "C+", "D", "D+", "F"]:
            base_hours += 2
        table_data.append([s["Name"], s["Credit"], s["Grade"], f"{base_hours} hrs/week"])

    table = Table(table_data, colWidths=[150, 80, 80, 130])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))
    table.wrapOn(c, 50, 700)
    table.drawOn(c, 50, 600)

    # Save chart to PDF using ImageReader
    chart_buffer = BytesIO()
    fig.savefig(chart_buffer, format='PNG', bbox_inches='tight')
    plt.close(fig)
    chart_buffer.seek(0)
    img = ImageReader(chart_buffer)
    c.drawImage(img, 100, 250, width=400, height=300)

    c.save()
    pdf_buffer.seek(0)

    st.download_button(
        label="📥 Download PDF Report",
        data=pdf_buffer,
        file_name="CGPA_Report.pdf",
        mime="application/pdf"
    )
