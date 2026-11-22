"""Spec of DownStreakVolumeFadeComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'DownStreakVolumeFadeComponent'
SETTINGS = [{}, {"max_bars": 180}, {"side": "up", "statistic": "log_ratio"}, {"side": "down", "statistic": "log_slope"}]


def hand(df, params):
    import math
    max_bars = int(params.get("max_bars", 180))
    side = params.get("side", "down")
    statistic = params.get("statistic", "slope")
    closes = [float(x) for x in list(df["close"])]
    vols = [float(x) for x in list(df["volume"])]
    last = len(closes) - 1
    first_row = last - max_bars
    for i in range(first_row, last + 1):
        if closes[i] != closes[i]:
            return float("nan")
    n = 0
    i = last
    while n < max_bars:
        if side == "down":
            ok = closes[i] < closes[i - 1]
        else:
            ok = closes[i] > closes[i - 1]
        if not ok:
            break
        n = n + 1
        i = i - 1
    if n < 2:
        return 0.0
    v = vols[last - n + 1: last + 1]
    xs = [float(k) for k in range(n)]
    xbar = sum(xs) / n

    def ls_slope(ys):
        ybar = sum(ys) / n
        num = 0.0
        den = 0.0
        for k in range(n):
            num = num + (xs[k] - xbar) * (ys[k] - ybar)
            den = den + (xs[k] - xbar) * (xs[k] - xbar)
        return num / den

    if statistic == "log_ratio":
        a = v[0]
        z = v[-1]
        if a != a or z != z or not a > 0 or not z > 0:
            return float("nan")
        return math.log(a / z)
    for x in v:
        if x != x:
            return float("nan")
    if statistic == "log_slope":
        for x in v:
            if not x > 0:
                return float("nan")
        return -ls_slope([math.log(x) for x in v])
    vbar = sum(v) / n
    if not vbar > 0:
        return float("nan")
    return -ls_slope(v) / vbar
