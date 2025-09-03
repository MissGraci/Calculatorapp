import streamlit as st

st.set_page_config(page_title="Converted CS IBDP Calculator – Mrs Graci", layout="centered")

st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: center; gap: 15px;">
        <img src="https://raw.githubusercontent.com/MissGraci/Calculatorapp/main/ib-world-school-logo-2-colour-rev.png" width="60">
        <h1 style="margin: 0; color: #1d427c; text-align: center;">
            Converted CS IBDP Calculator
        </h1>
        <img src="https://raw.githubusercontent.com/MissGraci/Calculatorapp/main/PASB-New-Logo-2021_G.png" width="120">
    </div>
    <p style='text-align: center; color: gray;'>(only SUMMATIVE will be converted - Mrs Dias Gracielle)</p>
    <p style='text-align: center; color: white;'> Please, enter your summative mark to see your IB Grade, PASB Range, and Converted PASB Value
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

score = st.number_input("Your marks", min_value=0, step=1, format="%d")
total = st.number_input("Total marks possible", min_value=1, step=1, format="%d")

# Boundaries IB oficiais + conversão PASB (30–100)
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

        # --- HTML estilizado com azul, vermelho e cinza PASB ---
        st.markdown(
            f"""
            <div style="
                background-color:#f5f5f5; 
                color:#1d1d1d; 
                padding:20px; 
                border-radius:12px; 
                border: 2px solid #1d427c;
                font-family:Arial, sans-serif;
                margin-top:20px;">
                
                <h3 style="margin-bottom:15px; color:#1d427c; text-align:center;">
                    📊 Results – {assessment}
                </h3>
                
                <table style="width:100%; border-collapse: collapse; text-align:center;">
                    <tr style="background-color:#1d427c; color:white;">
                        <th style="padding:10px;">IB Grade</th>
                        <th style="padding:10px;">Real IB %</th>
                        <th style="padding:10px;">PASB GPA Range</th>
                        <th style="padding:10px;">Converted PASB Value</th>
                    </tr>
                    <tr style="background-color:#ffffff; color:#1d1d1d; font-weight:600;">
                        <td style="padding:12px; border-bottom:1px solid #ccc;">{ib_grade}</td>
                        <td style="padding:12px; border-bottom:1px solid #ccc; color:#d32f2f;">{percentage:.2f}%</td>
                        <td style="padding:12px; border-bottom:1px solid #ccc; color:#1d427c;">{pasb_range}</td>
                        <td style="padding:12px; border-bottom:1px solid #ccc; color:#444;">{pasb_value:.2f}</td>
                    </tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠️ Percentage is outside the defined IB boundaries.")





