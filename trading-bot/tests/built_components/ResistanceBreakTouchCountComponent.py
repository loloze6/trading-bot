"""Spec of ResistanceBreakTouchCountComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'ResistanceBreakTouchCountComponent'
SETTINGS = [{}, {"period": 90, "side": 2, "band": 2.0, "cross_period": 1}]


def hand(df, params):
    period = int(params.get("period", 90))
    side = int(params.get("side", 2))
    band = float(params.get("band", 2.0))
    cross = int(params.get("cross_period", 1))
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    need = max(period, cross + 1)
    j = t - need + 1
    while j <= t:
        if closes[j] != closes[j]:
            return float("nan")
        j = j + 1
    first = t - period + 1
    swing = []
    i = first + side
    while i <= t - side:
        ok = True
        j = i - side
        while j < i:
            if not closes[i] >= closes[j]:
                ok = False
            j = j + 1
        j = i + 1
        while j <= i + side:
            if not closes[i] > closes[j]:
                ok = False
            j = j + 1
        if ok:
            swing.append(closes[i])
        i = i + 1
    now = closes[t]
    before = closes[t - cross]
    level = None
    for h in swing:
        if before <= h and h < now:
            if level is None or h > level:
                level = h
    if level is None:
        return 0.0
    if not level > 0:
        return float("nan")
    count = 0
    for h in swing:
        if abs(h - level) / level * 100.0 <= band:
            count = count + 1
    return count * (now - level) / level * 100.0
