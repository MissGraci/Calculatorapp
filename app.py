import streamlit as st
import pandas as pd

st.set_page_config(page_title="Converted CS IBDP Calculator – Mrs Graci", layout="centered")

# ------------------------------
# Boundaries oficiais IB + PASB
# ------------------------------
boundaries_data = {
    "HL": {
        "Paper 1": [(0,11,1,30,49),(12,23,2,50,59),(24,35,3,60,69),(36,45,4,70,79),
                    (46,54,5,80,89),(55,64,6,90,95),(65,100,7,96,100)],
        "Paper 2": [(0,10,1,30,49),(11,20,2,50,59),(21,24,3,60,69),(25,31,4,70,79),
                    (32,37,5,80,89),(38,44,6,90,95),(45,65,7,96,100)],
        "Paper 3": [(0,5,1,30,49),(6,11,2,50,59),(12,14,3,60,69),(15,17,4,70,79),
                    (18,19,5,80,89),(20,22,6,90,95),(23,30,7,96,100)],
        "IA Solution": [(0,4,1,30,49),(5,9,2,50,59),(10,14,3,60,69),(15,18,4,70,79),
                        (19,22,5,80,89),(23,26,6,90,95),(27,34,7,96,100)],
        "Final Grade (calculated)": [(0,13,1,30,49),(14,28,2,50,59),(29,39,3,60,69),
                                     (40,49,4,70,79),(50,59,5,80,89),(60,69,6,90,95),(70,100,7,96,100)]
    },
    "SL": {
        "Paper 1": [(0,5,1,30,49),(6,11,2,50,59),(12,20,3,60,69),(21,29,4,70,79),
                    (30,37,5,80,89),(38,46,6,90,95),(47,70,7,96,100)],
        "Paper 2": [(0,7,1,30,49),(8,15,2,50,59),(16,20,3,60,69),(21,22,4,70,79),
                    (23,25,5,80,89),(26,27,6,90,95),(28,45,7,96,100)],
        "IA Solution": [(0,4,1,30,49),(5,9,2,50,59),(10,14,3,60,69),(15,18,4,70,79),
                        (19,22,5,80,89),(23,26,6,90,95),(27,34,7,96,100)],
        "Final Grade (calculated)": [(0,11,1,30,49),(12,23,2,50,59),(24,36,3,60,69),
                                     (37,47,4,70,79),(48,57,5,80,89),(58,68,6,90,95),(68,100,7,96,100)]
    }
}

# Máximos oficiais IB
max_marks = {
    "HL": {"Paper 1": 100, "Paper 2": 65, "Paper 3": 30, "IA Solution": 34, "Final Grade (calculated)": 100},
    "SL": {"Paper 1": 70, "Paper 2": 45, "IA Solution": 34, "Final Grade (calculated)": 100}
}

# Função para calcular IB Grade usando boundaries
def calculate_ib_grade(level, assessment, score, total):
    max_ib_marks = max_marks[level][assessment]
    raw_ib = (score / total) * max_ib_marks if total > 0 else 0
    grade, pasb_range, pasb_value = None, None, None
    for low, high, g, pasb_low, pasb_high in boundaries_data[level][assessment]:
        if low <= raw_ib <= high:
            grade = g
            pasb_range = f"{pasb_low}–{pasb_high}"
            pasb_value = pasb_low + (raw_ib - low) / (high - low) * (pasb_high - pasb_low)
            break
    return int(round(raw_ib)), grade, pasb_range, pasb_value

