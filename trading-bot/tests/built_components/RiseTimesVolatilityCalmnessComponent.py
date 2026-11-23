"""Spec of RiseTimesVolatilityCalmnessComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'RiseTimesVolatilityCalmnessComponent'
SETTINGS = [{}, {"period": 24, "lag": 24, "vol_period": 720, "vol_lookback": 8760}]


def hand(df, params):
    import math
    period = int(params.get("period", 24))
    lag = int(params.get("lag", 24))
    vp = int(params.get("vol_period", 720))
    vl = int(params.get("vol_lookback", 8760))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    need = max(period + lag + 1, vl + vp)
    rows = c[t - need + 1:]
    for x in rows:
        if x != x or not x > 0:
            return float("nan")

    def ret(j):
        return c[j] / c[j - 1] - 1.0

    def std_at(i):
        xs = [ret(j) for j in range(i - vp + 1, i + 1)]
        m = sum(xs) / len(xs)
        ss = 0.0
        for x in xs:
            ss += (x - m) * (x - m)
        return math.sqrt(ss / (len(xs) - 1))

    rise = c[t - lag] / c[t - lag - period] - 1.0
    if rise < 0:
        rise = 0.0
    total = 0.0
    for i in range(t - vl + 1, t + 1):
        total += std_at(i)
    mean_s = total / vl
    s_t = std_at(t)
    if not s_t > 0:
        return float("nan")
    return rise * mean_s / s_t
