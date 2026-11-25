"""Spec of ScaledFallRangeMultipleComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'ScaledFallRangeMultipleComponent'
SETTINGS = [{}, {"period": 6, "lag": 6, "window": 180}, {"period": 1, "lag": 0, "window": 30, "scale": "std"}]


def hand(df, params):
    import math
    period = int(params.get("period", 6))
    lag = int(params.get("lag", 6))
    window = int(params.get("window", 180))
    scale = params.get("scale", "mean_abs")
    c = [float(x) for x in list(df["close"])]
    h = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    t = len(c) - 1
    e = t - lag
    # closes read: e-window-period+1 .. e ; highs/lows read: e-window-period+2 .. e
    for k in range(e - window - period + 1, e + 1):
        if c[k] != c[k]:
            return float("nan")
    for k in range(e - window - period + 2, e + 1):
        if h[k] != h[k] or lo[k] != lo[k]:
            return float("nan")
    for k in range(e - window - period + 1, e + 1):
        if not c[k] > 0:
            return float("nan")
    rets = []
    rngs = []
    for i in range(e - window + 1, e + 1):
        rets.append(c[i] / c[i - period] - 1.0)
        top = h[i - period + 1]
        bot = lo[i - period + 1]
        for k in range(i - period + 1, i + 1):
            if h[k] > top:
                top = h[k]
            if lo[k] < bot:
                bot = lo[k]
        rngs.append(top - bot)
    count = len(rets)
    if scale == "std":
        mu = sum(rets) / count
        ss = 0.0
        for x in rets:
            ss += (x - mu) * (x - mu)
        m = math.sqrt(ss / (count - 1))
    else:
        m = sum(abs(x) for x in rets) / count
    b = sum(rngs) / len(rngs)
    if m == 0 or b == 0:
        return 0.0
    fall = -(c[e] / c[e - period] - 1.0)
    if fall < 0:
        fall = 0.0
    return fall / m * rngs[-1] / b
