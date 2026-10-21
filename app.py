import streamlit as st
import pandas as pd

st.set_page_config(page_title="IBDP Computer Science Grade Converter – Mrs Graci", layout="centered")

import streamlit as st
import math

# ============================================================
# PASB EQUIVALENCE
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
# MAY 2025 IB COMPUTER SCIENCE GRADE BOUNDARIES
# ============================================================

BOUNDARIES = {

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

        "Paper 3": [
            (0, 3, 1),
            (4, 7, 2),
            (8, 10, 3),
            (11, 13, 4),
            (14, 17, 5),
            (18, 20, 6),
            (21, 30, 7),
        ],

        "Solution": [
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

        "Paper 3": [
            (0, 5, 1),
            (6, 11, 2),
            (12, 14, 3),
            (15, 16, 4),
            (17, 18, 5),
            (19, 20, 6),
            (21, 30, 7),
        ],

        "Solution": [
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

        "Solution": [
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

        "Solution": [
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
# MAXIMUM MARKS
# ============================================================

MAX_MARKS = {

    "HL": {
        "Paper 1": 100,
        "Paper 2": 65,
        "Paper 3": 30,
        "Solution": 34,
        "Final Grade": 100,
    },

    "SL": {
        "Paper 1": 70,
        "Paper 2": 45,
        "Solution": 34,
        "Final Grade": 100,
    }
}


# ============================================================
# FUNCTIONS
# ============================================================

def round_half_up(value):
    """
    Rounds .5 upward instead of using Python's banker's rounding.
    Example:
    54.4 -> 54
    54.5 -> 55
    54.6 -> 55
    """
    return math.floor(value + 0.5)


def get_grade(level, timezone, assessment, mark):
    """
    Returns IB grade and its boundary.
    """

    boundaries = BOUNDARIES[(level, timezone)][assessment]

    for low, high, grade in boundaries:
        if low <= mark <= high:
            return grade, low, high

    return None, None, None


def calculate_pasb_value(mark, low, high, grade):
    """
    Linear interpolation inside the corresponding PASB band.
    """

    pasb_low, pasb_high = PASB_RANGES[grade]

    if high == low:
        return pasb_low

    relative_position = (mark - low) / (high - low)

    pasb_value = (
        pasb_low
        + relative_position * (pasb_high - pasb_low)
    )

    return pasb_value


def calculate_ib_grade(
    level,
    timezone,
    assessment,
    student_score,
    total_score
):

    max_ib_marks = MAX_MARKS[level][assessment]

    # Percentage obtained in the classroom assessment
    percentage = student_score / total_score

    # Scale to official IB component maximum
    raw_ib_mark = percentage * max_ib_marks

    # IB boundaries use whole marks
    ib_mark = round_half_up(raw_ib_mark)

    # Prevent values above maximum
    ib_mark = min(ib_mark, max_ib_marks)

    grade, low, high = get_grade(
        level,
        timezone,
        assessment,
        ib_mark
    )

    if grade is None:
        return None

    pasb_low, pasb_high = PASB_RANGES[grade]

    pasb_value = calculate_pasb_value(
        ib_mark,
        low,
        high,
        grade
    )

    return {
        "percentage": percentage * 100,
        "raw_ib_mark": raw_ib_mark,
        "ib_mark": ib_mark,
        "ib_grade": grade,
        "ib_boundary": f"{low}–{high}",
        "pasb_range": f"{pasb_low}–{pasb_high}",
        "pasb_grade": round(pasb_value),
        "pasb_exact": pasb_value
    }


# ============================================================
# PAGE
# ============================================================

st.title("IBDP Computer Science Grade Converter")

st.caption(
    "May 2025 Computer Science grade boundaries – "
    "PASB equivalence calculator"
)

mode = st.radio(
    "Mode",
    ["Student Assessment", "Final Grade"]
)

level = st.selectbox(
    "IB Level",
    ["HL", "SL"]
)

timezone = st.selectbox(
    "Examination Timezone",
    ["Timezone 2", "Timezone 3"]
)


# ============================================================
# STUDENT ASSESSMENT MODE
# ============================================================

if mode == "Student Assessment":

    if level == "HL":
        assessment_options = [
            "Paper 1",
            "Paper 2",
            "Paper 3",
            "Solution"
        ]
    else:
        assessment_options = [
            "Paper 1",
            "Paper 2",
            "Solution"
        ]

    assessment = st.selectbox(
        "Assessment",
        assessment_options
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

    if st.button("Calculate"):

        if score > total:
            st.error(
                "Student marks cannot be higher than total marks."
            )

        else:

            result = calculate_ib_grade(
                level,
                timezone,
                assessment,
                score,
                total
            )

            if result:

                st.divider()

                st.subheader("Result")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Assessment %",
                        f"{result['percentage']:.1f}%"
                    )

                with col2:
                    st.metric(
                        "IB Grade",
                        result["ib_grade"]
                    )

                with col3:
                    st.metric(
                        "PASB Grade",
                        result["pasb_grade"]
                    )

                st.write(
                    f"**Equivalent IB mark:** "
                    f"{result['ib_mark']} marks"
                )

                st.write(
                    f"**IB boundary:** "
                    f"{result['ib_boundary']}"
                )

                st.write(
                    f"**PASB range:** "
                    f"{result['pasb_range']}"
                )

                st.write(
                    f"**Exact PASB conversion:** "
                    f"{result['pasb_exact']:.2f}"
                )


# ============================================================
# FINAL GRADE MODE
# ============================================================

else:

    st.subheader("Component Results")

    if level == "HL":

        p1 = st.number_input(
            "Paper 1 (%)",
            0.0,
            100.0,
            0.0
        )

        p2 = st.number_input(
            "Paper 2 (%)",
            0.0,
            100.0,
            0.0
        )

        p3 = st.number_input(
            "Paper 3 (%)",
            0.0,
            100.0,
            0.0
        )

        ia = st.number_input(
            "Solution / IA (%)",
            0.0,
            100.0,
            0.0
        )

        # Old HL weighting
        final_percentage = (
            p1 * 0.40
            + p2 * 0.20
            + p3 * 0.20
            + ia * 0.20
        )

    else:

        p1 = st.number_input(
            "Paper 1 (%)",
            0.0,
            100.0,
            0.0
        )

        p2 = st.number_input(
            "Paper 2 (%)",
            0.0,
            100.0,
            0.0
        )

        ia = st.number_input(
            "Solution / IA (%)",
            0.0,
            100.0,
            0.0
        )

        # Old SL weighting
        final_percentage = (
            p1 * 0.45
            + p2 * 0.25
            + ia * 0.30
        )

    if st.button("Calculate Final Grade"):

        final_mark = round_half_up(final_percentage)

        grade, low, high = get_grade(
            level,
            timezone,
            "Final Grade",
            final_mark
        )

        pasb_low, pasb_high = PASB_RANGES[grade]

        pasb_value = calculate_pasb_value(
            final_mark,
            low,
            high,
            grade
        )

        st.divider()

        st.subheader("Final Result")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Weighted IB %",
                f"{final_percentage:.1f}%"
            )

        with col2:
            st.metric(
                "IB Grade",
                grade
            )

        with col3:
            st.metric(
                "PASB Grade",
                round(pasb_value)
            )

        st.write(
            f"**IB Final Grade boundary:** {low}–{high}"
        )

        st.write(
            f"**PASB range:** {pasb_low}–{pasb_high}"
        )

        st.write(
            f"**Exact PASB conversion:** {pasb_value:.2f}"
        )
