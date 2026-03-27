# Copilot Instructions — Voting Systems Simulator

## Running the App

```bash
# Install dependencies
uv sync

# Run the Streamlit app
uv run streamlit run app.py
```

## Architecture

This is an educational Streamlit app demonstrating the mathematical limitations of six voting systems. Each method is isolated in its own module and rendered in a separate tab.

```
app.py                  # Entry point — wires st.tabs() to each method's render()
methods/
  fptp.py               # First Past the Post
  runoff.py             # 50%+1 Runoff
  irv.py                # Instant Runoff Voting
  borda.py              # Borda Count
  condorcet.py          # Condorcet method
utils/
  calc.py               # Pure calculation functions (no Streamlit)
  state.py              # Session state initialisation and reset helpers
```

## Key Conventions

### Module interface
Each `methods/*.py` exports exactly one function: `render()`. `app.py` calls each one inside the corresponding `st.tabs()` context — nothing else.

### Session state namespacing
All session state keys are prefixed with the tab name: `fptp_votes`, `irv_groups`, `borda_rankings`, etc. Use `utils/state.py` helpers to initialise and reset state:
- `init_defaults(tab_key, defaults)` — writes defaults only if keys are absent
- `reset_tab(tab_key, defaults)` — overwrites keys unconditionally (called by Reset button)

### Data model
Voter groups are represented as a list of dicts with `weight` (float, 0–100) and either `preferences` (ordered list of candidate names) or `approvals` (list of approved candidate names). Always validate that weights sum to 100 before running simulation logic.

### Tab layout (all tabs follow this order)
1. Method definition — `st.markdown()`
2. Preloaded paradox example — rendered from session state defaults
3. Simulation output — winner, intermediate steps, paradox highlight
4. Why it fails — `st.info()` or `st.warning()` callout
5. User controls — sliders / `st.data_editor` tables / checkboxes
6. Reset button — `st.button("Reset", key="reset_<tab>")` that calls `reset_tab()`

### Editable tables
Use `st.data_editor` (requires Streamlit ≥ 1.23) for all ranking and approval grid inputs.

### Calculation functions
Pure functions live in `utils/calc.py` and take only plain Python data (no Streamlit calls). Key functions:
- `borda_scores(groups, candidates)` → `dict[str, float]`
- `pairwise_matrix(groups, candidates)` → `pd.DataFrame`
- `irv_rounds(groups, candidates)` → `list[dict]` (one dict per round)

### Preloaded examples
Each tab's default state demonstrates a specific known failure:
- **FPTP**: vote splitting — Molly wins with 40% despite 60% preferring others
- **Runoff**: path dependence — Darrow beats early leader Molly after Mamoru is eliminated
- **IRV**: monotonicity violation — moving Darrow up causes Darrow to lose
- **Borda**: IIA violation — adding weak candidate C flips A→B winner
- **Condorcet**: Condorcet paradox — Burger > Pizza > Sushi > Burger cycle
- **Approval**: strategic sensitivity — outcome shifts based on breadth of approval

### Percentages
All weights are stored and displayed as floats from 0–100 (not 0–1). Sliders use `step=1` and the UI always shows a live sum indicator when editing weights.
