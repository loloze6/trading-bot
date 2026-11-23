"""Spec of CloseLocationTimesVolatilityComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'CloseLocationTimesVolatilityComponent'
SETTINGS = [{}, {"vol_period": 20}]


def hand(df, params):
    import math
    n = int(params.get("vol_period", 20))
    closes = [float(x) for x in list(df["close"])]
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    t = len(closes) - 1
    h = highs[t]
    l = lows[t]
    c = closes[t]
    used = [closes[t - k] for k in range(n + 1)]
    for x in used + [h, l]:
        if x != x:
            return float("nan")
    # one-bar returns of bars t-n+1 .. t
    rets = []
    for j in range(t - n + 1, t + 1):
        base = closes[j - 1]
        if not base > 0:
            return float("nan")
        rets.append(closes[j] / base - 1.0)
    total = 0.0
    for r in rets:
        total += r
    mean = total / len(rets)
    ss = 0.0
    for r in rets:
        ss += (r - mean) * (r - mean)
    s = math.sqrt(ss / (len(rets) - 1))
    if h == l:
        loc = 0.5
    else:
        loc = (h - c) / (h - l)
    return loc * s
