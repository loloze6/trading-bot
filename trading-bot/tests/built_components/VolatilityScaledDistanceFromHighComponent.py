"""Spec of VolatilityScaledDistanceFromHighComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'VolatilityScaledDistanceFromHighComponent'
SETTINGS = [{}, {"period": 20, "vol_period": 20}, {"period": 1, "vol_period": 20, "source": "high", "exclude_current": 0, "base": "close"}, {"period": 1, "vol_period": 30, "source": "high", "exclude_current": 0, "base": "close", "extreme": "low"}]


def hand(df, params):
    import math
    period = int(params.get("period", 20))
    vp = int(params.get("vol_period", 20))
    source = params.get("source", "close")
    ex = int(params.get("exclude_current", 1))
    base = params.get("base", "level")
    extreme = params.get("extreme", "high")
    close = [float(x) for x in list(df["close"])]
    t = len(close) - 1
    if source == "close":
        vals = close
    else:
        vals = [float(x) for x in list(df["high" if extreme == "high" else "low"])]
    # window bars
    if ex == 1:
        idx = [t - k for k in range(1, period + 1)]
    else:
        idx = [t - k for k in range(0, period)]
    win = [vals[i] for i in idx]
    closes_used = [close[t - k] for k in range(0, vp + 1)]
    for x in win + closes_used:
        if x != x:
            return float("nan")
    R = win[0]
    for x in win:
        if extreme == "high":
            if x > R:
                R = x
        else:
            if x < R:
                R = x
    if not R > 0:
        return float("nan")
    # returns j = t-vp+1 .. t
    rets = []
    for j in range(t - vp + 1, t + 1):
        if not close[j - 1] > 0:
            return float("nan")
        rets.append(close[j] / close[j - 1] - 1.0)
    c = close[t]
    if base == "close" and not c > 0:
        return float("nan")
    D = R if base == "level" else c
    m = sum(rets) / len(rets)
    ss = 0.0
    for r in rets:
        ss += (r - m) * (r - m)
    s = math.sqrt(ss / (len(rets) - 1))
    if not s > 0:
        return 0.0
    return (c - R) / D / s