# ------------------------------
# Cabeçalho
# ------------------------------
st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: center; gap: 15px;">
        <img src="https://raw.githubusercontent.com/MissGraci/Calculatorapp/main/ib-world-school-logo-2-colour-rev.png" width="60">
        <h1 style="margin: 0; color: #1d427c; text-align: center;">
            Converted CS IBDP Calculator
        </h1>
        <img src="https://raw.githubusercontent.com/MissGraci/Calculatorapp/main/PASB-New-Logo-2021_G.png" width="120">
    </div>
    """,
    unsafe_allow_html=True
)

# Escolha do modo
mode = st.radio("Choose mode:", ["Student Mode", "Teacher Mode"])

# =====================================================
# STUDENT MODE
# =====================================================
if mode == "Student Mode":
    st.subheader("Student Calculator")

    level = st.radio("Select your course level:", ["SL", "HL"])
    if level == "HL":
        assessment = st.selectbox("Select assessment:", ["Paper 1", "Paper 2", "Paper 3", "IA Solution", "Final Grade (calculated)"])
    else:
        assessment = st.selectbox("Select assessment:", ["Paper 1", "Paper 2", "IA Solution", "Final Grade (calculated)"])

    score = st.number_input("Your marks", min_value=0, step=1, format="%d")
    total = st.number_input("Total marks possible", min_value=1, step=1, format="%d")

    raw_ib, ib_grade, pasb_range, pasb_value = calculate_ib_grade(level, assessment, score, total)

    if ib_grade is not None:
        # Caixas rápidas
        st.success(f"Converted IB Marks: {raw_ib}/{max_marks[level][assessment]}  |  IB Grade: {ib_grade}")
        st.info(f"PASB GPA Range: {pasb_range}  |  Converted PASB Value: {pasb_value:.2f}")

        # Tabela detalhada
        results = {
            "Assessment": [assessment],
            "IB Grade": [ib_grade],
            "Real %": [f"{(score/total)*100:.2f}%" if total > 0 else "0%"],
            "Converted IB Marks": [f"{raw_ib}/{max_marks[level][assessment]}"],
            "PASB GPA Range": [pasb_range],
            "Converted PASB Value": [f"{pasb_value:.2f}"]
        }

        df = pd.DataFrame(results)
        st.dataframe(df, use_container_width=True)

# =====================================================
# TEACHER MODE
# =====================================================
else:
    st.subheader("Teacher Mode - IB Grade Predictor")

    if "records" not in st.session_state:
        st.session_state["records"] = pd.DataFrame(columns=[
            "Student", "Level", "Paper 1", "Paper 2", "Paper 3", "IA", 
            "Final %", "IB Grade", "PASB GPA Range", "Converted PASB Value"
        ])

    student = st.text_input("Student Name")
    level = st.radio("Course Level:", ["SL", "HL"], key="teacher_level")
    p1 = st.number_input("Paper 1", min_value=0, max_value=100, step=1)
    p2 = st.number_input("Paper 2", min_value=0, max_value=100, step=1)
    p3 = st.number_input("Paper 3", min_value=0, max_value=100, step=1) if level == "HL" else 0
    ia = st.number_input("IA", min_value=0, max_value=100, step=1)

    if st.button("Save Student Record"):
        if level == "HL":
            final_pct = (p1 * 0.4) + (p2 * 0.2) + (p3 * 0.2) + (ia * 0.2)
        else:
            final_pct = (p1 * 0.45) + (p2 * 0.25) + (ia * 0.30)

        # Determinar IB grade pela escala "Final Grade (calculated)"
        raw_ib, ib_grade, pasb_range, pasb_value = calculate_ib_grade(level, "Final Grade (calculated)", final_pct, 100)

        new_record = {
            "Student": student,
            "Level": level,
            "Paper 1": p1,
            "Paper 2": p2,
            "Paper 3": p3 if level == "HL" else "-",
            "IA": ia,
            "Final %": round(final_pct, 2),
            "IB Grade": ib_grade,
            "PASB GPA Range": pasb_range,
            "Converted PASB Value": round(pasb_value, 2) if pasb_value else None
        }
        st.session_state["records"] = pd.concat([st.session_state["records"], pd.DataFrame([new_record])], ignore_index=True)

    st.write("### Class Predictions")
    st.dataframe(st.session_state["records"], use_container_width=True)

    st.download_button(
        label="Download CSV",
        data=st.session_state["records"].to_csv(index=False),
        file_name="ib_predicted_grades.csv",
        mime="text/csv"
    )
