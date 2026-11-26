"""Spec of PriorDownRunOnUpCloseComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'PriorDownRunOnUpCloseComponent'
SETTINGS = [{}, {"max_bars": 30}, {"max_bars": 30, "form": "beyond_first"}]


def hand(df, params):
    cap = int(params.get("max_bars", 30))
    form = params.get("form", "count")
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    # rows read: bars t-cap-1 .. t
    for k in range(t - cap - 1, t + 1):
        if closes[k] != closes[k]:
            return float("nan")
    if not closes[t] > closes[t - 1]:
        return 0.0
    # count the down closes ending at t-1, walking back
    run = 0
    j = t - 1
    while True:
        if run >= cap:
            break
        if closes[j] < closes[j - 1]:
            run = run + 1
            j = j - 1
        else:
            break
    if form == "beyond_first":
        if run - 1 > 0:
            return float(run - 1)
        return 0.0
    return float(run)
