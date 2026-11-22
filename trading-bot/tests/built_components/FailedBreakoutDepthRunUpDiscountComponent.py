"""Spec of FailedBreakoutDepthRunUpDiscountComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'FailedBreakoutDepthRunUpDiscountComponent'
SETTINGS = [{}, {"period": 20, "fail_window": 10, "rise_period": 20, "window": 120}]


def hand(df, params):
    p = int(params.get("period", 20))
    fw = int(params.get("fail_window", 10))
    rp = int(params.get("rise_period", 20))
    w = int(params.get("window", 120))
    need = max(p + fw, rp + fw, w + rp)
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    for k in range(need):
        x = closes[t - k]
        if x != x or not x > 0:
            return float("nan")
    # most recent breakout bar j in t-fw+1 .. t
    j = -1
    old_high = 0.0
    k = 0
    while k < fw:
        cand = t - k
        hi = closes[cand - 1]
        q = 2
        while q <= p:
            if closes[cand - q] > hi:
                hi = closes[cand - q]
            q += 1
        if closes[cand] > hi:
            j = cand
            old_high = hi
            break
        k += 1
    if j < 0:
        return 0.0
    if closes[t] >= old_high:
        return 0.0
    depth = (old_high - closes[t]) / old_high * 100.0
    total = 0.0
    for i in range(t - w + 1, t + 1):
        total += abs(closes[i] / closes[i - rp] - 1.0)
    m = total / w
    if m == 0:
        return 0.0
    run_up = closes[j] / closes[j - rp] - 1.0
    weight = 1.0 - run_up / m
    if weight < 0:
        weight = 0.0
    return depth * weight
