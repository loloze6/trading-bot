"""
E-061 C1.3: how tools/run_protocol.py says "refused before any window ran -- no
market data touched", shared with workflow/run_phase1_research.py, which then
records no trial row for it. ONE definition each (the composition_names
pattern). No imports, so either side can import it without weight.
"""
# run_protocol.py's exit code for a refusal before any backtest.
EXIT_NO_DATA_TOUCHED = 3
# ... and the token that must open the FIRST line of its stderr.
NO_DATA_TOUCHED_TOKEN = "[run_protocol] NO DATA TOUCHED"


def stderr_declares_no_data_touched(stderr) -> bool:
    """True when the first line of `stderr` starts with NO_DATA_TOUCHED_TOKEN
    (anchored: the token later in the output, e.g. echoed by a window's own
    logging, does not count)."""
    first = (stderr or "").lstrip("\r\n").split("\n", 1)[0]
    return first.startswith(NO_DATA_TOUCHED_TOKEN)
