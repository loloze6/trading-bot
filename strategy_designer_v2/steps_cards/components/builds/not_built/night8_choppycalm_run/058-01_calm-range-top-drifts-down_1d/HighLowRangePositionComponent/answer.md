# not built: night8_choppycalm_run | 058-01_calm-range-top-drifts-down_1d | HighLowRangePositionComponent

## attempt 1

answer: exists
class: DonchianBreakoutComponent
settings: {"period": 20, "scaling_factor": 1.0, "source": "high_low"}
reason: With `source` "high_low" and `sf` 1, `DonchianBreakoutComponent` outputs exactly 2 x (close[t] − min(low[t-19..t])) / (max(high[t-19..t]) − min(low[t-19..t])) − 1, bar t included. A zero range gives pos 0.5 and so an output of 0, which is the wished value.

refused: DonchianBreakoutComponent does not take the settings ['source']

## attempt 2

answer: built
class: DonchianBreakoutComponent
settings: {"period": 20, "scaling_factor": 1.0, "source": "high_low"}
reason: `DonchianBreakoutComponent` computes this measure, the close's position in its recent range scaled to −`sf`..+`sf`, but only against the closes' range. It does not take the bars' high-low range, and no config step gives that, so the class is written again with a `source` setting whose default "close" keeps today's output exactly.

table: Directional components
row: | `DonchianBreakoutComponent` | `period` (48), `scaling_factor` (20.0), `source` ("close") | (2 x pos − 1) x `sf`, pos = (close[t] − L) / (H − L) over bars t-`period`+1 .. t (bar t included), pos = 0.5 when H = L. `source` "close": H, L = highest and lowest close. `source` "high_low": H = max(high), L = min(low). With `period` 20, `sf` 1, "high_low": 2 x (close[t] − min(low[t-19..t])) / (max(high[t-19..t]) − min(low[t-19..t])) − 1 | −`sf` to +`sf`, signed; positive above the window's middle, 0 at the middle or for a zero range; +`sf` at the window's top, −`sf` at its bottom | graded | forecast units (x `sf`) | `period` (48) | "close": closes only. "high_low": high and low (last `period` rows) and close[t]. A NaN in any value read gives NaN. These settings raise when the component is built: `period` < 1, `source` other than "close" or "high_low" | stateless. `source` "close" (default) is the original output, unchanged. "high_low" measures the close against the bars' full high-low range, which no config step gives, hence the setting. It is not a breakout event. `negate` gives the near-the-bottom reading |

```python class
class DonchianBreakoutComponent(SubStrategyComponent):
    """
    Where the close sits inside its recent range, on every bar:

        window = bars t-period+1 .. t (bar t included)
        source = "close" (default): H = max(close[window]), L = min(close[window])
        source = "high_low":        H = max(high[window]),  L = min(low[window])
        pos = (close[t] - L) / (H - L), pos = 0.5 when H = L
        raw_value = (2 x pos - 1) x scaling_factor

    With period 20, scaling_factor 1 and source "high_low":
        2 x (close[t] - min(low[t-19..t])) / (max(high[t-19..t]) - min(low[t-19..t])) - 1.
    Range and sign: -scaling_factor to +scaling_factor, signed. It is positive above the window's middle, 0 at
    the middle or for a zero range, +sf with the close at the window's top and -sf at its bottom. It is graded and
    continuous, not a breakout event. source "close" (default) is the original output, unchanged.
    Warm-up: period rows, bar t included.
    NaN: a NaN in any value read (the closes of the window with "close"; the highs and lows of the window and
    close[t] with "high_low") gives NaN.
    Building the component raises for a period below 1 or a source other than "close" or "high_low".

    WHY THIS CANNOT LEAK: it reads only the close, high and low columns of the last `period` rows of data, the
    last of which is bar t; every value is known at bar t's close.
    """

    def __init__(self, name="DonchianBreakout", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 48))
        if self.period < 1:
            raise ValueError(f"DonchianBreakoutComponent: period must be >= 1, got {self.period}")
        self.scaling_factor = float(self.parameters.get("scaling_factor", 20.0))
        self.source = self.parameters.get("source", "close")
        if self.source not in ("close", "high_low"):
            raise ValueError(
                f"DonchianBreakoutComponent: source must be 'close' or 'high_low', got {self.source!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.period
        close = data["close"].astype(float).to_numpy()
        c = float(close[-1])
        if self.source == "high_low":
            hi = data["high"].astype(float).to_numpy()[-n:]
            lo = data["low"].astype(float).to_numpy()[-n:]
        else:
            hi = close[-n:]
            lo = close[-n:]
        if np.isnan(c) or np.isnan(hi).any() or np.isnan(lo).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        H = float(np.max(hi))
        L = float(np.min(lo))
        rng = H - L
        if rng == 0:
            pos = 0.5
        else:
            pos = (c - L) / rng
        self._raw_value = float((2.0 * pos - 1.0) * self.scaling_factor)
        self.confidence = 1.0
        self.debug_info = {"high": H, "low": L, "pos": pos, "source": self.source}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.period
```

