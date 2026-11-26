"""Spec of FallCloseLocationComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'FallCloseLocationComponent'
SETTINGS = [{}, {"vol_period": 60}, {"vol_period": 30, "base": "mean_bar_range", "exclude_current": 1}]


def hand(df, params):
    import math
    vp = int(params.get("vol_period", 60))
    base = params.get("base", "std")
    e = int(params.get("exclude_current", 0))
    c = [float(x) for x in list(df["close"])]
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    t = len(c) - 1

    def isnan(x):
        return x != x

    if isnan(c[t]) or isnan(c[t - 1]) or isnan(h[t]) or isnan(l[t]):
        return float("nan")
    # where the close sits: 0 at the high, 1 at the low
    if h[t] - l[t] == 0:
        loc = 0.5
    else:
        loc = (h[t] - c[t]) / (h[t] - l[t])

    if base == "std":
        # returns j = t-e-vp+1 .. t-e
        rets = []
        for j in range(t - e - vp + 1, t - e + 1):
            a = c[j - 1]
            b = c[j]
            if isnan(a) or isnan(b):
                return float("nan")
            if not a > 0:
                return float("nan")
            rets.append(b / a - 1.0)
        if not c[t - 1] > 0:
            return float("nan")
        m = sum(rets) / len(rets)
        ss = 0.0
        for r in rets:
            ss += (r - m) * (r - m)
        s = math.sqrt(ss / (len(rets) - 1))
        day_ret = c[t] / c[t - 1] - 1.0
        fall = 0.0
        if s > 0 and day_ret < 0:
            fall = -day_ret / s
    else:
        # mean bar range over i = t-e-vp+1 .. t-e
        total = 0.0
        for i in range(t - e - vp + 1, t - e + 1):
            if isnan(h[i]) or isnan(l[i]):
                return float("nan")
            total += h[i] - l[i]
        mean_range = total / vp
        drop = c[t - 1] - c[t]
        fall = 0.0
        if mean_range > 0 and drop > 0:
            fall = drop / mean_range
    return fall * loc
