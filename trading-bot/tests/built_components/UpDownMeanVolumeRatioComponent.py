"""Spec of UpDownMeanVolumeRatioComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'UpDownMeanVolumeRatioComponent'
SETTINGS = [{}, {"period": 20, "form": "ratio"}]


def hand(df, params):
    import math
    p = int(params.get("period", 20))
    form = params.get("form", "ratio")
    close = [float(x) for x in list(df["close"])]
    vol = [float(x) for x in list(df["volume"])]
    t = len(close) - 1
    up_sum = 0.0
    up_n = 0
    dn_sum = 0.0
    dn_n = 0
    for i in range(t - p + 1, t + 1):
        a = close[i - 1]
        b = close[i]
        w = vol[i]
        if a != a or b != b or w != w:
            return float("nan")
        if b > a:
            up_sum += w
            up_n += 1
        elif b < a:
            dn_sum += w
            dn_n += 1
    if up_n == 0 or dn_n == 0:
        return float("nan")
    mu = up_sum / up_n
    md = dn_sum / dn_n
    if not (mu > 0 and md > 0):
        return float("nan")
    r = mu / md
    if form == "log":
        return math.log(r)
    if form == "centred":
        return r - 1.0
    return r
