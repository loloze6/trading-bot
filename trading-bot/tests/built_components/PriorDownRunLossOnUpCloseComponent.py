"""Spec of PriorDownRunLossOnUpCloseComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'PriorDownRunLossOnUpCloseComponent'
SETTINGS = [{}, {"max_bars": 30, "base": "percent", "window": 30}, {"base": "std", "window": 30}, {"base": "usual_moves", "window": 20, "exclude_current": 1}]


def hand(df, params):
    import math
    max_bars = int(params.get("max_bars", 30))
    base = params.get("base", "percent")
    window = int(params.get("window", 30))
    ex = int(params.get("exclude_current", 0))
    close = [float(x) for x in list(df["close"])]
    if base == "percent":
        need = max_bars + 2
    else:
        need = max(max_bars + 2, window + 1 + ex)
    last = close[len(close) - need:]
    for x in last:
        if x != x or not x > 0:
            return float("nan")
    t = len(close) - 1
    if not close[t] > close[t - 1]:
        return 0.0
    # length of the down run ending at t-1
    n = 0
    while n < max_bars and close[t - 1 - n] < close[t - 2 - n]:
        n = n + 1
    if n == 0:
        return 0.0
    first = close[t - 1 - n]
    loss = (first - close[t - 1]) / first
    if base == "percent":
        return loss * 100.0
    # one-bar returns of the window ending ex bars before t
    rets = []
    for k in range(window):
        j = t - ex - k
        rets.append(close[j] / close[j - 1] - 1.0)
    if base == "usual_moves":
        total = 0.0
        for r in rets:
            total = total + abs(r)
        scale = total / len(rets)
    else:
        mean = sum(rets) / len(rets)
        sq = 0.0
        for r in rets:
            sq = sq + (r - mean) * (r - mean)
        scale = math.sqrt(sq / (len(rets) - 1))
    if not scale > 0:
        return 0.0
    return loss / scale
