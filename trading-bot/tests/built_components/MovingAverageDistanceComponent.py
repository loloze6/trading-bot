"""Spec of MovingAverageDistanceComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'MovingAverageDistanceComponent'
SETTINGS = [{}, {"period": 20, "average": "sma", "base": "usual_moves", "vol_period": 20}]


def hand(df, params):
    import math
    n = int(params.get("period", 50))
    avg = params.get("average", "sma")
    base = params.get("base", "percent")
    vp = int(params.get("vol_period", 20))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    last = c[t]
    if last != last:
        return float("nan")
    if avg == "sma":
        total = 0.0
        for k in range(n):
            x = c[t - k]
            if x != x:
                return float("nan")
            total = total + x
        ma = total / n
    else:
        alpha = 2.0 / (n + 1.0)
        e = None
        for x in c:
            if x != x:
                continue
            if e is None:
                e = x
            else:
                e = (1.0 - alpha) * e + alpha * x
        ma = e
    if ma is None or ma == 0:
        return float("nan")
    rel = (last - ma) / ma
    if base == "percent":
        return rel * 100.0
    rets = []
    for j in range(t - vp + 1, t + 1):
        a = c[j - 1]
        b = c[j]
        if a != a or b != b or not a > 0:
            return float("nan")
        rets.append(b / a - 1.0)
    m = sum(rets) / len(rets)
    var = 0.0
    for r in rets:
        var = var + (r - m) * (r - m)
    s = math.sqrt(var / (len(rets) - 1))
    if s == 0:
        return 0.0
    return rel / s
