"""Spec of DownBarVolumeFadeComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'DownBarVolumeFadeComponent'
SETTINGS = [{}, {"short_period": 10, "base_period": 20}]


def hand(df, params):
    import math
    s = int(params.get("short_period", 10))
    b = int(params.get("base_period", 20))
    c = [float(x) for x in list(df["close"])]
    v = [float(x) for x in list(df["volume"])]
    t = len(c) - 1
    # closes read: bars t-s-b .. t; volumes read: bars t-s-b+1 .. t
    for i in range(t - s - b, t + 1):
        if c[i] != c[i]:
            return float("nan")
    for i in range(t - s - b + 1, t + 1):
        if v[i] != v[i]:
            return float("nan")
    recent = []
    for i in range(t - s + 1, t + 1):
        if c[i] < c[i - 1]:
            recent.append(v[i])
    base = []
    for i in range(t - s - b + 1, t - s + 1):
        if c[i] < c[i - 1]:
            base.append(v[i])
    if len(recent) == 0 or len(base) == 0:
        return 0.0
    a_mean = sum(recent) / len(recent)
    b_mean = sum(base) / len(base)
    if not a_mean > 0 or not b_mean > 0:
        return float("nan")
    return math.log(b_mean / a_mean)
