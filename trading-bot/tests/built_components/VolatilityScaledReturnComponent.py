"""Spec of VolatilityScaledReturnComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'VolatilityScaledReturnComponent'
SETTINGS = [{}, {"period": 1, "vol_period": 20, "lag": 1}, {"period": 24, "vol_period": 168, "vol_lookback": 720}]


def hand(df, params):
    import math
    p = int(params.get("period", 1))
    vp = int(params.get("vol_period", 20))
    lag = int(params.get("lag", 0))
    lb = int(params.get("vol_lookback", 1))
    c = [float(x) for x in list(df["close"])]
    n = len(c)
    first = n - lag - max(p + 1, vp + lb)
    j = first
    while j <= n - 1 - lag:
        if c[j] != c[j]:
            return float("nan")
        j = j + 1
    e = n - 1 - lag
    ret = c[e] / c[e - p] - 1.0

    def std1(xs):
        mu = sum(xs) / len(xs)
        acc = 0.0
        for x in xs:
            acc = acc + (x - mu) * (x - mu)
        return math.sqrt(acc / (len(xs) - 1))

    total = 0.0
    k = 0
    while k < lb:
        i = e - k
        rets = []
        jj = i - vp + 1
        while jj <= i:
            rets.append(c[jj] / c[jj - 1] - 1.0)
            jj = jj + 1
        total = total + std1(rets)
        k = k + 1
    m = total / lb
    if not m > 0:
        return 0.0
    return ret / (m * math.sqrt(p))
