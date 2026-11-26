"""Spec of PriorBreakoutCloseCountComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'PriorBreakoutCloseCountComponent'
SETTINGS = [{}, {"window": 20, "period": 20}]


def hand(df, params):
    w = int(params.get("window", 20))
    p = int(params.get("period", 20))
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    # rows read: t-w-p .. t-1
    for k in range(t - w - p, t):
        x = closes[k]
        if x != x:
            return float("nan")
    count = 0
    for i in range(t - w, t):
        highest = closes[i - p]
        for j in range(i - p + 1, i):
            if closes[j] > highest:
                highest = closes[j]
        if closes[i] > highest:
            count = count + 1
    return float(count)
