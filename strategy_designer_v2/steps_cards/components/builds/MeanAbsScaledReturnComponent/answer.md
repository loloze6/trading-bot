# MeanAbsScaledReturnComponent: night8_choppyagitated_run | 059-01.b1.b1.d1.b1.b1.d1.d1_raw-scaled-rise-four-weeks_1d | centred mean-abs-scaled return

## attempt 1

answer: built
class: MeanAbsScaledReturnComponent
settings: {"period": 7, "window": 30, "base": "mean_abs_return", "form": "centred"}
reason: `MeanAbsScaledReturnComponent` (`period` 7, `window` 30) computes this measure but has no shifted form. Subtracting 1 is neither a negation nor 1 minus the value, and no config step adds a constant (`standardise` divides without centring), so the class gets a `form` setting. Its default "ratio" keeps today's output exactly.

table: Directional components
row: | `MeanAbsScaledReturnComponent` | `period` (24), `window` (720), `base` ("mean_abs_return"), `form` ("ratio") | x = (close[t] / close[t-`period`] - 1) / m. `base` "mean_abs_return": m = mean over i = t-`window`+1 .. t of abs(close[i] / close[i-`period`] - 1), the overlapping `period`-bar simple returns ending at each of the last `window` bars, bar t included. `base` "mean_relative_range": m = mean over i = t-`window`+1 .. t of (high[i] - low[i]) / close[i], bar t included. x = 0 when m = 0. `form` "ratio": x. `form` "centred": x - 1. With `period` 7, `window` 30, "mean_abs_return", "centred": (close[t]/close[t-7] - 1) / mean(abs(close[i]/close[i-7] - 1), i = t-29 .. t) - 1 | "ratio": unbounded in practice, signed like the `period`-bar return, 0 for a flat move. With "mean_abs_return" its size is at most `window`. "centred": the same minus 1, signed. It is 0 at a rise of one usual move, negative below it (flat moves and falls included) and grows linearly above it; with "mean_abs_return" it runs from -`window`-1 to `window`-1 | graded | "mean_abs_return": usual `period`-bar moves ("centred": minus 1). "mean_relative_range": mean bar ranges as a fraction of the close ("centred": minus 1) | `window` + `period` (744; 37 at the wished settings) with "mean_abs_return"; max(`window`, `period` + 1) with "mean_relative_range" | "mean_abs_return": closes only. A NaN close in the last `window` + `period` rows gives NaN, and so does a close not above 0 there (never on real bars). "mean_relative_range": close (bars t-`window`+1 .. t and bar t-`period`), high and low (last `window` rows). A NaN in any of those gives NaN, and so does a close not above 0 among them (never on real bars). m = 0 gives x = 0, so "centred" reads -1 (never on real bars). These settings raise when the component is built: `period` < 1, `window` < 1, `base` other than "mean_abs_return" or "mean_relative_range", `form` other than "ratio" or "centred" | stateless. `base` "mean_abs_return" with `form` "ratio" (the defaults) is the original output, unchanged. "centred" subtracts 1, so 0 marks a move of exactly one usual move. No config step adds a constant (`standardise` does not centre), hence the setting, as with `VolumeRatioComponent` "centred". It is continuous in the closes. On 1d bars the wished settings give the 7-day return in usual 7-day moves over 30 days, minus 1. `negate` gives the fall-positive reading. No `scaling_factor`: scale it with transforms |

