"""Spec of DownDayVolumeShareComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'DownDayVolumeShareComponent'
SETTINGS = [{}, {"period": 10, "form": "share"}]


def hand(df, params):
    n = int(params.get("period", 10))
    form = params.get("form", "share")
    c = [float(x) for x in list(df["close"])]
    v = [float(x) for x in list(df["volume"])]
    t = len(c) - 1
    down_total = 0.0
    total = 0.0
    for i in range(t - n + 1, t + 1):
        ci = c[i]
        cp = c[i - 1]
        vi = v[i]
        if ci != ci or cp != cp or vi != vi:
            return float("nan")
        total = total + vi
        if ci < cp:
            down_total = down_total + vi
    if not total > 0:
        return float("nan")
    share = down_total / total
    if form == "centred":
        return share - 0.5
    return share
