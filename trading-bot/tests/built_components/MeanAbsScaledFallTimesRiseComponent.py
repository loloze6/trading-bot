"""Spec of MeanAbsScaledFallTimesRiseComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'MeanAbsScaledFallTimesRiseComponent'
SETTINGS = [{}, {"fall_period": 24, "window": 720, "rise_period": 720}, {"fall_period": 1, "window": 720, "rise_period": 24, "rise_lag": 1}]


def hand(df, params):
    fp = int(params.get("fall_period", 24))
    w = int(params.get("window", 720))
    rp = int(params.get("rise_period", 720))
    lag = int(params.get("rise_lag", 0))
    c = [float(x) for x in list(df["close"])]
    need = max(w + fp, rp + lag + 1)
    used = c[len(c) - need:]
    for x in used:
        if x != x or not x > 0:
            return float("nan")
    t = len(c) - 1
    fall = c[t] / c[t - fp] - 1.0
    total = 0.0
    i = t - w + 1
    while i <= t:
        r = c[i] / c[i - fp] - 1.0
        total = total + (r if r >= 0 else -r)
        i = i + 1
    m = total / w
    if m == 0:
        first = 0.0
    else:
        first = -fall / m
        if first < 0:
            first = 0.0
    rise = c[t - lag] / c[t - lag - rp] - 1.0
    if rise < 0:
        rise = 0.0
    return first * rise * 100.0
