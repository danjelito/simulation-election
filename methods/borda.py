import pandas as pd
import streamlit as st

from utils.ui import render_method_intro


def _render_case_table(rows: list[dict]):
    df = pd.DataFrame(rows)
    st.dataframe(df, hide_index=True, use_container_width=True)


def render():
    render_method_intro(
        "Borda Count",
        "Voters rank all candidates. First place gets the most points, last place gets the fewest, and the highest total score wins.",
        "Borda Count can violate independence of irrelevant alternatives: a weak extra candidate can change which strong candidate wins.",
        "Compare the two cases and watch candidate C. C never wins, but C still changes the point totals enough to flip A and B.",
    )

    st.divider()
    st.markdown("### Compare The Two Cases")
    st.warning(
        "**Key contradiction**: A beats B when there are only two options, but B beats A once a non-winning candidate C is added."
    )

    left, right = st.columns(2)

    with left:
        with st.container(border=True):
            st.markdown("#### Case 1: Only A and B")
            _render_case_table(
                [
                    {"Voter": "V1", "Ranking": "A > B", "Points awarded": "A=1, B=0"},
                    {"Voter": "V2", "Ranking": "A > B", "Points awarded": "A=1, B=0"},
                    {"Voter": "V3", "Ranking": "A > B", "Points awarded": "A=1, B=0"},
                    {"Voter": "V4", "Ranking": "A > B", "Points awarded": "A=1, B=0"},
                    {"Voter": "V5", "Ranking": "A > B", "Points awarded": "A=1, B=0"},
                    {"Voter": "V6", "Ranking": "A > B", "Points awarded": "A=1, B=0"},
                    {"Voter": "V7", "Ranking": "B > A", "Points awarded": "B=1, A=0"},
                    {"Voter": "V8", "Ranking": "B > A", "Points awarded": "B=1, A=0"},
                    {"Voter": "V9", "Ranking": "B > A", "Points awarded": "B=1, A=0"},
                    {"Voter": "V10", "Ranking": "B > A", "Points awarded": "B=1, A=0"},
                ]
            )
        st.markdown("**Points (1st = 1 pt, 2nd = 0 pts)**")
        st.markdown("A: 6×1 + 4×0 = 6 pts")
        st.markdown("B: 4×1 + 6×0 = 4 pts")
        st.success("A wins, which matches the fact that 60% of voters prefer A over B.")

    with right:
        with st.container(border=True):
            st.markdown("#### Case 2: Add candidate C")
            st.caption("C does not win, but C changes where the middle-rank points go.")
        _render_case_table(
            [
                {
                    "Voter": "V1",
                    "Ranking": "A > B > C",
                    "Points awarded": "A=2, B=1, C=0",
                },
                {
                    "Voter": "V2",
                    "Ranking": "A > B > C",
                    "Points awarded": "A=2, B=1, C=0",
                },
                {
                    "Voter": "V3",
                    "Ranking": "A > B > C",
                    "Points awarded": "A=2, B=1, C=0",
                },
                {
                    "Voter": "V4",
                    "Ranking": "A > B > C",
                    "Points awarded": "A=2, B=1, C=0",
                },
                {
                    "Voter": "V5",
                    "Ranking": "A > B > C",
                    "Points awarded": "A=2, B=1, C=0",
                },
                {
                    "Voter": "V6",
                    "Ranking": "A > B > C",
                    "Points awarded": "A=2, B=1, C=0",
                },
                {
                    "Voter": "V7",
                    "Ranking": "B > C > A",
                    "Points awarded": "B=2, C=1, A=0",
                },
                {
                    "Voter": "V8",
                    "Ranking": "B > C > A",
                    "Points awarded": "B=2, C=1, A=0",
                },
                {
                    "Voter": "V9",
                    "Ranking": "B > C > A",
                    "Points awarded": "B=2, C=1, A=0",
                },
                {
                    "Voter": "V10",
                    "Ranking": "B > C > A",
                    "Points awarded": "B=2, C=1, A=0",
                },
            ]
        )
        st.markdown("**Points (1st = 2 pts, 2nd = 1 pt, 3rd = 0 pts)**")
        st.markdown("A: (6×2) + (4×0) = 12 pts")
        st.markdown("B: (6×1) + (4×2) = 6 + 8 = 14 pts")
        st.markdown("C: (6×0) + (4×1) = 4 pts")
        st.error(
            "B now wins even though the same 60% voters still prefers A to B. Candidate C changed the scoring, not the underlying majority preference between A and B."
        )
