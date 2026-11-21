"""Spec of ExcessPredictivePowerZComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'ExcessPredictivePowerZComponent'
SETTINGS = [{}, {"high_period": 90, "corr_lookback": 365, "horizon": 5, "z_window": 365, "mean_window": 365}]


def hand(df, params):
    import math
    hp = int(params.get("high_period", 90))
    L = int(params.get("corr_lookback", 365))
    H = int(params.get("horizon", 5))
    Z = int(params.get("z_window", 365))
    M = int(params.get("mean_window", 365))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    need = max(M + L, Z - 1) + hp
    for k in range(t - need + 1, t + 1):
        if c[k] != c[k] or not c[k] > 0:
            return float("nan")

    def near(i):
        m = c[i]
        for j in range(i - hp + 1, i + 1):
            if c[j] > m:
                m = c[j]
        return c[i] / m - 1.0

    def fwd(i):
        return c[i + H] / c[i] - 1.0

    def pearson(xs, ys):
        k = len(xs)
        mx = sum(xs) / k
        my = sum(ys) / k
        sxy = 0.0
        sxx = 0.0
        syy = 0.0
        for a, b in zip(xs, ys):
            sxy += (a - mx) * (b - my)
            sxx += (a - mx) ** 2
            syy += (b - my) ** 2
        if sxx <= 0 or syy <= 0:
            return 0.0
        return sxy / math.sqrt(sxx * syy)

    def power(u):
        rows = list(range(u - L, u - H + 1))
        return pearson([near(i) for i in rows], [fwd(i) for i in rows])

    w_t = power(t)
    past = [power(u) for u in range(t - M, t)]
    wbar = sum(past) / len(past)
    vals = [near(i) for i in range(t - Z + 1, t + 1)]
    mu = sum(vals) / Z
    var = 0.0
    for v in vals:
        var += (v - mu) ** 2
    sd = math.sqrt(var / (Z - 1))
    z = (near(t) - mu) / sd if sd > 0 else 0.0
    return (w_t - wbar) * z
