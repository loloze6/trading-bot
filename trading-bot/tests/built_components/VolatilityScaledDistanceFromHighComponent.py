"""Spec of VolatilityScaledDistanceFromHighComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'VolatilityScaledDistanceFromHighComponent'
SETTINGS = [{}, {"period": 20, "vol_period": 20}, {"period": 1, "vol_period": 20, "source": "high", "exclude_current": 0, "base": "close"}]


def hand(df, params):
    import math
    p = int(params.get("period", 20))
    vp = int(params.get("vol_period", 20))
    source = params.get("source", "close")
    ex = int(params.get("exclude_current", 1))
    base = params.get("base", "level")
    c = [float(x) for x in list(df["close"])]
    src = c if source == "close" else [float(x) for x in list(df["high"])]
    t = len(c) - 1
    # window of the high: bars t-p-ex+1 .. t-ex
    win = []
    for k in range(p):
        win.append(src[t - ex - k])
    # closes for the returns: bars t-vp .. t
    closes = []
    for k in range(vp + 1):
        closes.append(c[t - vp + k])
    for x in win + closes:
        if x != x:
            return float("nan")
    H = win[0]
    for x in win:
        if x > H:
            H = x
    if not H > 0:
        return float("nan")
    for x in closes[:-1]:
        if not x > 0:
            return float("nan")
    ct = c[t]
    if base == "close" and not ct > 0:
        return float("nan")
    rets = []
    for k in range(1, len(closes)):
        rets.append(closes[k] / closes[k - 1] - 1.0)
    mean = sum(rets) / len(rets)
    ss = 0.0
    for r in rets:
        ss = ss + (r - mean) ** 2
    s = math.sqrt(ss / (len(rets) - 1))
    if s == 0:
        return 0.0
    D = H if base == "level" else ct
    return (ct - H) / D / s
