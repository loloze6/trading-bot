"""Spec of FallVolumeTimesPriorDeclineComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'FallVolumeTimesPriorDeclineComponent'
SETTINGS = [{}, {"vol_period": 20, "volume_period": 20, "decline_period": 20}]


def hand(df, params):
    import math
    vp = int(params.get("vol_period", 20))
    volp = int(params.get("volume_period", 20))
    dp = int(params.get("decline_period", 20))
    c = [float(x) for x in list(df["close"])]
    v = [float(x) for x in list(df["volume"])]
    t = len(c) - 1

    # closes read: bars t-vp .. t (returns) and bar t-1-dp (decline base)
    first = min(t - vp, t - 1 - dp)
    for i in range(first, t + 1):
        x = c[i]
        if x != x or not x > 0:
            return float("nan")
    # volumes read: bars t-volp .. t
    for i in range(t - volp, t + 1):
        if v[i] != v[i]:
            return float("nan")

    # std (ddof 1) of the vp one-bar returns ending at bar t
    rets = []
    for j in range(t - vp + 1, t + 1):
        rets.append(c[j] / c[j - 1] - 1.0)
    mu = sum(rets) / len(rets)
    ss = 0.0
    for r in rets:
        ss += (r - mu) ** 2
    s = math.sqrt(ss / (len(rets) - 1))

    today = c[t] / c[t - 1] - 1.0
    fall = 0.0
    if today < 0 and s > 0:
        fall = -today / s

    total = 0.0
    for i in range(t - volp, t):
        total += v[i]
    base = total / volp
    if not base > 0:
        return float("nan")
    vr = v[t] / base

    prior = c[t - 1] / c[t - 1 - dp] - 1.0
    decline = -prior * 100.0 if prior < 0 else 0.0

    return fall * vr * decline
