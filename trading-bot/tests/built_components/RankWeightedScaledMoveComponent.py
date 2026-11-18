"""Spec of RankWeightedScaledMoveComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'RankWeightedScaledMoveComponent'
SETTINGS = [{}, {"abs_period": 60, "vol_period": 20, "lookback": 100}]


def hand(df, params):
    ap = int(params.get("abs_period", 60))
    vp = int(params.get("vol_period", 20))
    lb = int(params.get("lookback", 100))
    closes = [float(x) for x in list(df["close"])]
    need = max(lb + vp, ap + 1)
    window = closes[len(closes) - need:]
    for x in window:
        if x != x:
            return float("nan")
    t = len(closes) - 1

    def ret(j):
        return closes[j] / closes[j - 1] - 1.0

    total = 0.0
    j = t - ap + 1
    while j <= t:
        total = total + abs(ret(j))
        j = j + 1
    m = total / ap
    if m == 0:
        move = 0.0
    else:
        move = ret(t) / m

    def sd(i):
        vals = []
        j = i - vp + 1
        while j <= i:
            vals.append(ret(j))
            j = j + 1
        mu = sum(vals) / len(vals)
        ss = 0.0
        for v in vals:
            ss = ss + (v - mu) * (v - mu)
        return (ss / (len(vals) - 1)) ** 0.5

    s_t = sd(t)
    count = 0
    i = t - lb + 1
    while i <= t:
        if sd(i) <= s_t:
            count = count + 1
        i = i + 1
    rank = count / lb
    return move * (1.0 - rank)
