import streamlit as st
import math


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="IBDP Computer Science Grade Converter",
    page_icon="💻",
    layout="centered"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-header {
    background: linear-gradient(135deg, #18304f 0%, #294f78 100%);
    padding: 36px 42px;
    border-radius: 22px;
    margin-bottom: 24px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.18);
}

.header-kicker {
    color: #b9cbe0;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.3px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.header-title {
    color: white;
    font-size: 42px;
    font-weight: 750;
    line-height: 1.15;
    margin-bottom: 14px;
}

.header-subtitle {
    color: #dce7f4;
    font-size: 17px;
    line-height: 1.5;
    margin-bottom: 18px;
    max-width: 800px;
}

.badge-container {
    margin-top: 16px;
}

.badge {
    display: inline-block;
    background-color: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.22);
    color: white;
    padding: 7px 14px;
    border-radius: 20px;
    margin-right: 8px;
    margin-bottom: 6px;
    font-size: 13px;
    font-weight: 600;
}

.info-box {
    background-color: #edf3f8;
    border-left: 5px solid #294f78;
    padding: 17px 20px;
    border-radius: 10px;
    margin-bottom: 25px;
    color: #1d2d3e;
    font-size: 15px;
    line-height: 1.55;
}

.info-box strong {
    color: #18304f;
}

