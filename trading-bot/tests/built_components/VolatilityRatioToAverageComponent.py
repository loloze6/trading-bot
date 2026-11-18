"""Spec of VolatilityRatioToAverageComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'VolatilityRatioToAverageComponent'
SETTINGS = [{}, {"vol_period": 20, "vol_lookback": 60}]


def hand(df, params):
    import math
    p = int(params.get("vol_period", 20))
    L = int(params.get("vol_lookback", 60))
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    i = last - (L + p) + 1
    while i <= last:
        if c[i] != c[i]:
            return float("nan")
        i = i + 1

    def sd(bar):
        rets = []
        j = bar - p + 1
        while j <= bar:
            rets.append(c[j] / c[j - 1] - 1.0)
            j = j + 1
        mu = sum(rets) / p
        acc = 0.0
        for x in rets:
            acc = acc + (x - mu) * (x - mu)
        return math.sqrt(acc / (p - 1))

    vals = []
    b = last - L + 1
    while b <= last:
        vals.append(sd(b))
        b = b + 1
    avg = sum(vals) / L
    if not avg > 0:
        return float("nan")
    return sd(last) / avg
