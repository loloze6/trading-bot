"""Spec of ExcessPowerReversalTimesMaDistanceComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'ExcessPowerReversalTimesMaDistanceComponent'
SETTINGS = [{}, {"high_period": 90, "corr_lookback": 365, "horizon": 5, "z_window": 365, "mean_window": 365, "ma_period": 100}]


def hand(df, params):
    import math
    hp = int(params.get("high_period", 90))
    L = int(params.get("corr_lookback", 365))
    h = int(params.get("horizon", 5))
    zw = int(params.get("z_window", 365))
    mw = int(params.get("mean_window", 365))
    ma = int(params.get("ma_period", 100))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    need = max(max(mw + L, zw - 1) + hp, ma)
    for k in range(need):
        x = c[t - k]
        if x != x or not x > 0:
            return float("nan")

    def s(i):
        m = c[i]
        for j in range(i - hp + 1, i + 1):
            if c[j] > m:
                m = c[j]
        return c[i] / m - 1.0

    def y(i):
        return c[i + h] / c[i] - 1.0

    def mean(xs):
        tot = 0.0
        for x in xs:
            tot += x
        return tot / len(xs)

    def flat(xs):
        return max(xs) == min(xs)

    def w(u):
        a = [s(i) for i in range(u - L, u - h + 1)]
        b = [y(i) for i in range(u - L, u - h + 1)]
        if flat(a) or flat(b):
            return 0.0
        ma_, mb_ = mean(a), mean(b)
        sab = saa = sbb = 0.0
        for k in range(len(a)):
            da = a[k] - ma_
            db = b[k] - mb_
            sab += da * db
            saa += da * da
            sbb += db * db
        if not saa * sbb > 0:
            return 0.0
        return sab / math.sqrt(saa * sbb)

    wt = w(t)
    wbar = mean([w(t - k) for k in range(1, mw + 1)])
    sw = [s(i) for i in range(t - zw + 1, t + 1)]
    if flat(sw):
        z = 0.0
    else:
        m = mean(sw)
        var = 0.0
        for x in sw:
            var += (x - m) * (x - m)
        sd = math.sqrt(var / (len(sw) - 1))
        z = (s(t) - m) / sd if sd > 0 else 0.0
    sma = mean([c[i] for i in range(t - ma + 1, t + 1)])
    dist = (c[t] - sma) / sma * 100.0
    return max(0.0, -(wt - wbar) * z) * max(0.0, dist)
