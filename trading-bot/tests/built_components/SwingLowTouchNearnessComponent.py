"""Spec of SwingLowTouchNearnessComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'SwingLowTouchNearnessComponent'
SETTINGS = [{}, {"period": 90, "side": 2, "band": 1.5, "fall_period": 5}]


def hand(df, params):
    period = int(params.get("period", 90))
    side = int(params.get("side", 2))
    band = float(params.get("band", 1.5))
    fall_period = int(params.get("fall_period", 5))
    low_all = [float(x) for x in list(df["low"])]
    close_all = [float(x) for x in list(df["close"])]
    last = len(close_all) - 1
    close_t = close_all[last]
    close_before = close_all[last - fall_period]
    window = low_all[len(low_all) - period:]
    for x in window:
        if x != x:
            return float("nan")
    if close_t != close_t or close_before != close_before:
        return float("nan")
    if not close_t > 0:
        return float("nan")
    if not close_t < close_before:
        return 0.0
    result = 0.0
    i = side
    while i <= period - 1 - side:
        is_swing = True
        j = i - side
        while j <= i + side:
            if j != i and not window[i] < window[j]:
                is_swing = False
            j = j + 1
        if is_swing:
            distance_pct = abs(close_t - window[i]) / close_t * 100.0
            nearness = 1.0 - distance_pct / band
            if nearness > 0:
                result = result + nearness
        i = i + 1
    return result
