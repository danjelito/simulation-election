import streamlit as st


def render_method_intro(
    title: str,
    summary: str,
    failure_mode: str,
    prompt: str,
) -> None:
    st.markdown(f"## {title}")
    st.markdown(summary)

    col1, col2, col3 = st.columns(3)
    sections = [
        ("🎖️ **Winner rule**", summary),
        ("❌ **Failure mode**", failure_mode),
        ("🔍 **What to look for**", prompt),
    ]

    for col, (label, text) in zip((col1, col2, col3), sections):
        with col:
            with st.container(border=True):
                st.caption(label)
                st.markdown(text)


def render_vote_total(total: float, target: float = 100.0) -> None:
    progress = 0.0 if target == 0 else min(max(total / target, 0.0), 1.0)
    st.progress(progress, text=f"Vote total: {total:.0f}% of {target:.0f}%")
    if total == target:
        st.caption(
            "The electorate is complete. Adjusting one value automatically rebalances the others."
        )
    else:
        st.caption(
            "Keep the total at 100% so the result represents one full electorate."
        )
