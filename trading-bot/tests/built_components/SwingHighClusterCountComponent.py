"""Spec of SwingHighClusterCountComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'SwingHighClusterCountComponent'
SETTINGS = [{}, {"period": 90, "side": 2, "band": 2.0, "form": "count"}, {"period": 90, "side": 2, "band": 2.0, "form": "count", "level": "below"}, {"period": 90, "side": 2, "band": 1.0, "form": "count", "level": "above", "pivot": "low", "exclude_current": 1}]


def hand(df, params):
    period = int(params.get("period", 90))
    side = int(params.get("side", 2))
    band = float(params.get("band", 2.0))
    form = params.get("form", "count")
    power = float(params.get("power", 1.0))
    level = params.get("level", "above")
    pivot = params.get("pivot", "high")
    ex = int(params.get("exclude_current", 0))
    col = "high" if pivot == "high" else "low"
    vals = [float(x) for x in list(df[col])]
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    close_t = closes[t]
    last = t - ex                      # last bar of the window
    first = last - period + 1          # first bar of the window
    for k in range(first, last + 1):
        if vals[k] != vals[k]:
            return float("nan")
    if close_t != close_t:
        return float("nan")
    swings = []
    i = first + side
    while i <= last - side:
        is_swing = True
        for k in range(i - side, i + side + 1):
            if k == i:
                continue
            if pivot == "high":
                if not vals[i] >= vals[k]:
                    is_swing = False
            else:
                if not vals[i] < vals[k]:
                    is_swing = False
        if is_swing:
            swings.append(vals[i])
        i += 1
    L = None
    for x in swings:
        if level == "above":
            if x >= close_t and (L is None or x < L):
                L = x
        else:
            if x < close_t and (L is None or x > L):
                L = x
    if L is None:
        return 0.0
    if not L > 0:
        return float("nan")
    n = 0
    for x in swings:
        if abs(x - L) / L * 100.0 <= band:
            n += 1
    if form == "count":
        return float(n)
    if level == "above":
        d = (L - close_t) / L * 100.0
    else:
        d = (close_t - L) / L * 100.0
    return float(n * (1.0 / (1.0 + d)) ** power)
