"""Spec of VolumeRatioComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'VolumeRatioComponent'
SETTINGS = [{}, {"period": 30}, {"period": 10}, {"period": 2}, {"period": 20, "exclude_current": 1}, {"period": 30, "short_period": 5, "form": "centred"}, {"period": 30, "form": "log"}, {"period": 20, "exclude_current": 1, "statistic": "median"}, {"period": 72, "short_period": 72, "short_statistic": "median"}, {"period": 120, "exclude_current": 49, "short_period": 48}]


def hand(df, params):
    import math
    n = int(params.get("period", 30))
    lag = int(params.get("exclude_current", 0))
    s = int(params.get("short_period", 1))
    form = params.get("form", "ratio")
    st = params.get("statistic", "mean")
    sst = params.get("short_statistic", "mean")
    v = [float(x) for x in list(df["volume"])]
    t = len(v) - 1

    def median_of(xs):
        srt = sorted(xs)
        m = len(srt)
        if m % 2 == 1:
            return srt[m // 2]
        return (srt[m // 2 - 1] + srt[m // 2]) / 2.0

    def mean_of(xs):
        total = 0.0
        for x in xs:
            total = total + x
        return total / len(xs)

    # recent: bars t-s+1 .. t
    recent = []
    for k in range(s):
        recent.append(v[t - k])
    # base: the n bars ending lag bars before t, i.e. t-lag-n+1 .. t-lag
    base = []
    for k in range(n):
        base.append(v[t - lag - k])
    for x in recent + base:
        if x != x:
            return float("nan")
    num = median_of(recent) if sst == "median" else mean_of(recent)
    den = median_of(base) if st == "median" else mean_of(base)
    if not den > 0:
        return float("nan")
    ratio = num / den
    if form == "log":
        if not ratio > 0:
            return float("nan")
        return math.log(ratio)
    if form == "centred":
        return ratio - 1.0
    return ratio
