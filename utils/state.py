import streamlit as st


def init_defaults(tab_key: str, defaults: dict) -> None:
    """Write defaults to session_state only if keys are absent."""
    for k, v in defaults.items():
        full_key = f"{tab_key}_{k}"
        if full_key not in st.session_state:
            st.session_state[full_key] = v


def reset_tab(tab_key: str, defaults: dict) -> None:
    """Overwrite session_state keys with defaults unconditionally."""
    for k, v in defaults.items():
        st.session_state[f"{tab_key}_{k}"] = v
