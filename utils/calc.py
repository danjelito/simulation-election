"""Pure calculation functions — no Streamlit calls."""
from __future__ import annotations

import pandas as pd

def borda_scores(groups: list[dict], candidates: list[str]) -> dict[str, float]:
    """Compute weighted Borda scores for each candidate.

    Each group has 'weight' (0-100) and 'preferences' (ordered list, best first).
    Points: n-1 for 1st, n-2 for 2nd, ..., 0 for last.
    """
    n = len(candidates)
    scores: dict[str, float] = {c: 0.0 for c in candidates}
    for group in groups:
        weight = group["weight"]
        prefs = group["preferences"]
        for rank, candidate in enumerate(prefs):
            if candidate in scores:
                scores[candidate] += weight * (n - 1 - rank)
    return scores


def pairwise_matrix(groups: list[dict], candidates: list[str]) -> pd.DataFrame:
    """Compute pairwise head-to-head vote shares.

    Returns a DataFrame where cell [A][B] = total weight of voters who prefer A over B.
    """
    n = len(candidates)
    matrix = {c: {d: 0.0 for d in candidates} for c in candidates}
    for group in groups:
        weight = group["weight"]
        prefs = group["preferences"]
        for i, a in enumerate(prefs):
            for j, b in enumerate(prefs):
                if i < j and a in matrix and b in matrix:
                    matrix[a][b] += weight
    return pd.DataFrame(matrix).T  # rows = winner, cols = loser


def irv_rounds(groups: list[dict], candidates: list[str]) -> list[dict]:
    """Simulate IRV elimination rounds.

    Returns a list of round dicts, each with:
      - 'tallies': dict[candidate, float]
      - 'eliminated': str | None
    """
    remaining = list(candidates)
    current_groups = [
        {"weight": g["weight"], "preferences": [p for p in g["preferences"] if p in remaining]}
        for g in groups
    ]

    rounds = []
    while len(remaining) > 1:
        tallies: dict[str, float] = {c: 0.0 for c in remaining}
        for group in current_groups:
            prefs = [p for p in group["preferences"] if p in remaining]
            if prefs:
                tallies[prefs[0]] += group["weight"]

        total = sum(tallies.values())
        # Check for majority
        for c, v in tallies.items():
            if total > 0 and v / total > 0.5:
                rounds.append({"tallies": tallies, "eliminated": None})
                return rounds

        # Eliminate lowest
        eliminated = min(tallies, key=lambda c: tallies[c])
        rounds.append({"tallies": tallies, "eliminated": eliminated})
        remaining.remove(eliminated)
        current_groups = [
            {"weight": g["weight"], "preferences": [p for p in g["preferences"] if p in remaining]}
            for g in current_groups
        ]

    # Last candidate standing
    if remaining:
        tallies = {remaining[0]: 100.0}
        rounds.append({"tallies": tallies, "eliminated": None})

    return rounds
