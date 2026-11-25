"""Spec of PriorLowReclaimInRangeComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'PriorLowReclaimInRangeComponent'
SETTINGS = [{}, {"period": 30}, {"period": 30, "form": "nearness"}]


def hand(df, params):
    n = int(params.get("period", 30))
    form = params.get("form", "reclaim")
    lo = [float(x) for x in list(df["low"])]
    hi = [float(x) for x in list(df["high"])]
    cl = [float(x) for x in list(df["close"])]
    t = len(cl) - 1
    # prior low over bars t-n .. t-1
    prior = []
    for k in range(1, n + 1):
        prior.append(lo[t - k])
    vals = prior + [lo[t], hi[t], cl[t]]
    for x in vals:
        if x != x:
            return float("nan")
    L = prior[0]
    for x in prior:
        if x < L:
            L = x
    low_t = lo[t]
    high_t = hi[t]
    close_t = cl[t]
    rng = high_t - low_t
    if not (low_t < L and L < close_t) or not rng > 0:
        return 0.0
    reclaim_share = (close_t - L) / rng
    if form == "nearness":
        return 1.0 - reclaim_share
    return reclaim_share
