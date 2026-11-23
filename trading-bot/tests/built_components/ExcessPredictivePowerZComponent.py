"""Spec of ExcessPredictivePowerZComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'ExcessPredictivePowerZComponent'
SETTINGS = [{}, {"high_period": 90, "corr_lookback": 365, "horizon": 5, "z_window": 365, "mean_window": 365}, {"signal": "volatility", "vol_period": 30, "corr_lookback": 365, "horizon": 5, "z_window": 365, "mean_window": 365}]


def hand(df, params):
    import math
    hp = int(params.get("high_period", 90))
    L = int(params.get("corr_lookback", 365))
    h = int(params.get("horizon", 5))
    zw = int(params.get("z_window", 365))
    mw = int(params.get("mean_window", 365))
    sig = params.get("signal", "high")
    vp = int(params.get("vol_period", 30))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    D = hp - 1 if sig == "high" else vp
    need = max(mw + L, zw - 1) + D + 1
    for x in c[t - need + 1:]:
        if x != x or not x > 0:
            return float("nan")

    memo = {}

    def s(i):
        if i in memo:
            return memo[i]
        if sig == "high":
            m = c[i]
            for k in range(i - hp + 1, i + 1):
                if c[k] > m:
                    m = c[k]
            v = c[i] / m - 1.0
        else:
            rets = []
            for j in range(i - vp + 1, i + 1):
                rets.append(c[j] / c[j - 1] - 1.0)
            mu = sum(rets) / len(rets)
            var = 0.0
            for r in rets:
                var += (r - mu) ** 2
            var = var / (len(rets) - 1)
            v = -math.sqrt(var)
        memo[i] = v
        return v

    def corr(xs, ys):
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
        if not sxx * syy > 0:
            return 0.0
        return sxy / math.sqrt(sxx * syy)

    def w(u):
        xs = []
        ys = []
        for i in range(u - L, u - h + 1):
            xs.append(s(i))
            ys.append(c[i + h] / c[i] - 1.0)
        return corr(xs, ys)

    total = 0.0
    for u in range(t - mw, t):
        total += w(u)
    wbar = total / mw

    vals = [s(i) for i in range(t - zw + 1, t + 1)]
    if max(vals) == min(vals):
        z = 0.0
    else:
        mu = sum(vals) / len(vals)
        var = 0.0
        for v in vals:
            var += (v - mu) ** 2
        sd = math.sqrt(var / (len(vals) - 1))
        z = (s(t) - mu) / sd if sd > 0 else 0.0

    return (w(t) - wbar) * z
