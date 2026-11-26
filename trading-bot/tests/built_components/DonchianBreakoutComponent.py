"""Spec of DonchianBreakoutComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'DonchianBreakoutComponent'
SETTINGS = [{}, {"period": 30, "source": "high_low", "scaling_factor": 1.0}, {"period": 30, "source": "high_low", "form": "below_proximity"}, {"period": 20, "scaling_factor": 1.0, "source": "high_low", "form": "position", "exclude_current": 1}]


def hand(df, params):
    p = int(params.get("period", 48))
    sf = float(params.get("scaling_factor", 20.0))
    source = params.get("source", "close")
    form = params.get("form", "position")
    ex = int(params.get("exclude_current", 0))
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    # window: bars t-ex-p+1 .. t-ex
    idx = [t - ex - k for k in range(p)]
    if source == "close":
        his = [closes[i] for i in idx]
        los = [closes[i] for i in idx]
    else:
        highs = [float(x) for x in list(df["high"])]
        lows = [float(x) for x in list(df["low"])]
        his = [highs[i] for i in idx]
        los = [lows[i] for i in idx]
    c = closes[t]
    for x in his + los + [c]:
        if x != x:
            return float("nan")
    H = his[0]
    for x in his:
        if x > H:
            H = x
    L = los[0]
    for x in los:
        if x < L:
            L = x
    if form == "position":
        if H - L == 0:
            pos = 0.5
        else:
            pos = (c - L) / (H - L)
        return (2.0 * pos - 1.0) * sf
    mid = (H + L) / 2.0
    if not mid > 0:
        return float("nan")
    if c < mid:
        D = (mid - c) / mid * 100.0
        return 1.0 / (1.0 + D)
    return 0.0
