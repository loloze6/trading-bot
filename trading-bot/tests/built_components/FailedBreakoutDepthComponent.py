"""Spec of FailedBreakoutDepthComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'FailedBreakoutDepthComponent'
SETTINGS = [{}, {"period": 20, "fail_window": 3}, {"period": 20, "fail_window": 4, "source": "high"}, {"period": 20, "fail_window": 10, "source": "high", "reference": "breakout_low", "exclude_current": 1}, {"period": 20, "fail_window": 3, "exclude_current": 1, "lag": 2, "source": "close", "reference": "prior_high"}]


def hand(df, params):
    p = int(params.get("period", 20))
    fw = int(params.get("fail_window", 3))
    source = params.get("source", "close")
    reference = params.get("reference", "prior_high")
    ex = int(params.get("exclude_current", 0))
    lag = int(params.get("lag", 0))
    c = [float(x) for x in list(df["close"])]
    h = [float(x) for x in list(df["high"])] if "high" in df.columns else None
    lo = [float(x) for x in list(df["low"])] if "low" in df.columns else None
    t = len(c) - 1
    e = t - lag

    def isnan(x):
        return x != x

    # every value the measure reads
    if source == "close":
        for i in range(e - p - fw - ex + 1, e + 1):
            if isnan(c[i]):
                return float("nan")
    else:
        for i in range(e - p - fw - ex + 1, e - ex):
            if isnan(h[i]):
                return float("nan")
        for i in range(e - fw - ex + 1, e + 1):
            if isnan(c[i]):
                return float("nan")

    # candidate breakout bars, most recent first
    if ex == 0:
        cands = [e - k for k in range(fw)]
    else:
        cands = [e - 1 - k for k in range(fw)]
    for j in cands:
        best = None
        for i in range(j - p, j):
            v = c[i] if source == "close" else h[i]
            if best is None or v > best:
                best = v
        if c[j] > best:
            R = best if reference == "prior_high" else lo[j]
            if isnan(R) or not R > 0:
                return float("nan")
            d = R - c[e]
            if d < 0:
                d = 0.0
            return d / R * 100.0
    return 0.0
