"""Spec of BreakoutInMeanRangesComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'BreakoutInMeanRangesComponent'
SETTINGS = [{}, {"period": 12, "base_period": 180}, {"period": 12, "base_period": 180, "side": "below"}, {"period": 1, "base_period": 20, "side": "below", "high_current": 1, "base_exclude_current": 1}, {"period": 1, "base_period": 30, "side": "below", "high_current": 0, "base_exclude_current": 1, "source": "close"}]


def hand(df, params):
    p = int(params.get("period", 12))
    bp = int(params.get("base_period", 180))
    side = params.get("side", "above")
    hc = int(params.get("high_current", 0))
    bex = int(params.get("base_exclude_current", 0))
    source = params.get("source", "high")
    closes = [float(x) for x in list(df["close"])]
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    t = len(closes) - 1
    xs = closes if source == "close" else highs

    # reference level: stretch ends at t-1 (hc 0) or at t (hc 1), p bars long
    end = t if hc == 1 else t - 1
    level_vals = [xs[i] for i in range(end - p + 1, end + 1)]
    # base: bp bar ranges ending at t (bex 0) or t-1 (bex 1)
    bend = t - bex
    ranges = [highs[i] - lows[i] for i in range(bend - bp + 1, bend + 1)]
    c = closes[t]
    for v in level_vals + ranges + [c]:
        if v != v:
            return float("nan")
    H = level_vals[0]
    for v in level_vals:
        if v > H:
            H = v
    total = 0.0
    for r in ranges:
        total += r
    B = total / len(ranges)
    if B == 0:
        return 0.0
    if side == "above":
        d = c - H
    else:
        d = H - c
    if d < 0:
        d = 0.0
    return d / B
