
import math
import base64
from pathlib import Path

import streamlit as st
import pandas as pd


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="IBDP Computer Science Grade Converter",
    page_icon="💻",
    layout="centered"
)


# ============================================================
# IMAGE PATHS
# ============================================================

APP_DIR = Path(__file__).resolve().parent

PASB_LOGO = APP_DIR / "PASB-New-Logo-2021_G.png"

IB_LOGO = APP_DIR / "ib-world-school-logo-2-colour-rev.png"


def image_to_base64(image_path):
    """
    Converts an image into Base64 so it can be displayed
    inside custom HTML/CSS elements.
    """

    if not image_path.exists():
        return None

    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


pasb_logo_base64 = image_to_base64(PASB_LOGO)
ib_logo_base64 = image_to_base64(IB_LOGO)


# ============================================================
# PASB GRADE SCALE
# ============================================================

PASB_RANGES = {
    1: (0, 50),
    2: (50, 59),
    3: (60, 69),
    4: (70, 79),
    5: (80, 89),
    6: (90, 95),
    7: (96, 100),
}


# ============================================================
# MAY 2025 IB REFERENCE BOUNDARIES
#
# These are NOT official 2027 boundaries.
# The calculator uses the average of the 2025 TZ2
# and TZ3 lower thresholds as provisional references.
# ============================================================

BOUNDARIES_2025 = {

    "HL": {

        "TZ2": {

            "Paper 1": [
                (0, 17, 1),
                (18, 35, 2),
                (36, 48, 3),
                (49, 58, 4),
                (59, 68, 5),
                (69, 78, 6),
                (79, 100, 7),
            ],

            "Paper 2": [
                (0, 10, 1),
                (11, 21, 2),
                (22, 26, 3),
                (27, 32, 4),
                (33, 38, 5),
                (39, 44, 6),
                (45, 65, 7),
            ],

            "IA": [
                (0, 4, 1),
                (5, 9, 2),
                (10, 14, 3),
                (15, 18, 4),
                (19, 22, 5),
                (23, 26, 6),
                (27, 34, 7),
            ],

            "Final Grade": [
                (0, 14, 1),
                (15, 30, 2),
                (31, 42, 3),
                (43, 52, 4),
                (53, 63, 5),
                (64, 73, 6),
                (74, 100, 7),
            ],
        },

        "TZ3": {

            "Paper 1": [
                (0, 17, 1),
                (18, 35, 2),
                (36, 48, 3),
                (49, 58, 4),
                (59, 69, 5),
                (70, 79, 6),
                (80, 100, 7),
            ],

            "Paper 2": [
                (0, 10, 1),
                (11, 20, 2),
                (21, 26, 3),
                (27, 32, 4),
                (33, 37, 5),
                (38, 43, 6),
                (44, 65, 7),
            ],

            "IA": [
                (0, 4, 1),
                (5, 9, 2),
                (10, 14, 3),
                (15, 18, 4),
                (19, 22, 5),
                (23, 26, 6),
                (27, 34, 7),
            ],

            "Final Grade": [
                (0, 16, 1),
                (17, 33, 2),
                (34, 45, 3),
                (46, 54, 4),
                (55, 64, 5),
                (65, 73, 6),
                (74, 100, 7),
            ],
        },
    },

    "SL": {

        "TZ2": {

            "Paper 1": [
                (0, 8, 1),
                (9, 17, 2),
                (18, 29, 3),
                (30, 37, 4),
                (38, 45, 5),
                (46, 53, 6),
                (54, 70, 7),
            ],

            "Paper 2": [
                (0, 8, 1),
                (9, 16, 2),
                (17, 21, 3),
                (22, 24, 4),
                (25, 26, 5),
                (27, 29, 6),
                (30, 45, 7),
            ],

            "IA": [
                (0, 4, 1),
                (5, 9, 2),
                (10, 14, 3),
                (15, 18, 4),
                (19, 22, 5),
                (23, 26, 6),
                (27, 34, 7),
            ],

            "Final Grade": [
                (0, 13, 1),
                (14, 28, 2),
                (29, 43, 3),
                (44, 53, 4),
                (54, 63, 5),
                (64, 73, 6),
                (74, 100, 7),
            ],
        },

        "TZ3": {

            "Paper 1": [
                (0, 8, 1),
                (9, 17, 2),
                (18, 27, 3),
                (28, 34, 4),
                (35, 42, 5),
                (43, 49, 6),
                (50, 70, 7),
            ],

            "Paper 2": [
                (0, 8, 1),
                (9, 16, 2),
                (17, 22, 3),
                (23, 24, 4),
                (25, 26, 5),
                (27, 28, 6),
                (29, 45, 7),
            ],

            "IA": [
                (0, 4, 1),
                (5, 9, 2),
                (10, 14, 3),
                (15, 18, 4),
                (19, 22, 5),
                (23, 26, 6),
                (27, 34, 7),
            ],

            "Final Grade": [
                (0, 13, 1),
                (14, 28, 2),
                (29, 42, 3),
                (43, 51, 4),
                (52, 61, 5),
                (62, 70, 6),
                (71, 100, 7),
            ],
        },
    },
}


