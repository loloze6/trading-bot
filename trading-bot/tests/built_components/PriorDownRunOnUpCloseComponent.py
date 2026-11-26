"""Spec of PriorDownRunOnUpCloseComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'PriorDownRunOnUpCloseComponent'
SETTINGS = [{}, {"max_bars": 30}]


def hand(df, params):
    cap = int(params.get("max_bars", 30))
    close = [float(x) for x in list(df["close"])]
    t = len(close) - 1
    # rows read: t-cap-1 .. t
    for k in range(cap + 2):
        x = close[t - k]
        if x != x:
            return float("nan")
    # bar t must close strictly above bar t-1
    if not (close[t] > close[t - 1]):
        return 0.0
    # count the down bars going back from t-1
    count = 0
    j = t - 1
    while count < cap:
        if close[j] < close[j - 1]:
            count = count + 1
            j = j - 1
        else:
            break
    return float(count)
