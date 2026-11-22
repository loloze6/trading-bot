"""Spec of DownStreakLossInUsualMovesComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'DownStreakLossInUsualMovesComponent'
SETTINGS = [{}, {"window": 180, "max_bars": 180}, {"window": 180, "max_bars": 180, "side": "up"}, {"window": 180, "max_bars": 180, "side": "down", "base": "end"}]


def hand(df, params):
    window = int(params.get("window", 180))
    max_bars = int(params.get("max_bars", 180))
    side = params.get("side", "down")
    base = params.get("base", "start")
    closes = [float(x) for x in list(df["close"])]
    need = max(window, max_bars) + 1
    c = closes[len(closes) - need:]
    for x in c:
        if x != x or not x > 0:
            return float("nan")
    t = len(c) - 1
    total = 0.0
    for j in range(t - window + 1, t + 1):
        total += abs(c[j] / c[j - 1] - 1.0)
    m = total / window
    n = 0
    while n < max_bars:
        cur = c[t - n]
        prev = c[t - n - 1]
        if side == "down" and cur < prev:
            n += 1
        elif side == "up" and cur > prev:
            n += 1
        else:
            break
    if n == 0 or m == 0.0:
        return 0.0
    first = c[t - n]
    now = c[t]
    if side == "down":
        if base == "end":
            frac = first / now - 1.0
        else:
            frac = 1.0 - now / first
    else:
        if base == "end":
            frac = 1.0 - first / now
        else:
            frac = now / first - 1.0
    return frac / m
