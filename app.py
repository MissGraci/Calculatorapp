import streamlit as st

st.set_page_config(page_title="Converted CS IBDP Calculator – Mrs Graci", layout="centered")

st.markdown("<h1 style='text-align: center; color: #2C3E50;'>🎓 Converted CS IBDP Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>(only SUMMATIVE will be converted)</p>", unsafe_allow_html=True)
st.write("Enter your summative mark to see your IB Grade, PASB Range, and Converted PASB Value:")

score = st.number_input("Your marks", min_value=0, step=1, format="%d")
total = st.number_input("Total marks possible", min_value=0, step=1, format="%d")

if total > 0:  
    percentage = (score / total) * 100
    st.info(f"Your percentage: **{percentage:.2f}%**")

    boundaries = [
        (0, 13, 1, 30, 49),
        (14, 28, 2, 50, 59),
        (29, 39, 3, 60, 69),
        (40, 49, 4, 70, 79),
        (50, 59, 5, 80, 89),
        (60, 69, 6, 90, 95),
        (70, 100, 7, 96, 100),
    ]

    ib_grade, gpa_range, gpa_exact = None, None, None

    for low, high, ib, pasb_low, pasb_high in boundaries:
        if low <= percentage <= high:
            ib_grade = ib
            gpa_range = f"{pasb_low}–{pasb_high}"
            gpa_exact = pasb_low + (percentage - low) / (high - low) * (pasb_high - pasb_low)
            break

    if ib_grade is not None:
        st.divider()
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("IB Grade", ib_grade)
        with col2:
            st.metric("PASB GPA Range", gpa_range)
        with col3:
            st.metric("Converted PASB Value", f"{gpa_exact:.2f}")
    else:
        st.warning("⚠️ Percentage is outside the defined boundaries.")
else:
    st.info("ℹ️ Please enter your total marks to calculate results.")
