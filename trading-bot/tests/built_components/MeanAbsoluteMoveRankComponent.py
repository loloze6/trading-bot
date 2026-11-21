"""Spec of MeanAbsoluteMoveRankComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'MeanAbsoluteMoveRankComponent'
SETTINGS = [{}, {"period": 168, "lookback": 720}]


def hand(df, params):
    p = int(params.get("period", 168))
    lb = int(params.get("lookback", 720))
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    first = last - (p + lb) + 1
    for i in range(first, last + 1):
        if c[i] != c[i] or not c[i] > 0:
            return float("nan")

    def mean_abs_move(i):
        total = 0.0
        for j in range(i - p + 1, i + 1):
            total = total + abs(c[j] / c[j - 1] - 1.0)
        return total / p

    current = mean_abs_move(last)
    count = 0
    for i in range(last - lb + 1, last + 1):
        if mean_abs_move(i) <= current:
            count = count + 1
    return count / lb
