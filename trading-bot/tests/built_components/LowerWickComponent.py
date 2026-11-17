"""Spec of LowerWickComponent for the standard checks (component_harness.py): its settings (the defaults first) and a
hand computation that uses only the rows up to bar t. Merged on 2026-11-17 from the specs of LowerWickShareComponent and
LowerWickPercentComponent (written by the components step), whose hand computations it keeps."""
CLASS = "LowerWickComponent"
SETTINGS = [{}, {"relative_to": "close"}]


def hand(df, params):
    o, h, l, c = (list(df[k])[-1] for k in ("open", "high", "low", "close"))
    if o != o or h != h or l != l or c != c:
        return float("nan")
    wick = (o if o < c else c) - l
    if params.get("relative_to", "range") == "range":
        return 0.0 if h - l == 0 else wick / (h - l)
    return wick / c * 100.0
