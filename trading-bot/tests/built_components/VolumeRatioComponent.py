"""Spec of VolumeRatioComponent for the standard checks (component_harness.py): its settings and a hand computation
that uses only the rows up to bar t (the last row of df)."""
CLASS = "VolumeRatioComponent"
SETTINGS = [{"period": 30}, {"period": 10}, {"period": 2}]   # the first is the defaults


def hand(df, params):
    n = params.get("period", 30)
    v = list(df["volume"])[-n:]
    mean = sum(v) / n
    return v[-1] / mean if mean > 0 else float("nan")
