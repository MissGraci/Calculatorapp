import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Converted CS IBDP Calculator – Mrs Graci", layout="centered")

# Cabeçalho
st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: center; gap: 15px;">
        <img src="https://raw.githubusercontent.com/MissGraci/Calculatorapp/main/ib-world-school-logo-2-colour-rev.png" width="60">
        <h1 style="margin: 0; color: #1d427c; text-align: center;">
            Converted CS IBDP Calculator
        </h1>
        <img src="https://raw.githubusercontent.com/MissGraci/Calculatorapp/main/PASB-New-Logo-2021_G.png" width="120">
    </div>
    <p style='text-align: center; color: gray;'>(only SUMMATIVE will be converted - Mrs. Dias, Gracielle)</p>
    Please, enter your summative marks to see your IB Grade, PASB Range, and Converted PASB Value
    """,
    unsafe_allow_html=True
)

# Escolha de nível
level = st.radio("Select your course level:", ["SL", "HL"])

# Escolha de avaliação
if level == "HL":
    assessment = st.selectbox("Select assessment:", ["Paper 1", "Paper 2", "Paper 3", "IA Solution", "Final Grade"])
else:
    assessment = st.selectbox("Select assessment:", ["Paper 1", "Paper 2", "IA Solution", "Final Grade"])

# Entrada de notas
score = st.number_input("Your marks", min_value=0, step=1, format="%d")
total = st.number_input("Total marks possible", min_value=1, step=1, format="%d")

# Boundaries oficiais IB + ranges PASB
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
        "Final Grade": [(0,13,1,30,49),(14,28,2,50,59),(29,39,3,60,69),(40,49,4,70,79),
                        (50,59,5,80,89),(60,69,6,90,95),(70,100,7,96,100)]
    },
    "SL": {
        "Paper 1": [(0,5,1,30,49),(6,11,2,50,59),(12,20,3,60,69),(21,29,4,70,79),
                    (30,37,5,80,89),(38,46,6,90,95),(47,70,7,96,100)],
        "Paper 2": [(0,7,1,30,49),(8,15,2,50,59),(16,20,3,60,69),(21,22,4,70,79),
                    (23,25,5,80,89),(26,27,6,90,95),(28,45,7,96,100)],
        "IA Solution": [(0,4,1,30,49),(5,9,2,50,59),(10,14,3,60,69),(15,18,4,70,79),
                        (19,22,5,80,89),(23,26,6,90,95),(27,34,7,96,100)],
        "Final Grade": [(0,11,1,30,49),(12,23,2,50,59),(24,36,3,60,69),(37,47,4,70,79),
                        (48,57,5,80,89),(58,68,6,90,95),(68,100,7,96,100)]
    }
}

# Cálculo
if total > 0:
    percentage = (score / total) * 100
    st.info(f"Your percentage: **{percentage:.2f}%**")

    selected_boundaries = boundaries_data[level][assessment]

    ib_grade, pasb_range, pasb_value = None, None, None

    for low, high, grade, pasb_low, pasb_high in selected_boundaries:
        if low <= percentage <= high:
            ib_grade = grade
            pasb_range = f"{pasb_low}–{pasb_high}"
            pasb_value = pasb_low + (percentage - low) / (high - low) * (pasb_high - pasb_low)
            break

    if ib_grade is not None:
        st.divider()

        # Criar tabela como DataFrame
        results = {
            "Assessment": [assessment],
            "IB Grade": [ib_grade],
            "Real (IB grade)": [f"{percentage:.2f}"],
            "PASB GPA Range": [pasb_range],
            "Converted PASB Value": [f"{pasb_value:.2f}"]
        }

        df = pd.DataFrame(results)
        st.dataframe(df, use_container_width=True)

    else:
        st.warning("⚠️ Percentage is outside the defined IB boundaries.")

