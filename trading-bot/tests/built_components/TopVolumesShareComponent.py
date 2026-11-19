"""Spec of TopVolumesShareComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'TopVolumesShareComponent'
SETTINGS = [{}, {"period": 72, "top_k": 3}]


def hand(df, params):
    n = int(params.get("period", 72))
    k = int(params.get("top_k", 3))
    v = [float(x) for x in list(df["volume"])]
    last = len(v) - 1
    window = []
    i = last - n + 1
    while i <= last:
        window.append(v[i])
        i = i + 1
    for x in window:
        if x != x:
            return float("nan")
    total = 0.0
    for x in window:
        total = total + x
    if not total > 0:
        return float("nan")
    remaining = list(window)
    top = 0.0
    picked = 0
    while picked < k:
        best_idx = 0
        j = 1
        while j < len(remaining):
            if remaining[j] > remaining[best_idx]:
                best_idx = j
            j = j + 1
        top = top + remaining[best_idx]
        remaining.pop(best_idx)
        picked = picked + 1
    return top / total
