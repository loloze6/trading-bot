"""Spec of BreakoutRunUpDiscountComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'BreakoutRunUpDiscountComponent'
SETTINGS = [{}, {"period": 60, "rise_period": 20, "rise_lag": 1, "window": 120}]


def hand(df, params):
    period = int(params.get("period", 60))
    rp = int(params.get("rise_period", 20))
    lag = int(params.get("rise_lag", 1))
    window = int(params.get("window", 120))
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    need = max(period + 1, window + rp, lag + rp + 1)
    used = closes[t - need + 1:]
    for x in used:
        if x != x or not x > 0:
            return float("nan")
    # breakout: close[t] strictly above each of the prior `period` closes
    high = closes[t - 1]
    for k in range(1, period + 1):
        if closes[t - k] > high:
            high = closes[t - k]
    broke = closes[t] > high
    # usual rise_period-bar move: mean abs return ending at each of the last `window` bars
    total = 0.0
    for i in range(t - window + 1, t + 1):
        ret = closes[i] / closes[i - rp] - 1.0
        total += ret if ret >= 0 else -ret
    m = total / window
    run_up = closes[t - lag] / closes[t - lag - rp] - 1.0
    if not broke or m == 0.0:
        return 0.0
    w = 1.0 - run_up / m
    return w if w > 0 else 0.0