# ============================================================
# OLD COMPONENT MAXIMUM MARKS
# Only used to convert 2025 thresholds to percentages.
# ============================================================

REFERENCE_MAX_MARKS = {
    "HL": {
        "Paper 1": 100,
        "Paper 2": 65,
        "IA": 34,
    },
    "SL": {
        "Paper 1": 70,
        "Paper 2": 45,
        "IA": 34,
    },
}


# ============================================================
# OFFICIAL 2027 ASSESSMENT STRUCTURE
# ============================================================

MAX_MARKS_2027 = {
    "HL": {
        "Paper 1": 80,
        "Paper 2": 80,
        "IA": 30,
    },
    "SL": {
        "Paper 1": 50,
        "Paper 2": 50,
        "IA": 30,
    },
}


WEIGHTS_2027 = {
    "HL": {
        "Paper 1": 0.40,
        "Paper 2": 0.40,
        "IA": 0.20,
    },
    "SL": {
        "Paper 1": 0.35,
        "Paper 2": 0.35,
        "IA": 0.30,
    },
}


# ============================================================
# SESSION STATE
# ============================================================

if "cs_registros" not in st.session_state:
    st.session_state.cs_registros = []

if "cs_ultimo_resultado" not in st.session_state:
    st.session_state.cs_ultimo_resultado = None


# ============================================================
# CALCULATION FUNCTIONS
# ============================================================

def round_half_up(value):
    return math.floor(value + 0.5)


def get_lower_boundary(boundaries, grade):

    for low, high, current_grade in boundaries:

        if current_grade == grade:
            return low

    return None


def build_component_boundaries(level, assessment):
    """
    Provisional boundaries based on the mean percentage
    of the 2025 TZ2 and TZ3 lower thresholds.
    """

    old_max = REFERENCE_MAX_MARKS[level][assessment]

    tz2 = BOUNDARIES_2025[level]["TZ2"][assessment]
    tz3 = BOUNDARIES_2025[level]["TZ3"][assessment]

    thresholds = {}

    for grade in range(1, 8):

        low_tz2 = get_lower_boundary(tz2, grade)
        low_tz3 = get_lower_boundary(tz3, grade)

        thresholds[grade] = (
            (low_tz2 / old_max * 100)
            + (low_tz3 / old_max * 100)
        ) / 2

    boundaries = []

    for grade in range(1, 8):

        low = thresholds[grade]

        high = (
            thresholds[grade + 1]
            if grade < 7
            else 100.0
        )

        boundaries.append((low, high, grade))

    return boundaries


def build_final_boundaries(level):

    tz2 = BOUNDARIES_2025[level]["TZ2"]["Final Grade"]
    tz3 = BOUNDARIES_2025[level]["TZ3"]["Final Grade"]

    thresholds = {}

    for grade in range(1, 8):

        low_tz2 = get_lower_boundary(tz2, grade)
        low_tz3 = get_lower_boundary(tz3, grade)

        thresholds[grade] = (
            low_tz2 + low_tz3
        ) / 2

    boundaries = []

    for grade in range(1, 8):

        low = thresholds[grade]

        high = (
            thresholds[grade + 1]
            if grade < 7
            else 100.0
        )

        boundaries.append((low, high, grade))

    return boundaries


