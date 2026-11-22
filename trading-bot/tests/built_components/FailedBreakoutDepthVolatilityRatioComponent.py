"""Spec of FailedBreakoutDepthVolatilityRatioComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'FailedBreakoutDepthVolatilityRatioComponent'
SETTINGS = [{}, {"period": 20, "fail_window": 3, "exclude_current": 1, "vol_period": 20, "base_vol_period": 60}]


def hand(df, params):
    import math
    period = int(params.get("period", 20))
    fw = int(params.get("fail_window", 3))
    ex = int(params.get("exclude_current", 1))
    vp = int(params.get("vol_period", 20))
    bvp = int(params.get("base_vol_period", 60))
    closes = [float(x) for x in list(df["close"])]
    need = max(period + fw + ex, vp + 1, bvp + 1)
    rows = closes[len(closes) - need:]
    for x in rows:
        if x != x or not x > 0:
            return float("nan")
    t = len(closes) - 1

    # breakout search: most recent bar first
    if ex == 1:
        candidates = list(range(t - 1, t - fw - 1, -1))
    else:
        candidates = list(range(t, t - fw, -1))
    old_high = None
    for j in candidates:
        prior = closes[j - period:j]
        top = prior[0]
        for x in prior:
            if x > top:
                top = x
        if closes[j] > top:
            old_high = top
            break
    depth = 0.0
    if old_high is not None:
        if not old_high > 0:
            return float("nan")
        gap = old_high - closes[t]
        if gap < 0:
            gap = 0.0
        depth = gap / old_high * 100.0

    def sample_std(m):
        rets = []
        for i in range(t - m + 1, t + 1):
            rets.append(closes[i] / closes[i - 1] - 1.0)
        mean = sum(rets) / len(rets)
        ss = 0.0
        for x in rets:
            ss += (x - mean) ** 2
        return math.sqrt(ss / (len(rets) - 1))

    s_recent = sample_std(vp)
    s_base = sample_std(bvp)
    if s_recent == 0.0:
        return 0.0
    return depth * s_base / s_recent
