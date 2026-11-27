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
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    if source == "close":
        col = closes
    elif extreme == "high":
        col = [float(x) for x in list(df["high"])]
    else:
        col = [float(x) for x in list(df["low"])]
    # window: bars t-ex-period+1 .. t-ex
    vals = []
    for k in range(period):
        vals.append(col[t - ex - k])
    c = closes[t]
    rc = []
    for j in range(t - vp, t + 1):
        rc.append(closes[j])
    for x in vals + [c] + rc:
        if x != x:
            return float("nan")
    for x in rc[:-1]:
        if not x > 0:
            return float("nan")
    R = vals[0]
    for x in vals:
        if extreme == "high":
            if x > R:
                R = x
        else:
            if x < R:
                R = x
    if not R > 0:
        return float("nan")
    if base == "close" and not c > 0:
        return float("nan")
    rets = []
    for i in range(1, len(rc)):
        rets.append(rc[i] / rc[i - 1] - 1.0)
    m = sum(rets) / len(rets)
    var = 0.0
    for r in rets:
        var += (r - m) * (r - m)
    s = math.sqrt(var / (len(rets) - 1))
    if s == 0:
        return 0.0
    D = R if base == "level" else c
    return (c - R) / D / s