def identify_ib_grade(boundaries, percentage):

    for low, high, grade in boundaries:

        if grade < 7:

            if low <= percentage < high:
                return grade, low, high

        else:

            if low <= percentage <= 100:
                return grade, low, high

    raise ValueError(
        "Unable to identify the estimated IB grade."
    )


def calculate_pasb(percentage, grade, low, high):

    pasb_low, pasb_high = PASB_RANGES[grade]

    if high == low:
        return float(pasb_low)

    position = (
        percentage - low
    ) / (
        high - low
    )

    position = max(
        0.0,
        min(position, 1.0)
    )

    return (
        pasb_low
        + position * (pasb_high - pasb_low)
    )


def calculate_result(
    student_name,
    level,
    assessment,
    student_marks,
    total_marks
):

    if total_marks <= 0:
        raise ValueError(
            "Total marks must be greater than zero."
        )

    if student_marks < 0 or student_marks > total_marks:
        raise ValueError(
            "Student marks must be between 0 and total marks."
        )

    percentage = (
        student_marks / total_marks
    ) * 100

    official_max = MAX_MARKS_2027[level][assessment]

    equivalent_marks = (
        percentage / 100
    ) * official_max

    boundaries = build_component_boundaries(
        level,
        assessment
    )

    grade, low, high = identify_ib_grade(
        boundaries,
        percentage
    )

    pasb_exact = calculate_pasb(
        percentage,
        grade,
        low,
        high
    )

    pasb_low, pasb_high = PASB_RANGES[grade]

    return {
        "Student": student_name,
        "Level": level,
        "Component": assessment,
        "Marks": (
            f"{student_marks:g}/{total_marks:g}"
        ),
        "Percentage (%)": round(percentage, 2),
        "Equivalent IB Marks": (
            f"{equivalent_marks:.2f}/{official_max}"
        ),
        "IB Grade": grade,
        "IB Boundaries": f"{low:.2f}–{high:.2f}%",
        "PASB Grade": round_half_up(pasb_exact),
        "PASB Range": f"{pasb_low}–{pasb_high}",
        "Exact PASB": round(pasb_exact, 2),
    }


def calculate_final_result(
    student_name,
    level,
    paper1,
    paper2,
    ia
):

    weights = WEIGHTS_2027[level]

    final_percentage = (
        paper1 * weights["Paper 1"]
        + paper2 * weights["Paper 2"]
        + ia * weights["IA"]
    )

    boundaries = build_final_boundaries(level)

    grade, low, high = identify_ib_grade(
        boundaries,
        final_percentage
    )

    pasb_exact = calculate_pasb(
        final_percentage,
        grade,
        low,
        high
    )

    pasb_low, pasb_high = PASB_RANGES[grade]

    return {
        "Student": student_name,
        "Level": level,
        "Component": "Final Grade",
        "Marks": "—",
        "Percentage (%)": round(final_percentage, 2),
        "Equivalent IB Marks": "—",
        "IB Grade": grade,
        "IB Boundaries": f"{low:.2f}–{high:.2f}%",
        "PASB Grade": round_half_up(pasb_exact),
        "PASB Range": f"{pasb_low}–{pasb_high}",
        "Exact PASB": round(pasb_exact, 2),
    }


def display_result(result):

    st.divider()

    st.subheader("Assessment Result")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Assessment %",
            f"{result['Percentage (%)']:.2f}%"
        )

    with c2:
        st.metric(
            "Estimated IB Grade",
            result["IB Grade"]
        )

    with c3:
        st.metric(
            "PASB Grade",
            result["PASB Grade"]
        )

    st.markdown(
        f"""
**Student:** {result['Student']}

**IB Level:** {result['Level']}

**Assessment:** {result['Component']}

**Student Marks:** {result['Marks']}

**Equivalent 2027 Marks:** {result['Equivalent IB Marks']}

**Provisional IB Boundaries:** {result['IB Boundaries']}

**PASB Range:** {result['PASB Range']}

**Exact PASB Conversion:** {result['Exact PASB']:.2f}
"""
    )