```python class
class MeanAbsScaledReturnComponent(SubStrategyComponent):
    """
    A move counted in usual moves, on every bar:

        x = (close[t] / close[t - period] - 1) / m
        base = "mean_abs_return" (default):
            m = mean over i = t-window+1 .. t of abs(close[i] / close[i-period] - 1)
        base = "mean_relative_range":
            m = mean over i = t-window+1 .. t of (high[i] - low[i]) / close[i]
        x = 0 when m = 0
        form = "ratio" (default): raw_value = x
        form = "centred":         raw_value = x - 1

    The defaults (base "mean_abs_return", form "ratio") are the original output, unchanged.
    "centred" reads 0 at a move of exactly one usual move, below 0 for smaller moves (falls included)
    and grows linearly above it.
    Range: "ratio" is signed like the period-bar return; with "mean_abs_return" its size is at most
    window. "centred" is the same minus 1.
    Warm-up: window + period rows with "mean_abs_return"; max(window, period + 1) with
    "mean_relative_range".

    WHY THIS CANNOT LEAK: it reads only the close (and, with "mean_relative_range", the high and the
    low) of the rows up to and including bar t (the last row of data). That covers at most the last
    window + period rows, and each value is known at its bar's close.

    NaN: a NaN in any value read gives NaN, and so does a close not above 0 among them (never on real
    bars). m = 0 gives x = 0 (never on real bars).
    Building raises for period < 1, window < 1, an unknown base or an unknown form.
    """

    def __init__(self, name="MeanAbsScaledReturn", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 24))
        if self.period < 1:
            raise ValueError(f"MeanAbsScaledReturnComponent: period must be >= 1, got {self.period}")
        self.window = int(self.parameters.get("window", 720))
        if self.window < 1:
            raise ValueError(f"MeanAbsScaledReturnComponent: window must be >= 1, got {self.window}")
        self.base = self.parameters.get("base", "mean_abs_return")
        if self.base not in ("mean_abs_return", "mean_relative_range"):
            raise ValueError(
                f"MeanAbsScaledReturnComponent: base must be 'mean_abs_return' or 'mean_relative_range', got {self.base!r}")
        self.form = self.parameters.get("form", "ratio")
        if self.form not in ("ratio", "centred"):
            raise ValueError(f"MeanAbsScaledReturnComponent: form must be 'ratio' or 'centred', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data["close"].astype(float).to_numpy()
        n = len(close)
        t = n - 1
        p = self.period
        w = self.window
        if self.base == "mean_abs_return":
            seg = close[n - (w + p):]
            if np.isnan(seg).any() or (seg <= 0).any():
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            rets = seg[p:] / seg[:-p] - 1.0
            m = float(np.mean(np.abs(rets)))
            r = float(rets[-1])
        else:
            high = data["high"].astype(float).to_numpy()
            low = data["low"].astype(float).to_numpy()
            cl = close[n - w:]
            hi = high[n - w:]
            lo = low[n - w:]
            c0 = close[t - p]
            if (np.isnan(cl).any() or np.isnan(hi).any() or np.isnan(lo).any() or np.isnan(c0)
                    or (cl <= 0).any() or not c0 > 0):
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            m = float(np.mean((hi - lo) / cl))
            r = float(close[t] / c0 - 1.0)
        x = 0.0 if m == 0 else r / m
        if self.form == "centred":
            x = x - 1.0
        self._raw_value = float(x)
        self.confidence = 1.0
        self.debug_info = {"return": r, "usual_move": m, "base": self.base, "form": self.form}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        if self.base == "mean_abs_return":
            return self.window + self.period
        return max(self.window, self.period + 1)
```

```python hand
def hand(df, params):
    p = int(params.get("period", 24))
    w = int(params.get("window", 720))
    base = params.get("base", "mean_abs_return")
    form = params.get("form", "ratio")
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    if base == "mean_abs_return":
        # every close used: bars t-w-p+1 .. t
        for k in range(t - w - p + 1, t + 1):
            if c[k] != c[k] or not c[k] > 0:
                return float("nan")
        total = 0.0
        for i in range(t - w + 1, t + 1):
            total += abs(c[i] / c[i - p] - 1.0)
        m = total / w
    else:
        h = [float(x) for x in list(df["high"])]
        lo = [float(x) for x in list(df["low"])]
        if c[t - p] != c[t - p] or not c[t - p] > 0:
            return float("nan")
        total = 0.0
        for i in range(t - w + 1, t + 1):
            if c[i] != c[i] or h[i] != h[i] or lo[i] != lo[i] or not c[i] > 0:
                return float("nan")
            total += (h[i] - lo[i]) / c[i]
        m = total / w
    r = c[t] / c[t - p] - 1.0
    x = 0.0 if m == 0 else r / m
    if form == "centred":
        x -= 1.0
    return x
```

checks:
MeanAbsScaledReturnComponent: every check passed
the bot's suite: == 1668 passed, 16 skipped, 75 deselected, 2244 warnings in 146.74s (0:02:26) ==
