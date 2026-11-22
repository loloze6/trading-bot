"""Spec of UpStreakGainTimesDepthBelowAverageComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'UpStreakGainTimesDepthBelowAverageComponent'
SETTINGS = [{}, {"window": 180, "max_bars": 180, "ma_period": 180}]


def hand(df, params):
    window = int(params.get("window", 180))
    max_bars = int(params.get("max_bars", 180))
    ma_period = int(params.get("ma_period", 180))
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    need = max(window + 1, max_bars + 1, ma_period)
    for i in range(last - need + 1, last + 1):
        x = c[i]
        if x != x or not x > 0:
            return float("nan")
    # current run of up closes
    n = 0
    while n < max_bars and c[last - n] > c[last - n - 1]:
        n = n + 1
    # usual one-bar move
    total = 0.0
    for j in range(last - window + 1, last + 1):
        total = total + abs(c[j] / c[j - 1] - 1.0)
    m = total / window
    if n > 0 and m > 0:
        start = c[last - n]
        gain = (c[last] - start) / start / m
    else:
        gain = 0.0
    s = 0.0
    for j in range(last - ma_period + 1, last + 1):
        s = s + c[j]
    sma = s / ma_period
    depth = (sma - c[last]) / sma * 100.0
    if depth < 0:
        depth = 0.0
    return gain * depth