# ============================================================
# CUSTOM CSS - BLUE THEME
# ============================================================

st.markdown("""
<style>

.block-container {
    max-width: 1050px;
    padding-top: 2rem;
}

/* HEADER */

.cs-header {
    background: linear-gradient(
        135deg,
        #18304f 0%,
        #294f78 100%
    );

    padding: 34px 38px;
    border-radius: 22px;
    margin-bottom: 24px;

    box-shadow:
        0 6px 18px rgba(0,0,0,0.18);
}

/* HEADER LAYOUT */

.cs-header-content {
    display: flex;
    align-items: center;
    gap: 30px;
}

.cs-header-logo {
    flex: 0 0 auto;
}

.cs-header-logo img {
    width: 145px;
    max-width: 100%;
    height: auto;
    object-fit: contain;
}

.cs-header-text {
    flex: 1;
    min-width: 0;
}

/* HEADER TEXT */

.cs-header .kicker {
    color: #b9cbe0 !important;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.3px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.cs-header .heading {
    color: #FFFFFF !important;
    font-size: clamp(1.7rem, 3vw, 2.5rem);
    font-weight: 750;
    line-height: 1.15;
    margin-bottom: 14px;
}

.cs-header .subtitle {
    color: #dce7f4 !important;
    font-size: 15px;
    line-height: 1.5;
}

/* BADGES */

.cs-badge {
    display: inline-block;
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.22);

    color: #FFFFFF !important;

    padding: 7px 12px;
    border-radius: 20px;
    margin-right: 6px;
    margin-top: 12px;

    font-size: 12px;
    font-weight: 600;
}

/* INFORMATION BOX */

.cs-info {
    background-color: #edf3f8;
    border-left: 5px solid #294f78;

    padding: 18px 20px;
    border-radius: 10px;
    margin-bottom: 25px;

    color: #1d2d3e !important;
    line-height: 1.55;
}

.cs-info strong {
    color: #18304f !important;
}

/* BUTTONS */

div.stButton > button[kind="primary"] {
    background-color: #294f78 !important;
    color: #FFFFFF !important;
    border: 1px solid #294f78 !important;
    border-radius: 10px !important;
    font-weight: 650 !important;
}

div.stButton > button[kind="primary"]:hover {
    background-color: #3A6898 !important;
    border-color: #3A6898 !important;
    color: #FFFFFF !important;
}

/* FOOTER */

.cs-footer {
    text-align: center;
    color: #8B9BAF;
    font-size: 13px;
    padding: 12px 0 6px;
}

/* RESPONSIVE */

@media (max-width: 650px) {

    .cs-header {
        padding: 26px 22px;
    }

    .cs-header-content {
        flex-direction: column;
        align-items: flex-start;
        gap: 18px;
    }

    .cs-header-logo img {
        width: 120px;
    }

    .cs-header .heading {
        font-size: 1.8rem;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER WITH PASB LOGO
# ============================================================

if pasb_logo_base64:

    logo_html = (
        '<div class="cs-header-logo">'
        '<img src="data:image/png;base64,'
        + pasb_logo_base64
        + '" alt="PASB Logo">'
        '</div>'
    )

else:
    logo_html = ""


st.markdown(
    f"""
<div class="cs-header">
<div class="cs-header-content">
{logo_html}
<div class="cs-header-text">
<div class="kicker">PASB · ASSESSMENT TOOL</div>
<div class="heading">IBDP Computer Science<br>Grade Converter</div>
<div class="subtitle">Convert assessment performance into an estimated IB grade and PASB equivalent using the 2027 assessment structure. Organize student results in a grade table.</div>
<span class="cs-badge">IBDP Computer Science</span>
<span class="cs-badge">First Assessment 2027</span>
<span class="cs-badge">PASB Conversion</span>
</div>
</div>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# INFORMATION BOX
# ============================================================

st.markdown("""
<div class="cs-info">
<strong>How the calculator works:</strong>
Enter the student's marks and the total available marks.
The calculator converts the result into a percentage,
estimates the IB Grade using provisional reference
boundaries, and determines the corresponding PASB Grade.
You can add results to the student table and export
them as a CSV file.
<br><br>
<strong>Boundary reference:</strong>
Official 2027 assessment structure with provisional
percentage thresholds calculated from the average
of May 2025 TZ2 and TZ3 grade boundaries.
These estimates are not official 2027 IB boundaries.
</div>
""", unsafe_allow_html=True)


# ============================================================
# ASSESSMENT SETUP
# ============================================================

st.subheader("Assessment Setup")

mode = st.radio(
    "Calculation Mode",
    [
        "Single Assessment",
        "Final IB Grade"
    ],
    horizontal=True
)

level = st.selectbox(
    "IB Level",
    ["HL", "SL"]
)


# ============================================================
# SINGLE ASSESSMENT MODE
# ============================================================

if mode == "Single Assessment":

    st.divider()

    name = st.text_input(
        "Student Name",
        placeholder="Enter student name"
    )

    assessment = st.selectbox(
        "Assessment Component",
        ["Paper 1", "Paper 2", "IA"],
        format_func=lambda x: (
            "Internal Assessment (IA)"
            if x == "IA"
            else x
        )
    )

    official_max = MAX_MARKS_2027[level][assessment]

    st.caption(
        f"Official 2027 maximum: {official_max} marks."
    )

    col1, col2 = st.columns(2)

    with col1:
        score = st.number_input(
            "Student Marks",
            min_value=0.0,
            value=0.0,
            step=0.5
        )

    with col2:
        total = st.number_input(
            "Total Marks Possible",
            min_value=0.5,
            value=float(official_max),
            step=0.5
        )

    if st.button(
        "Calculate and Add Student",
        type="primary",
        use_container_width=True
    ):

        if not name.strip():

            st.error(
                "Please enter the student's name."
            )

        else:

            try:

                result = calculate_result(
                    name.strip(),
                    level,
                    assessment,
                    score,
                    total
                )

                st.session_state.cs_registros.append(
                    result
                )

                st.session_state.cs_ultimo_resultado = (
                    result
                )

                st.success(
                    f"{name.strip()} was added to the grade table."
                )

            except ValueError as error:
                st.error(str(error))


# ============================================================
# FINAL IB GRADE MODE
# ============================================================

else:

    st.divider()

    name = st.text_input(
        "Student Name",
        placeholder="Enter student name"
    )

    st.subheader(f"{level} Component Results")

    weights = WEIGHTS_2027[level]

    st.info(
        f"2027 {level} Weighting: "
        f"Paper 1 = {weights['Paper 1']:.0%} · "
        f"Paper 2 = {weights['Paper 2']:.0%} · "
        f"IA = {weights['IA']:.0%}"
    )

    p1 = st.number_input(
        "Paper 1 (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.5
    )

    p2 = st.number_input(
        "Paper 2 (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.5
    )

    ia = st.number_input(
        "Internal Assessment (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.5
    )

    if st.button(
        "Calculate and Add Student",
        type="primary",
        use_container_width=True
    ):

        if not name.strip():

            st.error(
                "Please enter the student's name."
            )

        else:

            try:

                result = calculate_final_result(
                    name.strip(),
                    level,
                    p1,
                    p2,
                    ia
                )

                st.session_state.cs_registros.append(
                    result
                )

                st.session_state.cs_ultimo_resultado = (
                    result
                )

                st.success(
                    f"{name.strip()}'s final grade was added."
                )

            except ValueError as error:
                st.error(str(error))


# ============================================================
# LAST RESULT
# ============================================================

if st.session_state.cs_ultimo_resultado is not None:

    display_result(
        st.session_state.cs_ultimo_resultado
    )


# ============================================================
# STUDENT GRADE TABLE
# ============================================================

st.divider()

st.subheader("Student Grade Table")

if st.session_state.cs_registros:

    df = pd.DataFrame(
        st.session_state.cs_registros
    )

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True
    )

    st.caption(
        f"Total records: {len(df)}"
    )

    # --------------------------------------------------------
    # CSV EXPORT
    # --------------------------------------------------------

    csv_data = df.to_csv(
        index=False,
        sep=";",
        decimal=","
    ).encode("utf-8-sig")

    st.download_button(
        label="Download Grade Table (CSV / Excel)",
        data=csv_data,
        file_name="ibdp_computer_science_grades.csv",
        mime="text/csv",
        use_container_width=True
    )

    # --------------------------------------------------------
    # TABLE CONTROLS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Remove Last Record",
            use_container_width=True
        ):

            st.session_state.cs_registros.pop()

            st.session_state.cs_ultimo_resultado = None

            st.rerun()

    with col2:

        if st.button(
            "Clear Grade Table",
            use_container_width=True
        ):

            st.session_state.cs_registros = []

            st.session_state.cs_ultimo_resultado = None

            st.rerun()

