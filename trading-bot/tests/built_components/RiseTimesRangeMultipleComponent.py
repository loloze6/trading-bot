"""Spec of RiseTimesRangeMultipleComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'RiseTimesRangeMultipleComponent'
SETTINGS = [{}, {"rise_period": 5, "range_period": 20}, {"rise_period": 1, "range_period": 14, "side": "down", "exclude_current": 1}]


def hand(df, params):
    rp = int(params.get("rise_period", 5))
    rg = int(params.get("range_period", 20))
    side = params.get("side", "up")
    ex = int(params.get("exclude_current", 0))
    c = [float(x) for x in list(df["close"])]
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    t = len(c) - 1
    # base bars: t-rg+1 .. t (ex 0) or t-rg .. t-1 (ex 1)
    idx = [t - ex - k for k in range(rg)]
    vals = [c[t], c[t - rp], h[t], l[t]]
    for i in idx:
        vals.append(h[i])
        vals.append(l[i])
    for v in vals:
        if v != v:
            return float("nan")
    if not c[t - rp] > 0:
        return float("nan")
    ret = c[t] / c[t - rp] - 1.0
    if side == "up":
        move = ret if ret > 0 else 0.0
    else:
        move = -ret if ret < 0 else 0.0
    total = 0.0
    for i in idx:
        total = total + (h[i] - l[i])
    mean_range = total / rg
    if mean_range == 0:
        return 0.0
    return move * 100.0 * (h[t] - l[t]) / mean_range
