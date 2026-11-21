"""Spec of PastPredictivePowerWeightedCompositeComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'PastPredictivePowerWeightedCompositeComponent'
SETTINGS = [{}, {"return_period": 28, "reversal_period": 1, "high_period": 90, "vol_period": 30, "z_window": 365, "corr_lookback": 365, "horizon": 5}, {"weighting": "regression", "return_period": 28, "reversal_period": 1, "high_period": 90, "vol_period": 30, "corr_lookback": 365, "horizon": 5}, {"return_period": 28, "reversal_period": 1, "high_period": 90, "vol_period": 30, "z_window": 365, "corr_lookback": 365, "horizon": 5, "weighting": "best"}, {"weighting": "single", "signal": "momentum"}]


def hand(df, params):
    import math
    p1 = int(params.get("return_period", 28))
    p2 = int(params.get("reversal_period", 1))
    p3 = int(params.get("high_period", 90))
    p4 = int(params.get("vol_period", 30))
    Z = int(params.get("z_window", 365))
    C = int(params.get("corr_lookback", 365))
    h = int(params.get("horizon", 5))
    wt = params.get("weighting", "correlation")
    sig = params.get("signal", "momentum")
    names = ["momentum", "reversal", "high", "volatility"]

    allc = [float(x) for x in list(df["close"])]
    lag = max(p1, p2, p3 - 1, p4)
    need = max(Z - 1, C) + lag + 1
    c = allc[len(allc) - need:]
    for x in c:
        if x != x or not x > 0:
            return float("nan")
    t = len(c) - 1

    def mean(xs):
        s = 0.0
        for x in xs:
            s += x
        return s / len(xs)

    def sd1(xs):
        m = mean(xs)
        s = 0.0
        for x in xs:
            s += (x - m) * (x - m)
        return math.sqrt(s / (len(xs) - 1))

    def value(k, i):
        if k == 0:
            return c[i] / c[i - p1] - 1.0
        if k == 1:
            return -(c[i] / c[i - p2] - 1.0)
        if k == 2:
            hi = c[i]
            for j in range(i - p3 + 1, i + 1):
                if c[j] > hi:
                    hi = c[j]
            return c[i] / hi - 1.0
        rets = []
        for j in range(i - p4 + 1, i + 1):
            rets.append(c[j] / c[j - 1] - 1.0)
        return -sd1(rets)

    z = []
    for k in range(4):
        win = [value(k, i) for i in range(t - Z + 1, t + 1)]
        s = sd1(win)
        z.append((value(k, t) - mean(win)) / s if s > 0 else 0.0)

    rows = list(range(t - C, t - h + 1))
    y = [c[i + h] / c[i] - 1.0 for i in rows]
    xs = [[value(k, i) for i in rows] for k in range(4)]

    my = mean(y)
    syy = 0.0
    for v in y:
        syy += (v - my) * (v - my)
    w = []
    for k in range(4):
        mx = mean(xs[k])
        sxx = 0.0
        sxy = 0.0
        for a, b in zip(xs[k], y):
            sxx += (a - mx) * (a - mx)
            sxy += (a - mx) * (b - my)
        w.append(sxy / math.sqrt(sxx * syy) if sxx > 0 and syy > 0 else 0.0)

    if wt == "correlation":
        den = sum(abs(v) for v in w)
        if den <= 0:
            return 0.0
        return sum(w[k] * z[k] for k in range(4)) / den
    if wt == "best":
        best = -1
        for k in range(4):
            if abs(w[k]) > 0 and (best < 0 or abs(w[k]) > abs(w[best])):
                best = k
        if best < 0:
            return 0.0
        sgn = 1.0 if w[best] > 0 else -1.0
        return sgn * z[best]
    if wt == "single":
        k = names.index(sig)
        return w[k] * z[k]

    # regression: normal equations with an intercept, solved by Gaussian elimination
    cols = []
    xt = []
    for k in range(4):
        m = mean(xs[k])
        s = sd1(xs[k])
        if s > 0:
            cols.append([(a - m) / s for a in xs[k]])
            xt.append((value(k, t) - m) / s)
    if not cols:
        return 0.0
    feats = [[1.0] * len(y)] + cols
    p = len(feats)
    M = [[0.0] * (p + 1) for _ in range(p)]
    for r in range(p):
        for q in range(p):
            M[r][q] = sum(feats[r][i] * feats[q][i] for i in range(len(y)))
        M[r][p] = sum(feats[r][i] * y[i] for i in range(len(y)))
    for col in range(p):
        piv = col
        for r in range(col + 1, p):
            if abs(M[r][col]) > abs(M[piv][col]):
                piv = r
        M[col], M[piv] = M[piv], M[col]
        for r in range(p):
            if r != col:
                f = M[r][col] / M[col][col]
                for q in range(col, p + 1):
                    M[r][q] -= f * M[col][q]
    coef = [M[r][p] / M[r][r] for r in range(p)]
    return 100.0 * sum(coef[j + 1] * xt[j] for j in range(len(xt)))