else:

    st.info(
        "No student records yet. Enter student details "
        "and click 'Calculate and Add Student'."
    )


# ============================================================
# PROVISIONAL BOUNDARY TABLE
# ============================================================

with st.expander(
    "View Provisional IB Grade Boundaries"
):

    selected_component = st.selectbox(
        "Component for boundary reference",
        [
            "Paper 1",
            "Paper 2",
            "IA",
            "Final Grade"
        ],
        key="boundary_component",
        format_func=lambda x: (
            "Internal Assessment (IA)"
            if x == "IA"
            else x
        )
    )

    if selected_component == "Final Grade":

        boundaries = build_final_boundaries(level)

    else:

        boundaries = build_component_boundaries(
            level,
            selected_component
        )

    rows = []

    for low, high, grade in reversed(boundaries):

        pasb_low, pasb_high = PASB_RANGES[grade]

        rows.append({
            "IB Grade": grade,
            "Provisional Boundary (%)": (
                f"{low:.2f}–{high:.2f}"
            ),
            "PASB Range": f"{pasb_low}–{pasb_high}"
        })

    st.dataframe(
        pd.DataFrame(rows),
        hide_index=True,
        use_container_width=True
    )

    st.caption(
        "These boundaries are provisional percentage "
        "thresholds based on May 2025 averages, "
        "not official 2027 IB grade boundaries. "
        "Upper thresholds belong to the next grade, "
        "except at 100%."
    )


