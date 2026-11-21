"""Spec of SignalPredictivePowerComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'SignalPredictivePowerComponent'
SETTINGS = [{}, {"signal": "momentum", "corr_lookback": 365, "horizon": 5}]


def hand(df, params):
    import math
    rp = int(params.get("return_period", 28))
    rev = int(params.get("reversal_period", 1))
    hp = int(params.get("high_period", 90))
    vp = int(params.get("vol_period", 30))
    L = int(params.get("corr_lookback", 365))
    h = int(params.get("horizon", 5))
    sig = params.get("signal", "momentum")
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    if sig == "momentum":
        lag = rp
    elif sig == "reversal":
        lag = rev
    elif sig == "high":
        lag = hp - 1
    else:
        lag = vp
    first = t - L - lag
    for j in range(first, t + 1):
        if c[j] != c[j] or not c[j] > 0:
            return float("nan")

    def s_at(i):
        if sig == "momentum":
            return c[i] / c[i - rp] - 1.0
        if sig == "reversal":
            return -(c[i] / c[i - rev] - 1.0)
        if sig == "high":
            m = c[i]
            for j in range(i - hp + 1, i + 1):
                if c[j] > m:
                    m = c[j]
            return c[i] / m - 1.0
        rets = []
        for j in range(i - vp + 1, i + 1):
            rets.append(c[j] / c[j - 1] - 1.0)
        mu = sum(rets) / len(rets)
        var = sum((r - mu) ** 2 for r in rets) / (len(rets) - 1)
        return -math.sqrt(var)

    xs = []
    ys = []
    for i in range(t - L, t - h + 1):
        xs.append(s_at(i))
        ys.append(c[i + h] / c[i] - 1.0)
    if max(xs) == min(xs) or max(ys) == min(ys):
        return 0.0
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    sxy = 0.0
    sxx = 0.0
    syy = 0.0
    for a, b in zip(xs, ys):
        sxy += (a - mx) * (b - my)
        sxx += (a - mx) ** 2
        syy += (b - my) ** 2
    den = math.sqrt(sxx * syy)
    if not den > 0:
        return 0.0
    r = sxy / den
    return max(-1.0, min(1.0, r))
