import streamlit as st
import math

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="IBDP Computer Science Grade Converter - Mrs. Graci",
    page_icon="💻",
    layout="centered"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-header {
        background: linear-gradient(135deg, #162A46 0%, #294D73 100%);
        padding: 2rem 2rem 1.7rem 2rem;
        border-radius: 18px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }

    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
    }

    .main-header p {
        color: #DCE6F2;
        margin-top: 0.6rem;
        margin-bottom: 0;
        font-size: 1rem;
    }

    .badge {
        display: inline-block;
        background-color: rgba(255,255,255,0.16);
        color: white;
        padding: 0.3rem 0.7rem;
        border-radius: 20px;
        margin-right: 0.4rem;
        margin-top: 0.8rem;
        font-size: 0.82rem;
    }

    .info-box {
        background-color: #F2F6FA;
        border-left: 5px solid #294D73;
        padding: 1rem 1.2rem;
        border-radius: 8px;
        margin-bottom: 1.3rem;
    }

    .result-box {
        background-color: #F7F9FC;
        border: 1px solid #DCE3EB;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-top: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="main-header">
        <h1>💻 IBDP Computer Science Grade Converter</h1>

        <p>
        Convert assessment performance into an estimated IB grade
        and PASB equivalent using the 2027 assessment structure.
        </p>

        <span class="badge">IBDP Computer Science</span>
        <span class="badge">First Assessment 2027</span>
        <span class="badge">PASB Conversion</span>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="info-box">
        <b>Boundary reference:</b> This calculator uses the official
        2027 assessment structure. Since official 2027 grade boundaries
        are not yet available, the May 2025 boundaries are used as a
        proportional reference for estimation.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PASB RANGES
# ============================================================

PASB_RANGES = {
    1: (30, 49),
    2: (50, 59),
    3: (60, 69),
    4: (70, 79),
    5: (80, 89),
    6: (90, 95),
    7: (96, 100),
}


# ============================================================
# 2025 REFERENCE BOUNDARIES
# ============================================================
#
# These are the boundaries supplied from the 2025 session.
#
# They are NOT official 2027 boundaries.
#
# They are used proportionally to estimate equivalent grade bands
# under the new 2027 component structure.
#
# ============================================================

REFERENCE_BOUNDARIES = {

    # --------------------------------------------------------
    # HL - TIMEZONE 2
    # --------------------------------------------------------

    ("HL", "Timezone 2"): {

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


    # --------------------------------------------------------
    # HL - TIMEZONE 3
    # --------------------------------------------------------

    ("HL", "Timezone 3"): {

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


    # --------------------------------------------------------
    # SL - TIMEZONE 2
    # --------------------------------------------------------

    ("SL", "Timezone 2"): {

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


    # --------------------------------------------------------
    # SL - TIMEZONE 3
    # --------------------------------------------------------

    ("SL", "Timezone 3"): {

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
}


# ============================================================
# 2025 COMPONENT MAXIMUMS
# Used only to convert old boundaries into percentages
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
    }
}


# ============================================================
# OFFICIAL 2027 STRUCTURE
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
    }
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
    }
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def round_half_up(number):
    return math.floor(number + 0.5)


def get_reference_grade(level, timezone, assessment, percentage):

    boundaries = REFERENCE_BOUNDARIES[
        (level, timezone)
    ][assessment]

    reference_max = REFERENCE_MAX_MARKS[level][assessment]

    reference_mark = percentage * reference_max / 100

    for low, high, grade in boundaries:

        if low <= reference_mark <= high + 0.999999:

            low_percentage = (
                low / reference_max
            ) * 100

            high_percentage = (
                high / reference_max
            ) * 100

            return (
                grade,
                low_percentage,
                high_percentage
            )

    return None, None, None


def get_final_grade(level, timezone, percentage):

    boundaries = REFERENCE_BOUNDARIES[
        (level, timezone)
    ]["Final Grade"]

    for low, high, grade in boundaries:

        if low <= percentage <= high + 0.999999:

            return grade, low, high

    return None, None, None


def calculate_pasb(
    percentage,
    grade,
    lower_boundary,
    upper_boundary
):

    pasb_low, pasb_high = PASB_RANGES[grade]

    if upper_boundary == lower_boundary:
        return float(pasb_low)

    position = (
        percentage - lower_boundary
    ) / (
        upper_boundary - lower_boundary
    )

    position = max(
        0,
        min(position, 1)
    )

    return (
        pasb_low
        + position
        * (pasb_high - pasb_low)
    )


# ============================================================
# MODE
# ============================================================

st.subheader("Assessment setup")

mode = st.radio(
    "Choose calculation mode",
    [
        "Single Assessment",
        "Final IB Grade"
    ],
    horizontal=True
)

col1, col2 = st.columns(2)

with col1:

    level = st.selectbox(
        "IB Level",
        ["HL", "SL"]
    )

with col2:

    timezone = st.selectbox(
        "Boundary Reference",
        ["Timezone 2", "Timezone 3"]
    )


# ============================================================
# SINGLE ASSESSMENT
# ============================================================

if mode == "Single Assessment":

    st.divider()

    assessment = st.selectbox(
        "Assessment Component",
        [
            "Paper 1",
            "Paper 2",
            "IA"
        ]
    )

    official_max = MAX_MARKS_2027[
        level
    ][assessment]

    st.caption(
        f"Official 2027 maximum for {assessment}: "
        f"{official_max} marks."
    )

    col1, col2 = st.columns(2)

    with col1:

        score = st.number_input(
            "Student marks",
            min_value=0.0,
            step=0.5
        )

    with col2:

        total = st.number_input(
            "Total marks possible",
            min_value=1.0,
            step=1.0
        )

    if st.button(
        "Calculate grade",
        use_container_width=True
    ):

        if score > total:

            st.error(
                "Student marks cannot be greater "
                "than the total marks possible."
            )

        else:

            percentage = (
                score / total
            ) * 100

            equivalent_mark = (
                percentage / 100
            ) * official_max

            equivalent_mark_rounded = (
                round_half_up(
                    equivalent_mark
                )
            )

            (
                grade,
                boundary_low,
                boundary_high
            ) = get_reference_grade(
                level,
                timezone,
                assessment,
                percentage
            )

            pasb = calculate_pasb(
                percentage,
                grade,
                boundary_low,
                boundary_high
            )

            pasb_rounded = round_half_up(
                pasb
            )

            st.markdown(
                """
                <div class="result-box">
                """,
                unsafe_allow_html=True
            )

            st.subheader("Assessment Result")

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "Raw Score",
                    f"{percentage:.1f}%"
                )

            with c2:

                st.metric(
                    "Estimated IB Grade",
                    grade
                )

            with c3:

                st.metric(
                    "PASB Grade",
                    pasb_rounded
                )

            st.write(
                f"**Equivalent 2027 {assessment} mark:** "
                f"{equivalent_mark:.1f}/{official_max}"
            )

            st.write(
                f"**Reference IB boundary:** "
                f"{boundary_low:.1f}% – "
                f"{boundary_high:.1f}%"
            )

            pasb_low, pasb_high = (
                PASB_RANGES[grade]
            )

            st.write(
                f"**PASB band:** "
                f"{pasb_low}–{pasb_high}"
            )

            st.write(
                f"**Exact PASB conversion:** "
                f"{pasb:.2f}"
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


# ============================================================
# FINAL IB GRADE
# ============================================================

else:

    st.divider()

    st.subheader(
        f"{level} Component Results"
    )

    st.caption(
        "Enter each component result as a percentage."
    )

    if level == "HL":

        st.info(
            "HL weighting: Paper 1 = 40% · "
            "Paper 2 = 40% · IA = 20%"
        )

    else:

        st.info(
            "SL weighting: Paper 1 = 35% · "
            "Paper 2 = 35% · IA = 30%"
        )

    p1 = st.number_input(
        "Paper 1 (%)",
        min_value=0.0,
        max_value=100.0,
        step=0.5
    )

    p2 = st.number_input(
        "Paper 2 (%)",
        min_value=0.0,
        max_value=100.0,
        step=0.5
    )

    ia = st.number_input(
        "Internal Assessment (%)",
        min_value=0.0,
        max_value=100.0,
        step=0.5
    )

    if st.button(
        "Calculate final grade",
        use_container_width=True
    ):

        weights = WEIGHTS_2027[level]

        final_percentage = (
            p1 * weights["Paper 1"]
            + p2 * weights["Paper 2"]
            + ia * weights["IA"]
        )

        (
            final_grade,
            final_low,
            final_high
        ) = get_final_grade(
            level,
            timezone,
            final_percentage
        )

        pasb = calculate_pasb(
            final_percentage,
            final_grade,
            final_low,
            final_high
        )

        pasb_rounded = (
            round_half_up(pasb)
        )

        st.markdown(
            """
            <div class="result-box">
            """,
            unsafe_allow_html=True
        )

        st.subheader(
            "Final Course Result"
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Weighted Result",
                f"{final_percentage:.1f}%"
            )

        with c2:

            st.metric(
                "Estimated IB Grade",
                final_grade
            )

        with c3:

            st.metric(
                "PASB Grade",
                pasb_rounded
            )

        st.write(
            f"**Reference final boundary:** "
            f"{final_low}–{final_high}%"
        )

        pasb_low, pasb_high = (
            PASB_RANGES[final_grade]
        )

        st.write(
            f"**PASB band:** "
            f"{pasb_low}–{pasb_high}"
        )

        st.write(
            f"**Exact PASB conversion:** "
            f"{pasb:.2f}"
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "PASB • IBDP Computer Science • "
    "2027 Assessment Structure"
)

st.caption(
    "Grade estimates are based on May 2025 boundary patterns "
    "and should not be interpreted as official 2027 IB grade boundaries."
)
