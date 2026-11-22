"""Spec of FailedBreakoutExcursionComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'FailedBreakoutExcursionComponent'
SETTINGS = [{}, {"period": 20, "fail_window": 4}, {"period": 20, "fail_window": 4, "peak_source": "close"}]


def hand(df, params):
    period = int(params.get("period", 20))
    fw = int(params.get("fail_window", 4))
    src = params.get("peak_source", "high")
    c = [float(x) for x in list(df["close"])]
    hi = [float(x) for x in list(df["high"])]
    t = len(c) - 1
    # every close read: bars t-fw+1-period .. t
    for i in range(t - fw + 1 - period, t + 1):
        if c[i] != c[i]:
            return float("nan")
    j = -1
    old = 0.0
    for d in range(fw):
        cand = t - d
        best = c[cand - 1]
        for i in range(cand - period, cand):
            if c[i] > best:
                best = c[i]
        if c[cand] > best:
            j = cand
            old = best
            break
    if j < 0:
        return 0.0
    if not old > 0:
        return float("nan")
    if not c[t] < old:
        return 0.0
    peak = None
    for i in range(j, t + 1):
        v = hi[i] if src == "high" else c[i]
        if v != v:
            return float("nan")
        if peak is None or v > peak:
            peak = v
    return (peak - old) / old * 100.0
