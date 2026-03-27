import pandas as pd
import streamlit as st

from utils.ui import render_method_intro


def _render_round(title: str, rows: list[dict], note: str | None = None):
    st.markdown(f"**{title}**")
    df = pd.DataFrame(rows)
    st.dataframe(df, hide_index=True, use_container_width=True)
    if note:
        st.caption(note)


def render():
    render_method_intro(
        "Instant Runoff",
        "Voters rank the candidates. Each round, the last place candidate is removed. Their votes move to the next choice until someone gets over 50%.",
        "Ranking a candidate higher can sometimes make them lose.",
        "Compare the two cases. Darrow gets extra support, but this changes who is removed first and affects the final winner.",
    )

    st.divider()
    st.markdown("### Compare The Two Cases")
    st.warning(
        "**Contradiction to notice**: When Mamoru perform worse in first round, he wins!"
    )
    st.markdown(
        "**Scenario**: The candidates are Molly, Darrow, and Mamoru. Molly and Mamoru have very conflicting views, while Darrow is moderate."
    )
    left, separator, right = st.columns([1, 0.05, 1])

    with left:
        with st.container(border=True):
            st.markdown("#### Case 1")
        _render_round(
            "First round",
            [
                {"Candidate": "Mamoru", "Votes (%)": "45%"},
                {"Candidate": "Darrow", "Votes (%)": "30%"},
                {"Candidate": "Molly", "Votes (%)": "25%"},
            ],
        )
        st.markdown("**Elimination:** Molly is removed first.")
        st.caption(
            "Because of their conflicting views, Molly's supporters prefer Darrow over Mamoru, so their ballots all move to Darrow."
        )
        _render_round(
            "Second round",
            [
                {"Candidate": "Darrow", "Votes (%)": "30% + 25% = 55%"},
                {"Candidate": "Mamoru", "Votes (%)": "45%"},
            ],
        )
        st.success("Darrow wins because Molly is eliminated before him.")

    with right:
        with st.container(border=True):
            st.markdown("#### Case 2")
            st.markdown(
                "Let's say that Mamoru's campaign speech goes horribly wrong, making 6% of his voters choose Molly instead."
            )
        _render_round(
            "First round",
            [
                {"Candidate": "Mamoru", "Votes (%)": "45% - 6% = 39%"},
                {"Candidate": "Molly", "Votes (%)": "25% + 6% = 31%"},
                {"Candidate": "Darrow", "Votes (%)": "30%"},
            ],
        )
        st.markdown("**Elimination:** Darrow is now removed first.")
        st.caption(
            "Because Darrow's supporters are moderate, their second choices split evenly between Mamoru and Molly."
        )
        _render_round(
            "Second round",
            [
                {"Candidate": "Mamoru", "Votes (%)": "39% + (30% / 2) = 54%"},
                {"Candidate": "Molly", "Votes (%)": "31% + (30% / 2) = 46%"},
            ],
        )
        st.error(
            "Mamoru wins. Doing worse in the first round changes the elimination order and turns the final result upside down. Compare this to Case 1."
        )
