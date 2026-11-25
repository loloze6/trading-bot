"""Spec of FallTimesRangeExcessComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'FallTimesRangeExcessComponent'
SETTINGS = [{}]


def hand(df, params):
    closes = [float(x) for x in list(df["close"])]
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    t = len(closes) - 1
    prev = closes[t - 1]
    now = closes[t]
    hi = highs[t]
    lo = lows[t]
    for x in (prev, now, hi, lo):
        if x != x:
            return float("nan")
    if not prev > 0:
        return float("nan")
    drop = prev - now
    if drop < 0:
        drop = 0.0
    fall = drop / prev * 100.0
    beyond = (hi - lo) - drop
    if beyond < 0:
        beyond = 0.0
    beyond_pct = beyond / prev * 100.0
    return fall * beyond_pct
