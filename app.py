import streamlit as st

st.set_page_config(page_title="CS Grade Calculator", page_icon="🎓")

st.title("🎓 Computer Science Grade Calculator")
st.write("Enter your scores to calculate your final % and IB grade.")

formative_scores = st.text_input("Formative scores (separate with commas)", "70,80,60")
summative_scores = st.text_input("Summative scores (separate with commas)", "50,60")

formative_list = [float(x.strip()) for x in formative_scores.split(",") if x.strip()]
summative_list = [float(x.strip()) for x in summative_scores.split(",") if x.strip()]

if formative_list and summative_list:
    formative_avg = sum(formative_list) / len(formative_list)
    summative_avg = sum(summative_list) / len(summative_list)

    final_percentage = (formative_avg * 0.3) + (summative_avg * 0.7)

    st.subheader("Step 1 – Averages")
    st.write(f"Formative Avg = {formative_avg:.2f}%")
    st.write(f"Summative Avg = {summative_avg:.2f}%")

    st.subheader("Step 2 – Weighted Final %")
    st.write(f"Final % = ({formative_avg:.2f} × 30%) + ({summative_avg:.2f} × 70%)")
    st.success(f"Final % = {final_percentage:.2f}%")

    if final_percentage <= 13:
        ib_grade, gpa = 1, "30–49"
    elif final_percentage <= 28:
        ib_grade, gpa = 2, "50–59"
    elif final_percentage <= 39:
        ib_grade, gpa = 3, "60–69"
    elif final_percentage <= 49:
        ib_grade, gpa = 4, "70–79"
    elif final_percentage <= 59:
        ib_grade, gpa = 5, "80–89"
    elif final_percentage <= 69:
        ib_grade, gpa = 6, "90–95"
    else:
        ib_grade, gpa = 7, "96–100"

    st.subheader("Step 3 – IB Conversion")
    st.write(f"IB Grade: **{ib_grade}**")
    st.write(f"PASB GPA Range: **{gpa}**")
