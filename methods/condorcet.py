import pandas as pd
import streamlit as st
from streamlit_sortables import sort_items

from utils.calc import pairwise_matrix
from utils.state import init_defaults, reset_tab
from utils.ui import render_method_intro

_KEY = "condorcet"
_CANDIDATES = ["Pizza", "Burger", "Sushi"]
_DEFAULTS = {
    "rankings": [
        ["Burger", "Pizza", "Sushi"],
        ["Pizza", "Sushi", "Burger"],
        ["Sushi", "Burger", "Pizza"],
    ],
    "reset_nonce": 0,
}


def _fresh_defaults() -> dict:
    return {
        "rankings": [ranking[:] for ranking in _DEFAULTS["rankings"]],
        "reset_nonce": _DEFAULTS["reset_nonce"],
    }


def _find_condorcet_winner(matrix: pd.DataFrame, candidates: list[str]) -> str | None:
    for c in candidates:
        if all(
            float(matrix.at[c, d]) > float(matrix.at[d, c])
            for d in candidates
            if d != c
        ):
            return c
    return None


def _find_cycle(
    matrix: pd.DataFrame, candidates: list[str]
) -> list[tuple[str, str]] | None:
    cycle = []
    for i, a in enumerate(candidates):
        b = candidates[(i + 1) % len(candidates)]
        if float(matrix.at[a, b]) > float(matrix.at[b, a]):
            cycle.append((a, b))
    return cycle if len(cycle) == len(candidates) else None


def _rankings_to_groups(rankings: list[list[str]]) -> list[dict]:
    return [{"weight": 1.0, "preferences": ranking} for ranking in rankings]


def _candidate_results(
    matrix: pd.DataFrame, candidates: list[str], candidate: str
) -> tuple[int, int, int, list[str]]:
    wins = 0
    losses = 0
    ties = 0
    details = []

    for other in candidates:
        if other == candidate:
            continue

        cv = int(matrix.at[candidate, other])
        ov = int(matrix.at[other, candidate])

        if cv > ov:
            wins += 1
            details.append(f"beats {other} {cv}-{ov}")
        elif ov > cv:
            losses += 1
            details.append(f"loses to {other} {cv}-{ov}")
        else:
            ties += 1
            details.append(f"ties {other} {cv}-{ov}")

    return wins, losses, ties, details


def render():
    init_defaults(_KEY, _fresh_defaults())

    render_method_intro(
        "Condorcet Method",
        "A Condorcet winner is a candidate who beats every other candidate in one-on-one comparisons.",
        "Group preferences can cycle, so every candidate can beat one rival and lose to another. When that happens, no Condorcet winner exists.",
        "Drag the rankings below and watch for a loop such as Burger beats Pizza, Pizza beats Sushi, and Sushi beats Burger.",
    )

    rankings: list[list[str]] = st.session_state[f"{_KEY}_rankings"]
    reset_nonce: int = st.session_state[f"{_KEY}_reset_nonce"]

    st.divider()
    st.markdown("### Edit The Voter Rankings")
    st.caption(
        "Drag candidates within each column (left = higher preference, right = lower). The page updates immediately after you reorder a voter."
    )

    # Collect all sorted rankings from the component
    new_rankings = []
    changed = False

    for i in range(len(rankings)):
        st.markdown(f"**Voter {i + 1}**")

        sorted_ranking = sort_items(
            rankings[i], 
            key=f"{_KEY}_voter_{i}_{reset_nonce}"
        )

        new_rankings.append(sorted_ranking)
        
        # Track if any ranking changed (by value, not reference)
        if sorted_ranking != rankings[i]:
            changed = True

    # Update session state only once if any ranking changed
    if changed:
        st.session_state[f"{_KEY}_rankings"] = new_rankings
        st.rerun()

    groups = _rankings_to_groups(new_rankings)
    matrix = pairwise_matrix(groups, _CANDIDATES)

    st.markdown("### Current Head-To-Head Outcome")

    winner = _find_condorcet_winner(matrix, _CANDIDATES)
    if winner is not None:
        wins, _, _, details = _candidate_results(matrix, _CANDIDATES, winner)
        st.success(
            f"{winner} is the Condorcet winner because it stays undefeated across all head-to-head matchups."
        )
        st.caption(f"Why: {'; '.join(details)}.")
    else:
        st.error("No winner exists because the group creates a preference cycle.")
        cycle = _find_cycle(matrix, _CANDIDATES)
        if cycle is not None:
            cycle_str = " -> ".join(a for a, _ in cycle) + f" -> {cycle[0][0]}"
            cycle_details = ", ".join(
                f"{a} beats {b} {int(matrix.at[a, b])}-{int(matrix.at[b, a])}"
                for a, b in cycle
            )
            st.markdown(f"**Cycle detected:** {cycle_str}")
            st.caption(f"Why no winner emerges: {cycle_details}.")

    st.info(
        "A Condorcet winner must beat everyone else directly. If the head-to-head preferences form a loop, the method has no clean answer."
    )

    summary_cols = st.columns(len(_CANDIDATES))
    for col, candidate in zip(summary_cols, _CANDIDATES):
        wins, losses, ties, details = _candidate_results(matrix, _CANDIDATES, candidate)
        with col:
            with st.container(border=True):
                st.markdown(f"**{candidate}**")
                st.metric("Record", f"{wins}-{losses}", delta=f"{ties} ties")
                for detail in details:
                    st.markdown(f"- {detail}")

    pairwise_rows = []
    for candidate in _CANDIDATES:
        row = {"Candidate": candidate}
        for other in _CANDIDATES:
            if other == candidate:
                row[other] = "-"
            else:
                row[other] = (
                    f"{int(matrix.at[candidate, other])}-{int(matrix.at[other, candidate])}"
                )
        pairwise_rows.append(row)

    st.markdown("#### Pairwise evidence")
    st.dataframe(pd.DataFrame(pairwise_rows), hide_index=True, use_container_width=True)
    st.caption(
        "Each cell reads as votes for the row candidate versus votes for the column candidate."
    )

    st.markdown("### Reset The Example")
    st.caption("Reset returns the page to the three-voter paradox example.")

    if st.button("Reset", type="primary", key=f"reset_{_KEY}"):
        reset_nonce = st.session_state.get(f"{_KEY}_reset_nonce", 0)
        reset_tab(_KEY, _fresh_defaults())
        st.session_state[f"{_KEY}_reset_nonce"] = reset_nonce + 1
        st.rerun()
