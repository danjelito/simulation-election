import pandas as pd
import streamlit as st

from utils.state import init_defaults, reset_tab
from utils.ui import render_method_intro, render_vote_total

_KEY = "runoff"
_DEFAULTS = {
    "candidates": ["Molly", "Darrow", "Mamoru"],
    "round1": [40, 35, 25],
    "transfer_to": "Darrow",
}


def _on_slider_change(changed_idx: int) -> None:
    """Keep all round-1 sliders summing to 100 by proportionally adjusting the others."""
    candidates = st.session_state[f"{_KEY}_candidates"]
    n = len(candidates)
    votes = list(st.session_state[f"{_KEY}_round1"])
    new_val = st.session_state[f"{_KEY}_r1_{changed_idx}"]

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

    int_votes = [int(round(v)) for v in new_votes]
    int_votes[changed_idx] = new_val
    diff = 100 - sum(int_votes)
    if diff != 0:
        adjust_idx = max(others, key=lambda j: int_votes[j])
        int_votes[adjust_idx] = max(0, int_votes[adjust_idx] + diff)

    st.session_state[f"{_KEY}_round1"] = int_votes
    for j in range(n):
        st.session_state[f"{_KEY}_r1_{j}"] = int_votes[j]


def render():
    init_defaults(_KEY, _DEFAULTS)

    render_method_intro(
        "50%+1 Runoff",
        "If no one gets 50%, remove the last place candidate. Move their votes to others. Keep going until someone wins.",
        "The order of removal can change the winner.",
        "See what happens when the first leader loses after Mamoru is removed and his votes go to Darrow.",
    )

    candidates: list[str] = st.session_state[f"{_KEY}_candidates"]
    round1: list[int] = st.session_state[f"{_KEY}_round1"]
    transfer_to: str = st.session_state[f"{_KEY}_transfer_to"]

    # Initialise slider keys from round1 on first load (or after reset)
    for i, v in enumerate(round1):
        key = f"{_KEY}_r1_{i}"
        if key not in st.session_state:
            st.session_state[key] = int(v)

    st.divider()
    st.markdown("### Simulation")

    total1 = sum(round1)
    if total1 > 0:
        normed1 = [v / total1 * 100 for v in round1]
        paired = list(zip(candidates, normed1))
        sorted1 = sorted(paired, key=lambda x: -x[1])
        round1_leader = sorted1[0][0]

        summary_cols = st.columns(3)
        summary_cols[0].metric("Round 1 leader", round1_leader)

        st.markdown("#### Round 1")
        df1 = pd.DataFrame(
            [{"Candidate": c, "Vote share": f"{p:.1f}%"} for c, p in sorted1]
        )
        st.dataframe(df1, hide_index=True, use_container_width=True)

        if max(normed1) > 50:
            winner = candidates[normed1.index(max(normed1))]
            summary_cols[1].metric("Eliminated", "None")
            summary_cols[2].metric("Final winner", winner)
            st.success(
                f"{winner} already has more than 50%, so the runoff never happens."
            )
            st.caption(
                "This scenario does not demonstrate the failure mode because the first round already produced a majority winner."
            )
        else:
            eliminated_name, eliminated_pct = min(paired, key=lambda x: x[1])
            remaining = [(c, p) for c, p in paired if c != eliminated_name]
            summary_cols[1].metric("Eliminated", eliminated_name)

            st.warning(
                f"No one has a majority, so {eliminated_name} is eliminated with {eliminated_pct:.1f}%."
                f" **In this simplified demo, all of {eliminated_name}'s votes transfer to {transfer_to}**."
            )

            round2: dict[str, float] = {c: p for c, p in remaining}
            if transfer_to in round2:
                round2[transfer_to] += eliminated_pct

            total2 = sum(round2.values())
            round2_normed = {c: v / total2 * 100 for c, v in round2.items()}
            sorted2 = sorted(round2_normed.items(), key=lambda x: -x[1])

            st.markdown("#### Final Round")
            df2 = pd.DataFrame(
                [{"Candidate": c, "Vote share": f"{p:.1f}%"} for c, p in sorted2]
            )
            st.dataframe(df2, hide_index=True, use_container_width=True)

            winner = max(round2_normed, key=round2_normed.get)
            winner_pct = round2_normed[winner]
            summary_cols[2].metric("Final winner", winner)
            st.success(
                f"{winner} wins the runoff with {winner_pct:.1f}% after the transfer."
            )

            if winner != round1_leader:
                st.error(
                    f"**Note:** {round1_leader} led after Round 1 but lost to {winner} in the final round. "
                    "The transfer of votes changed the outcome."
                )
            else:
                st.info(
                    f"**Note:** {winner} wins in both rounds. Try moving the slider below to see different outcomes."
                )

    else:
        st.warning("All round 1 votes are 0.")

    st.markdown("### Try A Different Round 1")
    st.caption(
        "First set the opening vote shares, then choose where the eliminated candidate's votes go. That transfer is the lever that reveals path dependence in this simplified example."
    )

    for i, c in enumerate(candidates):
        st.slider(
            c,
            0,
            100,
            key=f"{_KEY}_r1_{i}",
            on_change=_on_slider_change,
            args=(i,),
        )

    current_eliminated = candidates[round1.index(min(round1))]
    remaining_candidates = [c for c in candidates if c != current_eliminated]

    st.markdown(f"#### Transfer rule for {current_eliminated}")
    transfer_idx = (
        remaining_candidates.index(transfer_to)
        if transfer_to in remaining_candidates
        else 0
    )
    new_transfer = st.selectbox(
        f"If {current_eliminated} is eliminated, transfer those votes to:",
        remaining_candidates,
        index=transfer_idx,
        key=f"{_KEY}_transfer_sel",
    )
    if new_transfer != transfer_to:
        st.session_state[f"{_KEY}_transfer_to"] = new_transfer
        st.rerun()

    if st.button("Reset", type="primary", key=f"reset_{_KEY}"):
        reset_tab(_KEY, _DEFAULTS)
        for i in range(len(candidates)):
            st.session_state.pop(f"{_KEY}_r1_{i}", None)
        st.rerun()
