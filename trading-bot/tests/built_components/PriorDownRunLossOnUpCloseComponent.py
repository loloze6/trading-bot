"""Spec of PriorDownRunLossOnUpCloseComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'PriorDownRunLossOnUpCloseComponent'
SETTINGS = [{}, {"max_bars": 30, "base": "percent", "window": 30}, {"base": "std", "window": 30}, {"base": "usual_moves", "window": 20, "exclude_current": 1}, {"side": "up", "base": "usual_moves", "window": 30, "exclude_current": 1, "max_bars": 30}]


def hand(df, params):
    max_bars = int(params.get("max_bars", 30))
    base = params.get("base", "percent")
    window = int(params.get("window", 30))
    ex = int(params.get("exclude_current", 0))
    side = params.get("side", "down")
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    if base == "percent":
        need = max_bars + 2
    else:
        need = max(max_bars + 2, window + 1 + ex)
    for x in c[len(c) - need:]:
        if x != x or not x > 0:
            return float("nan")
    # bar t must break the run: a down close for an up run, an up close for a down run
    if side == "up":
        if not c[t] < c[t - 1]:
            return 0.0
    else:
        if not c[t] > c[t - 1]:
            return 0.0
    # length of the run ending at bar t-1
    n = 0
    i = t - 1
    while n < max_bars:
        if side == "up":
            ok = c[i] > c[i - 1]
        else:
            ok = c[i] < c[i - 1]
        if not ok:
            break
        n = n + 1
        i = i - 1
    if n == 0:
        return 0.0
    first = c[t - 1 - n]
    last = c[t - 1]
    if side == "up":
        move = (last - first) / first
    else:
        move = (first - last) / first
    if base == "percent":
        return move * 100.0
    # one-bar returns of the window ending ex bars before t
    rets = []
    j = t - ex
    for k in range(window):
        rets.append(c[j - k] / c[j - k - 1] - 1.0)
    if base == "usual_moves":
        total = 0.0
        for r in rets:
            total = total + abs(r)
        d = total / window
    else:
        mu = sum(rets) / window
        ss = 0.0
        for r in rets:
            ss = ss + (r - mu) * (r - mu)
        d = (ss / (window - 1)) ** 0.5
    if not d > 0:
        return 0.0
    return move / d
