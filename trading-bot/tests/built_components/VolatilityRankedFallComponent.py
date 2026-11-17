"""Spec of VolatilityRankedFallComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'VolatilityRankedFallComponent'
SETTINGS = [{}, {"vol_period": 20, "lookback": 120}]


def hand(df, params):
    import math
    m = int(params.get("vol_period", 20))
    L = int(params.get("lookback", 120))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    first = t - L - m + 1
    i = first
    while i <= t:
        if c[i] != c[i]:
            return float("nan")
        i = i + 1

    def ret(j):
        return c[j] / c[j - 1] - 1.0

    def sd(i):
        xs = []
        j = i - m + 1
        while j <= i:
            xs.append(ret(j))
            j = j + 1
        mean = 0.0
        for x in xs:
            mean = mean + x
        mean = mean / m
        ss = 0.0
        for x in xs:
            ss = ss + (x - mean) * (x - mean)
        return math.sqrt(ss / (m - 1))

    s_now = sd(t)
    if not s_now > 0:
        return float("nan")
    count = 0
    i = t - L + 1
    while i <= t:
        if sd(i) <= s_now:
            count = count + 1
        i = i + 1
    rank = count / L
    z = -ret(t) / s_now
    if z < 0:
        z = 0.0
    return z * rank
