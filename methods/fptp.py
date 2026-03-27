import pandas as pd
import streamlit as st

from utils.state import init_defaults, reset_tab
from utils.ui import render_method_intro, render_vote_total

_KEY = "fptp"
_DEFAULTS = {
    "candidates": ["Molly", "Darrow", "Mamoru"],
    "votes": [40, 35, 25],
}


def _on_slider_change(changed_idx: int) -> None:
    """Keep all sliders summing to 100 by proportionally adjusting the others."""
    candidates = st.session_state[f"{_KEY}_candidates"]
    n = len(candidates)
    votes = list(st.session_state[f"{_KEY}_votes"])
    new_val = st.session_state[f"{_KEY}_slider_{changed_idx}"]

    remaining = 100 - new_val
    others = [j for j in range(n) if j != changed_idx]
    others_sum = sum(votes[j] for j in others)

    new_votes = list(votes)
    new_votes[changed_idx] = new_val

    if others_sum > 0:
        for j in others:
            new_votes[j] = remaining * votes[j] / others_sum
    elif remaining > 0:
        for j in others:
            new_votes[j] = remaining / len(others)
    else:
        for j in others:
            new_votes[j] = 0

    # Round to ints and correct any rounding drift to keep exact sum of 100
    int_votes = [int(round(v)) for v in new_votes]
    int_votes[changed_idx] = new_val
    diff = 100 - sum(int_votes)
    if diff != 0:
        adjust_idx = max(others, key=lambda j: int_votes[j])
        int_votes[adjust_idx] = max(0, int_votes[adjust_idx] + diff)

    st.session_state[f"{_KEY}_votes"] = int_votes
    for j in range(n):
        st.session_state[f"{_KEY}_slider_{j}"] = int_votes[j]


def render():
    init_defaults(_KEY, _DEFAULTS)

    render_method_intro(
        "First Past the Post",
        "Each voter picks one candidate. The candidate with the most votes wins, even without a majority.",
        "Votes can split between similar candidates. This can let someone win even if most voters prefer others.",
        "Try to keep Molly winning, while the total votes for the other two are still above 50%.",
    )

    candidates: list[str] = st.session_state[f"{_KEY}_candidates"]
    votes: list[int] = st.session_state[f"{_KEY}_votes"]

    # Initialise slider keys from votes on first load (or after reset)
    for i, v in enumerate(votes):
        key = f"{_KEY}_slider_{i}"
        if key not in st.session_state:
            st.session_state[key] = int(v)

    st.divider()
    st.markdown("### Simulation")

    total = sum(votes)
    if total == 0:
        st.warning("All vote shares are 0.")
        return

    winner_idx = votes.index(max(votes))
    winner = candidates[winner_idx]
    winner_pct = float(votes[winner_idx])
    others_pct = 100.0 - winner_pct

    col1, col2, col3 = st.columns(3)
    col1.metric("Winner", winner)
    col2.metric("Winning vote share", f"{winner_pct:.0f}%")
    col3.metric("Combined opposition", f"{others_pct:.0f}%")

    results = sorted(zip(candidates, votes), key=lambda x: -x[1])
    df = pd.DataFrame([{"Candidate": c, "Vote share": f"{p}%"} for c, p in results])
    st.dataframe(df, hide_index=True, use_container_width=True)
    if winner_pct < 50:
        st.error(
            f"{winner} finishes first with {winner_pct:.0f}%, but {others_pct:.0f}% of voters preferred someone else."
        )
        st.caption(
            "This is the classic vote-splitting problem: the majority is divided across multiple alternatives."
        )
    else:
        st.success(
            f"{winner} has a true majority with {winner_pct:.0f}%, so the result is not being distorted by vote splitting here."
        )
        st.caption(
            "When the leader is above 50%, the winner is also the majority choice."
        )

    st.markdown("### Try A Different Split")

    for i, c in enumerate(candidates):
        st.slider(
            c,
            0,
            100,
            key=f"{_KEY}_slider_{i}",
            on_change=_on_slider_change,
            args=(i,),
        )

    if st.button("Reset", type="primary", key=f"reset_{_KEY}"):
        reset_tab(_KEY, _DEFAULTS)
        for i in range(len(candidates)):
            st.session_state.pop(f"{_KEY}_slider_{i}", None)
        st.rerun()
