"""Spec of PriorDownRunOnUpCloseComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'PriorDownRunOnUpCloseComponent'
SETTINGS = [{}, {"max_bars": 30}, {"max_bars": 30, "form": "beyond_first"}, {"side": "up"}]


def hand(df, params):
    max_bars = int(params.get("max_bars", 30))
    form = params.get("form", "count")
    side = params.get("side", "down")
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    # NaN anywhere in the last max_bars + 2 rows gives NaN
    for k in range(max_bars + 2):
        x = closes[t - k]
        if x != x:
            return float("nan")
    # does bar t break a run to the counted side?
    if side == "up":
        if not closes[t] < closes[t - 1]:
            return 0.0
    else:
        if not closes[t] > closes[t - 1]:
            return 0.0
    # length of the run of moving bars ending at t-1
    n = 0
    i = t - 1
    while True:
        if n == max_bars:
            break
        if side == "up":
            moved = closes[i] > closes[i - 1]
        else:
            moved = closes[i] < closes[i - 1]
        if not moved:
            break
        n = n + 1
        i = i - 1
    if form == "beyond_first":
        if n - 1 > 0:
            return float(n - 1)
        return 0.0
    return float(n)
