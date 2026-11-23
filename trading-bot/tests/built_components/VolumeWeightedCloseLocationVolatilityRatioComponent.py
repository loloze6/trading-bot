"""Spec of VolumeWeightedCloseLocationVolatilityRatioComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'VolumeWeightedCloseLocationVolatilityRatioComponent'
SETTINGS = [{}, {"volume_period": 20, "vol_period": 20, "vol_lookback": 60}]


def hand(df, params):
    import math
    vp = int(params.get("volume_period", 20))
    sp = int(params.get("vol_period", 20))
    L = int(params.get("vol_lookback", 60))
    high = [float(x) for x in list(df["high"])]
    low = [float(x) for x in list(df["low"])]
    close = [float(x) for x in list(df["close"])]
    volume = [float(x) for x in list(df["volume"])]
    t = len(close) - 1

    def isnan(x):
        return x != x

    # location of the close from the bar's high
    if isnan(high[t]) or isnan(low[t]) or isnan(close[t]):
        return float("nan")
    rng = high[t] - low[t]
    if rng == 0:
        loc = 0.5
    else:
        loc = (high[t] - close[t]) / rng

    # volume today against the mean of the prior vp volumes
    if isnan(volume[t]):
        return float("nan")
    total = 0.0
    for i in range(t - vp, t):
        if isnan(volume[i]):
            return float("nan")
        total += volume[i]
    base_mean = total / vp
    if not base_mean > 0:
        return float("nan")
    vr = volume[t] / base_mean

    # closes used: bars t-L-sp+1 .. t
    for i in range(t - L - sp + 1, t + 1):
        if isnan(close[i]) or not close[i] > 0:
            return float("nan")

    def sd_at(i):
        rets = []
        for j in range(i - sp + 1, i + 1):
            rets.append(close[j] / close[j - 1] - 1.0)
        m = sum(rets) / len(rets)
        ss = 0.0
        for x in rets:
            ss += (x - m) * (x - m)
        return math.sqrt(ss / (len(rets) - 1))

    svals = []
    for i in range(t - L + 1, t + 1):
        svals.append(sd_at(i))
    s_mean = sum(svals) / len(svals)
    if not s_mean > 0:
        return float("nan")
    volr = sd_at(t) / s_mean

    return loc * vr * volr
