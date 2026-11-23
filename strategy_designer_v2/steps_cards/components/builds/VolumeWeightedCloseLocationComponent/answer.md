# VolumeWeightedCloseLocationComponent: brief_absorption_run | 030-04_heavy-flat-low-close-reverses_1d | CloseLocationVolumeRatio

## attempt 1

answer: built
class: VolumeWeightedCloseLocationComponent
settings: {"volume_period": 20, "exclude_current": 1, "reference": "high"}
reason: `VolumeWeightedCloseLocationComponent` already measures the bar's close location times its volume against the average volume, but it has only the signed location (2 x (close − low) / range − 1) and a base that includes bar t. No config step turns that into (high − close) / range, and none moves the base to the 20 bars before t. The class is written again with two new settings, `reference` and `exclude_current`, whose defaults keep today's output exactly.

table: Directional components
row: | `VolumeWeightedCloseLocationComponent` | `volume_period` (20), `exclude_current` (0), `reference` ("signed") | loc x volume[t] / mean(volume[t-`volume_period`-`exclude_current`+1 .. t-`exclude_current`]). `exclude_current` 0: base volume[t-`volume_period`+1 .. t], bar t included. `exclude_current` 1: base volume[t-`volume_period` .. t-1], bar t excluded. `reference` "signed": loc = 2 x (close[t] − low[t]) / (high[t] − low[t]) − 1, 0 when high[t] = low[t]. `reference` "low": loc = (close[t] − low[t]) / (high[t] − low[t]). `reference` "high": loc = (high[t] − close[t]) / (high[t] − low[t]). "low" and "high" give loc = 0.5 when high[t] = low[t] | "signed": signed; positive in the upper half of the bar, negative in the lower half, 0 at mid-range. "low" and "high": 0 and up, never negative, no direction. "high" is 0 with the close at the high and grows as the close nears the low. With `exclude_current` 0 the volume ratio is above 0 and at most `volume_period`, so "signed" runs −`volume_period` to +`volume_period` and "low"/"high" run 0 to `volume_period`. With `exclude_current` 1 the ratio is unbounded above | graded | dimensionless (share of the bar's range, signed or not, x volume ratio) | `volume_period` + `exclude_current` (20) | high, low, close of bar t; volume of bar t and of the base window. A NaN in any of those gives NaN. A base mean not above 0 gives NaN (never on real bars). These settings raise when the component is built: `volume_period` < 2, `exclude_current` not 0 or 1, `reference` other than "signed", "low" or "high" | stateless. `reference` "signed" with `exclude_current` 0 (the defaults) is the original output, unchanged. "high" is (1 − "low") x ratio, and no config step gives 1 minus a value, hence the setting. `exclude_current` 1 sets volume[t] against the prior `volume_period` days, so bar t's own volume cannot raise its base. With `volume_period` 20, `exclude_current` 1 and `reference` "high" it equals `CloseLocationInRangeComponent` (`reference` "high") x `VolumeRatioComponent` (`period` 20, `exclude_current` 1). Continuous in the close and the volumes while the range is above 0. Ignores the open. No `scaling_factor`: scale it with transforms |

```python class
class VolumeWeightedCloseLocationComponent(SubStrategyComponent):
    """
    Close location in the bar's range, weighted by the bar's volume against its average volume:

        base = volume[t - volume_period - exclude_current + 1 .. t - exclude_current]
            exclude_current = 0 (default): volume[t - volume_period + 1 .. t]  (bar t included)
            exclude_current = 1:           volume[t - volume_period .. t - 1]  (bar t excluded)
        ratio = volume[t] / mean(base)
        rng = high[t] - low[t]
        reference = "signed" (default): loc = 2 x (close[t] - low[t]) / rng - 1   (0 when rng = 0)
        reference = "low":              loc = (close[t] - low[t]) / rng            (0.5 when rng = 0)
        reference = "high":             loc = (high[t] - close[t]) / rng           (0.5 when rng = 0)
        raw_value = loc x ratio

    The defaults ("signed", exclude_current 0) give the original output, unchanged.
    Range: "signed" is signed, positive when the close is in the upper half of the bar. "low" and "high" are
    0 and up, never negative. "high" is 0 with the close at the high and grows as the close nears the low.
    With exclude_current 0 the ratio is at most volume_period; with exclude_current 1 it is unbounded above.
    Graded, continuous in the close and the volumes while rng > 0.
    Warm-up: volume_period + exclude_current rows, bar t included.

    NaN: a NaN high, low or close on bar t, a NaN volume[t], or a NaN volume in the base gives NaN. A base mean
    not above 0 gives NaN (never on real bars).
    Building the component raises for a volume_period below 2, an exclude_current other than 0 or 1, or a
    reference other than "signed", "low" or "high".

    WHY THIS CANNOT LEAK: it reads high, low and close of the last row (bar t) and volume over at most the last
    volume_period + exclude_current rows, all at or before bar t; every value is known at bar t's close.
    """

    def __init__(self, name="VolumeWeightedCloseLocation", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.volume_period = int(self.parameters.get("volume_period", 20))
        if self.volume_period < 2:
            raise ValueError(
                f"VolumeWeightedCloseLocationComponent: volume_period must be >= 2, got {self.volume_period}")
        ex = self.parameters.get("exclude_current", 0)
        if isinstance(ex, bool):
            ex = int(ex)
        if ex not in (0, 1):
            raise ValueError(
                f"VolumeWeightedCloseLocationComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self.reference = self.parameters.get("reference", "signed")
        if self.reference not in ("signed", "low", "high"):
            raise ValueError(
                "VolumeWeightedCloseLocationComponent: reference must be 'signed', 'low' or 'high', "
                f"got {self.reference!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = len(data)
        h = float(data["high"].iloc[-1])
        l = float(data["low"].iloc[-1])
        c = float(data["close"].iloc[-1])
        vol = data["volume"].astype(float).to_numpy()
        v_t = float(vol[-1])
        ex = self.exclude_current
        base = vol[n - self.volume_period - ex: n - ex]
        if np.isnan(h) or np.isnan(l) or np.isnan(c) or np.isnan(v_t) or np.isnan(base).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        den = float(np.mean(base))
        if not den > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rng = h - l
        if self.reference == "signed":
            loc = 0.0 if rng == 0 else 2.0 * (c - l) / rng - 1.0
        elif self.reference == "low":
            loc = 0.5 if rng == 0 else (c - l) / rng
        else:
            loc = 0.5 if rng == 0 else (h - c) / rng
        ratio = v_t / den
        self._raw_value = float(loc * ratio)
        self.confidence = 1.0
        self.debug_info = {"location": loc, "volume_ratio": ratio, "reference": self.reference,
                           "exclude_current": ex}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.volume_period + self.exclude_current
```

```python hand
def hand(df, params):
    p = int(params.get("volume_period", 20))
    ex = int(params.get("exclude_current", 0))
    ref = params.get("reference", "signed")
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    vols = [float(x) for x in list(df["volume"])]
    t = len(closes) - 1
    h = highs[t]
    l = lows[t]
    c = closes[t]
    v_t = vols[t]
    # base: the p volumes ending ex bars before t
    base = []
    for k in range(p):
        base.append(vols[t - ex - k])
    for x in [h, l, c, v_t] + base:
        if x != x:
            return float("nan")
    total = 0.0
    for x in base:
        total = total + x
    mean_base = total / p
    if not mean_base > 0:
        return float("nan")
    rng = h - l
    if ref == "high":
        if rng == 0:
            loc = 0.5
        else:
            loc = (h - c) / rng
    elif ref == "low":
        if rng == 0:
            loc = 0.5
        else:
            loc = (c - l) / rng
    else:
        if rng == 0:
            loc = 0.0
        else:
            loc = 2.0 * (c - l) / rng - 1.0
    return loc * (v_t / mean_base)
```

checks:
VolumeWeightedCloseLocationComponent: every check passed
the bot's suite: == 1636 passed, 16 skipped, 75 deselected, 2244 warnings in 73.37s (0:01:13) ===