# ============================================================
# IMPORTANT NOTICES
# ============================================================

st.warning(
    "Student records are stored only during the active "
    "Streamlit session. Download the CSV file before "
    "closing or restarting the session."
)

st.caption(
    "PASB conversion uses linear interpolation within "
    "each IB grade's school percentage range. "
    "This is a calculator convention, not an "
    "official IB conversion formula."
)


# ============================================================
# FOOTER WITH IB WORLD SCHOOL LOGO
# ============================================================

st.divider()

if ib_logo_base64:

    st.markdown(
        f"""
<div style="text-align:center; margin:25px 0 15px 0;">
<img
src="data:image/png;base64,{ib_logo_base64}"
alt="IB World School Logo"
style="width:220px; max-width:75%; height:auto; object-fit:contain;"
>
</div>
""",
        unsafe_allow_html=True
    )

st.markdown("""
<div class="cs-footer">
PASB · IBDP Computer Science · First Assessment 2027
<br>
© 2026 Gracielle Dias. All rights reserved.
</div>
""", unsafe_allow_html=True)


# ============================================================
# IMAGE FILE CHECK
# ============================================================

if not PASB_LOGO.exists() or not IB_LOGO.exists():

    missing_files = []

    if not PASB_LOGO.exists():
        missing_files.append(PASB_LOGO.name)

    if not IB_LOGO.exists():
        missing_files.append(IB_LOGO.name)

    st.warning(
        "The following image files were not found: "
        + ", ".join(missing_files)
    )
