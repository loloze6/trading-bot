"""Spec of RsiChangeFromPriorLowComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'RsiChangeFromPriorLowComponent'
SETTINGS = [{}, {"rsi_period": 14, "lookback": 30, "exclude": 3, "rsi_window": 100}]


def hand(df, params):
    p = params.get("rsi_period", 14)
    lb = params.get("lookback", 30)
    ex = params.get("exclude", 3)
    w = params.get("rsi_window", 100)
    c = list(df["close"])
    t = len(c) - 1
    if any(x != x for x in c[t - lb - w:]):
        return float("nan")

    def rsi(i):
        a = 1.0 / p
        g = l = None
        for k in range(i - w + 1, i + 1):
            d = c[k] - c[k - 1]
            up = d if d > 0 else 0.0
            dn = -d if d < 0 else 0.0
            if g is None:
                g, l = up, dn
            else:
                g = (1 - a) * g + a * up
                l = (1 - a) * l + a * dn
        return 50.0 if g + l == 0 else 100.0 * g / (g + l)

    candidates = list(range(t - lb, t - ex))
    low = min(c[i] for i in candidates)
    s = max(i for i in candidates if c[i] == low)
    return rsi(t) - rsi(s)