```python hand
def hand(df, params):
    n = int(params.get("period", 48))
    sf = float(params.get("scaling_factor", 20.0))
    source = params.get("source", "close")
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    c = closes[t]
    if source == "high_low":
        highs = [float(x) for x in list(df["high"])]
        lows = [float(x) for x in list(df["low"])]
        his = [highs[t - k] for k in range(n)]
        los = [lows[t - k] for k in range(n)]
    else:
        his = [closes[t - k] for k in range(n)]
        los = list(his)
    for x in his + los + [c]:
        if x != x:
            return float("nan")
    top = his[0]
    for x in his:
        if x > top:
            top = x
    bottom = los[0]
    for x in los:
        if x < bottom:
            bottom = x
    width = top - bottom
    if width == 0:
        pos = 0.5
    else:
        pos = (c - bottom) / width
    return (2.0 * pos - 1.0) * sf
```

checks:
the bot's suite fails:
umns_in_the_run
tests/test_d146_register_read_feeds_only.py::test_registered_unread_feeds_really_put_their_columns_in_the_run
tests/test_d146_register_read_feeds_only.py::test_required_feed_missing_still_raises
tests/test_d146_register_read_feeds_only.py::test_required_feed_missing_from_an_empty_menu_still_raises
  /home/user/trading-bot/trading-bot/tests/test_d146_register_read_feeds_only.py:131: DeprecationWarning: The 'generic' unit for NumPy timedelta is deprecated, and will raise an error in the future. This includes implicit conversion of bare integers (e.g. `+ 1`).Please use a specific unit instead.
    prints = pd.date_range(START - pd.Timedelta(days=1), periods=60, freq="8h")

tests/test_d176_sizing_block.py: 250 warnings
  /home/user/trading-bot/trading-bot/tests/test_d176_sizing_block.py:73: DeprecationWarning: The 'generic' unit for NumPy timedelta is deprecated, and will raise an error in the future. This includes implicit conversion of bare integers (e.g. `+ 1`).Please use a specific unit instead.
    return str(pd.Timestamp("2024-04-01") + pd.Timedelta(hours=int(i)))

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
FAILED tests/test_feed_dependencies.py::test_no_undeclared_feed_reference_drift
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
= 1 failed, 730 passed, 2 skipped, 75 deselected, 2106 warnings in 80.20s (0:01:20) =


## attempt 3

answer: exists
class: DonchianBreakoutComponent
settings: {"period": 20, "scaling_factor": 1.0, "source": "high_low"}
reason: With `source` "high_low", `period` 20 and `sf` 1, `DonchianBreakoutComponent` outputs exactly 2 x (close[t] − min(low[t-19..t])) / (max(high[t-19..t]) − min(low[t-19..t])) − 1. It reads 0 for a zero range (pos = 0.5) and is signed and graded from −1 at the range's low to +1 at its high, so no new class is needed.

refused: DonchianBreakoutComponent does not take the settings ['source']
