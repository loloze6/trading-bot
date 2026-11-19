"""Spec of VolumeRatioComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'VolumeRatioComponent'
SETTINGS = [{}, {"period": 30}, {"period": 10}, {"period": 2}, {"period": 20, "exclude_current": 1}, {"period": 30, "short_period": 5, "form": "centred"}, {"period": 30, "form": "log"}, {"period": 20, "exclude_current": 1, "statistic": "median"}, {"period": 72, "short_period": 72, "short_statistic": "median"}]


def hand(df, params):
    import math
    n = int(params.get("period", 30))
    ex = int(params.get("exclude_current", 0))
    s = int(params.get("short_period", 1))
    form = params.get("form", "ratio")
    st = params.get("statistic", "mean")
    sst = params.get("short_statistic", "mean")
    v = [float(x) for x in list(df["volume"])]
    last = len(v) - 1

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

    recent = []
    i = last - s + 1
    while i <= last:
        recent.append(v[i])
        i = i + 1
    base = []
    if ex == 1:
        i = last - n
        while i <= last - 1:
            base.append(v[i])
            i = i + 1
    else:
        i = last - n + 1
        while i <= last:
            base.append(v[i])
            i = i + 1
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
    return ratio - (1.0 if form == "centred" else 0.0)
