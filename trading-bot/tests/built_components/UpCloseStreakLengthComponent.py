"""Spec of UpCloseStreakLengthComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'UpCloseStreakLengthComponent'
SETTINGS = [{}, {"max_bars": 30}, {"base": "mean_streak", "base_window": 365}, {"base": "rank", "base_window": 365}, {"side": "down"}]


def hand(df, params):
    mb = int(params.get("max_bars", 30))
    base = params.get("base", "none")
    bw = int(params.get("base_window", 365))
    side = params.get("side", "up")
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    if base == "none":
        need = mb + 1
    else:
        need = max(mb, bw) + 1
    for i in range(t - need + 1, t + 1):
        if c[i] != c[i]:
            return float("nan")

    def mv(i):
        if side == "up":
            return c[i] > c[i - 1]
        return c[i] < c[i - 1]

    n = 0
    i = t
    while n < mb and mv(i):
        n = n + 1
        i = i - 1
    if base == "none":
        return float(n)
    if n == 0:
        return 0.0
    lo = t - bw + 1
    lengths = []
    i = lo
    while i <= t:
        if mv(i):
            j = i
            while j + 1 <= t and mv(j + 1):
                j = j + 1
            before_ok = (i - 1 >= lo) and (not mv(i - 1))
            after_ok = (j + 1 <= t) and (not mv(j + 1))
            if before_ok and after_ok:
                lengths.append(j - i + 1)
            i = j + 1
        else:
            i = i + 1
    if len(lengths) == 0:
        return float("nan")
    if base == "mean_streak":
        total = 0.0
        for L in lengths:
            total = total + L
        return n / (total / len(lengths))
    count = 0
    for L in lengths:
        if L <= n:
            count = count + 1
    return count / len(lengths)
