"""Spec of UpDayVolumeShareComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'UpDayVolumeShareComponent'
SETTINGS = [{}, {"period": 20, "form": "share"}, {"period": 20, "base": "mean_volume", "base_period": 60}]


def hand(df, params):
    p = int(params.get("period", 20))
    form = params.get("form", "share")
    base = params.get("base", "window")
    bp = int(params.get("base_period", 60))
    closes = [float(x) for x in list(df["close"])]
    vols = [float(x) for x in list(df["volume"])]
    t = len(closes) - 1
    # up-day volume over bars t-p+1 .. t
    U = 0.0
    total = 0.0
    for i in range(t - p + 1, t + 1):
        ci = closes[i]
        cp = closes[i - 1]
        vi = vols[i]
        if ci != ci or cp != cp or vi != vi:
            return float("nan")
        total += vi
        if ci > cp:
            U += vi
    if base == "mean_volume":
        s = 0.0
        for i in range(t - bp + 1, t + 1):
            if vols[i] != vols[i]:
                return float("nan")
            s += vols[i]
        D = s / bp
    else:
        D = total
    if not D > 0:
        return float("nan")
    val = U / D
    if form == "centred":
        val -= 0.5
    return val
