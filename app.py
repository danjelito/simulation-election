import streamlit as st

from methods import borda, condorcet, fptp, irv, runoff

st.set_page_config(
    page_title="Voting Systems Simulator",
    page_icon="🗳️",
    layout="centered",
)

st.markdown(
    """
    <style>
    div[data-testid="stMetric"] {
        background: rgba(245, 247, 242, 0.9);
        border: 1px solid rgba(35, 52, 39, 0.12);
        border-radius: 0.9rem;
        padding: 0.75rem;
    }
    div[data-testid="stVerticalBlock"] div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"] div[data-testid="stDataFrame"] {
        border-radius: 0.75rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🗳️ Voting Systems Simulator")
with st.container(border=True):
    st.markdown(
        "This simulator compares five voting systems and shows how each one can produce a result that feels mathematically or politically unsatisfying."
    )
    st.markdown(
        "Open a tab, read the short scenario prompt, then change the inputs to see how the winner or paradox shifts."
    )
    st.caption(
        'Inspired by the Veritasium video "[Why Democracy Is Mathematically Impossible](https://www.youtube.com/watch?v=qf7ws2DF-zk)." Each tab focuses on one different failure mode.'
    )
    st.caption(
        "Methodology and related work: [https://danjelito.github.io](https://danjelito.github.io)"
    )

tabs = st.tabs(
    [
        "First Past the Post",
        "50%+1 Runoff",
        "Instant Runoff",
        "Borda Count",
        "Condorcet Method",
    ]
)

with tabs[0]:
    fptp.render()

with tabs[1]:
    runoff.render()

with tabs[2]:
    irv.render()

with tabs[3]:
    borda.render()

with tabs[4]:
    condorcet.render()
