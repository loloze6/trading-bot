"""Spec of RiseTimesRangeMultipleComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'RiseTimesRangeMultipleComponent'
SETTINGS = [{}, {"rise_period": 5, "range_period": 20}]


def hand(df, params):
    p = int(params.get("rise_period", 5))
    n = int(params.get("range_period", 20))
    c = [float(x) for x in list(df["close"])]
    hi = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    t = len(c) - 1
    now = c[t]
    base = c[t - p]
    widths = []
    for k in range(n):
        i = t - k
        if hi[i] != hi[i] or lo[i] != lo[i]:
            return float("nan")
        widths.append(hi[i] - lo[i])
    if now != now or base != base:
        return float("nan")
    if not base > 0:
        return float("nan")
    ret = now / base - 1.0
    if ret < 0.0:
        ret = 0.0
    total = 0.0
    for w in widths:
        total = total + w
    avg = total / n
    if avg == 0.0:
        return 0.0
    today = hi[t] - lo[t]
    return ret * 100.0 * today / avg
