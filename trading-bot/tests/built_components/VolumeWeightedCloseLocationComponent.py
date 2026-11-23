"""Spec of VolumeWeightedCloseLocationComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'VolumeWeightedCloseLocationComponent'
SETTINGS = [{}, {"volume_period": 20}, {"volume_period": 20, "exclude_current": 1, "reference": "high"}]


def hand(df, params):
    p = int(params.get("volume_period", 20))
    ex = int(params.get("exclude_current", 0))
    ref = params.get("reference", "signed")
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    vols = [float(x) for x in list(df["volume"])]
    t = len(closes) - 1
    h = highs[t]
    l = lows[t]
    c = closes[t]
    v_t = vols[t]
    # base: the p volumes ending ex bars before t
    base = []
    for k in range(p):
        base.append(vols[t - ex - k])
    for x in [h, l, c, v_t] + base:
        if x != x:
            return float("nan")
    total = 0.0
    for x in base:
        total = total + x
    mean_base = total / p
    if not mean_base > 0:
        return float("nan")
    rng = h - l
    if ref == "high":
        if rng == 0:
            loc = 0.5
        else:
            loc = (h - c) / rng
    elif ref == "low":
        if rng == 0:
            loc = 0.5
        else:
            loc = (c - l) / rng
    else:
        if rng == 0:
            loc = 0.0
        else:
            loc = 2.0 * (c - l) / rng - 1.0
    return loc * (v_t / mean_base)