.result-box {
    background-color: rgba(237, 243, 248, 0.08);
    border: 1px solid rgba(120, 145, 170, 0.35);
    border-radius: 14px;
    padding: 18px 20px;
    margin-top: 18px;
    margin-bottom: 18px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div class="main-header">
<div class="header-kicker">PASB • Assessment • Mrs. Graci Dias Tool</div>
<div class="header-title">IBDP Computer Science<br>Grade Converter</div>
<div class="header-subtitle">
Convert assessment performance into an estimated IB grade
and PASB equivalent using the 2027 assessment structure.
</div>

<div class="badge-container">
<span class="badge">IBDP Computer Science</span>
<span class="badge">First Assessment 2027</span>
<span class="badge">PASB Conversion</span>
</div>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# INFORMATION BOX
# ============================================================

st.markdown(
    """
<div class="info-box">
<strong>Boundary reference:</strong>
This calculator uses the official 2027 assessment structure.
Because official 2027 grade boundaries are not yet available,
May 2025 Computer Science boundaries are used as a provisional
percentage-based reference. The provisional thresholds are based
on the average of the available 2025 TZ2 and TZ3 boundaries.
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
# 2025 SOURCE BOUNDARIES
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
# OLD 2025 COMPONENT MAXIMUMS
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


def get_grade_lower_boundary(boundaries, grade):
    for low, high, g in boundaries:
        if g == grade:
            return low
    return None


def build_average_percentage_boundaries(level, assessment):
    """
    Builds provisional percentage boundaries using the average
    of the 2025 TZ2 and TZ3 lower thresholds.
    """

    max_old = REFERENCE_MAX_MARKS[level][assessment]

    tz2 = BOUNDARIES_2025[level]["TZ2"][assessment]
    tz3 = BOUNDARIES_2025[level]["TZ3"][assessment]

    lower_thresholds = {}

    for grade in range(1, 8):

        tz2_low = get_grade_lower_boundary(
            tz2,
            grade
        )

        tz3_low = get_grade_lower_boundary(
            tz3,
            grade
        )

        tz2_percentage = (
            tz2_low / max_old
        ) * 100

        tz3_percentage = (
            tz3_low / max_old
        ) * 100

        average_percentage = (
            tz2_percentage
            + tz3_percentage
        ) / 2

        lower_thresholds[grade] = (
            average_percentage
        )

    boundaries = []

    for grade in range(1, 8):

        low = lower_thresholds[grade]

        if grade < 7:
            high = lower_thresholds[grade + 1]
        else:
            high = 100.0

        boundaries.append(
            (low, high, grade)
        )

    return boundaries


def build_average_final_boundaries(level):
    """
    Builds provisional final-grade boundaries using the average
    of TZ2 and TZ3 lower thresholds.
    """

    tz2 = BOUNDARIES_2025[level]["TZ2"]["Final Grade"]
    tz3 = BOUNDARIES_2025[level]["TZ3"]["Final Grade"]

    lower_thresholds = {}

    for grade in range(1, 8):

        tz2_low = get_grade_lower_boundary(
            tz2,
            grade
        )

        tz3_low = get_grade_lower_boundary(
            tz3,
            grade
        )

        average = (
            tz2_low + tz3_low
        ) / 2

        lower_thresholds[grade] = average

    boundaries = []

    for grade in range(1, 8):

        low = lower_thresholds[grade]

        if grade < 7:
            high = lower_thresholds[grade + 1]
        else:
            high = 100.0

        boundaries.append(
            (low, high, grade)
        )

    return boundaries


def get_estimated_grade(level, assessment, percentage):
    """
    Determines provisional IB grade based on averaged
    2025 percentage thresholds.
    """

    boundaries = build_average_percentage_boundaries(
        level,
        assessment
    )

    for low, high, grade in boundaries:

        if grade < 7:

            if low <= percentage < high:
                return grade, low, high

        else:

            if low <= percentage <= 100:
                return grade, low, high

    return None, None, None


def get_estimated_final_grade(level, percentage):

    boundaries = build_average_final_boundaries(
        level
    )

    for low, high, grade in boundaries:

        if grade < 7:

            if low <= percentage < high:
                return grade, low, high

        else:

            if low <= percentage <= 100:
                return grade, low, high

    return None, None, None


def calculate_pasb(
    value,
    grade,
    lower_boundary,
    upper_boundary
):
    """
    Linear interpolation inside PASB band.
    """

    pasb_low, pasb_high = (
        PASB_RANGES[grade]
    )

    if upper_boundary == lower_boundary:
        return float(pasb_low)

    position = (
        value - lower_boundary
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
# ASSESSMENT SETUP
# ============================================================

st.subheader("Assessment Setup")

mode = st.radio(
    "Choose calculation mode",
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

    official_max = (
        MAX_MARKS_2027[level][assessment]
    )

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
        "Calculate Grade",
        use_container_width=True
    ):

        if score > total:

            st.error(
                "Student marks cannot be greater than "
                "the total marks possible."
            )

        else:

            # ------------------------------------------------
            # RAW PERCENTAGE
            # ------------------------------------------------

            percentage = (
                score / total
            ) * 100

            # ------------------------------------------------
            # EQUIVALENT 2027 RAW MARK
            # ------------------------------------------------

            equivalent_mark = (
                percentage / 100
            ) * official_max

            # ------------------------------------------------
            # ESTIMATED IB GRADE
            # ------------------------------------------------

            (
                grade,
                boundary_low,
                boundary_high
            ) = get_estimated_grade(
                level,
                assessment,
                percentage
            )

            if grade is None:

                st.error(
                    "Unable to determine the estimated IB grade."
                )

            else:

                # --------------------------------------------
                # PASB CONVERSION
                # --------------------------------------------

                pasb = calculate_pasb(
                    percentage,
                    grade,
                    boundary_low,
                    boundary_high
                )

                pasb_rounded = (
                    round_half_up(pasb)
                )

                pasb_low, pasb_high = (
                    PASB_RANGES[grade]
                )

                # --------------------------------------------
                # RESULTS
                # --------------------------------------------

                st.divider()

                st.subheader(
                    "Assessment Result"
                )

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

                st.markdown(
                    f"""
<div class="result-box">

<strong>Equivalent 2027 {assessment} mark:</strong>
{equivalent_mark:.1f}/{official_max}
<br><br>

<strong>Estimated IB Grade:</strong>
{grade}
<br><br>

<strong>Provisional reference boundary:</strong>
{boundary_low:.1f}% – {boundary_high:.1f}%
<br><br>

<strong>PASB band:</strong>
{pasb_low}–{pasb_high}
<br><br>

<strong>Exact PASB conversion:</strong>
{pasb:.2f}

</div>
""",
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
            "2027 HL weighting: "
            "Paper 1 = 40% · "
            "Paper 2 = 40% · "
            "IA = 20%"
        )

    else:

        st.info(
            "2027 SL weighting: "
            "Paper 1 = 35% · "
            "Paper 2 = 35% · "
            "IA = 30%"
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
        "Calculate Final Grade",
        use_container_width=True
    ):

        weights = (
            WEIGHTS_2027[level]
        )

        # ----------------------------------------------------
        # WEIGHTED FINAL RESULT
        # ----------------------------------------------------

        final_percentage = (
            p1 * weights["Paper 1"]
            + p2 * weights["Paper 2"]
            + ia * weights["IA"]
        )

        # ----------------------------------------------------
        # ESTIMATED FINAL IB GRADE
        # ----------------------------------------------------

        (
            final_grade,
            final_low,
            final_high
        ) = get_estimated_final_grade(
            level,
            final_percentage
        )

        if final_grade is None:

            st.error(
                "Unable to determine the estimated final IB grade."
            )

        else:

            # ------------------------------------------------
            # PASB CONVERSION
            # ------------------------------------------------

            pasb = calculate_pasb(
                final_percentage,
                final_grade,
                final_low,
                final_high
            )

            pasb_rounded = (
                round_half_up(pasb)
            )

            pasb_low, pasb_high = (
                PASB_RANGES[final_grade]
            )

            # ------------------------------------------------
            # RESULTS
            # ------------------------------------------------

            st.divider()

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

            st.markdown(
                f"""
<div class="result-box">

<strong>Weighted result:</strong>
{final_percentage:.2f}%
<br><br>

<strong>Estimated IB Grade:</strong>
{final_grade}
<br><br>

<strong>Provisional final boundary:</strong>
{final_low:.1f}% – {final_high:.1f}%
<br><br>

<strong>PASB band:</strong>
{pasb_low}–{pasb_high}
<br><br>

<strong>Exact PASB conversion:</strong>
{pasb:.2f}

</div>
""",
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
    "IB grade estimates are provisional. "
    "May 2025 boundaries are used as a percentage-based reference "
    "until official 2027 boundaries are published."
)
