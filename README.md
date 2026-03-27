# Voting Systems Simulator

An educational Streamlit app demonstrating the mathematical limitations of five voting systems: First Past the Post, Runoff, Instant Runoff Voting, Borda Count, and Condorcet.

## Quick Start

```bash
uv sync
uv run streamlit run app.py
```

## Features

- **Five voting methods** — each isolated in its own tab
- **Preloaded paradox examples** — explore known failure modes
- **Interactive simulation** — edit voter preferences and see live results
- **Educational focus** — understand why single methods fail

## Structure

```
app.py              # Entry point
methods/            # One module per voting system
utils/
    calc.py           # Pure calculation functions
    state.py          # Session state helpers
```

Each tab follows the same flow:

1. Method definition
2. Preloaded paradox example
3. Simulation output
4. Why it fails
5. User controls
6. Reset button