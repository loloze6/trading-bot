# COMPONENT_CATALOG.md

The inventory of every strategy component: what each one outputs, exactly. Read together with
`STRATEGY_DESIGN_GUIDE.md` (how to design a config from these components). Every class below lives in
`strategies.strategy_components`; a config refers to one as
`"class": "strategies.strategy_components.<ClassName>"`. There are 28 classes. No other component exists: a class
name that is not a row below is invented.

## How to read a row

- **params (defaults)**: the keys accepted under the component's `params`. A key that is not listed is silently
  ignored, and so is a typo: the default is used and nothing warns. A `scaling_factor` is written `sf` below.
- **exact output**: what the component's raw value is on bar t, computed from the bars up to and including bar
  t's close (the two SMA components lag one bar, noted in their rows). The raw value is what a transform
  pipeline starts from. Rows say "closes" for the `close` column of the bar window.
- **range & sign**: the values the raw value can take, at the default `sf` where one exists. "Forecast units"
  means the output is meant to live on the `[-20, +20]` forecast scale (allocation = forecast / 10).
- **units**: what the number measures (percent, price units, dimensionless, forecast units).
- **warmup**: the component's own `get_required_periods()` at the default params, in bars of the backtest
  timeframe. The strategy as a whole needs more (see the design guide, "The forecast for each regime").
- **data & NaN**: which bar columns the component reads, and what it does with a missing column or a NaN. A NaN
  close appears only when the run uses gap handling that leaves NaN rows; without it, closes are always finite.
  Where a component turns a NaN into `0.0`, that zero is a fabricated reading, not a measurement.
- **notes**: state kept between bars, unused parameters, misleading names.

Parameters are counted in bars, so their meaning changes with the timeframe (48 bars is two days on 1h bars and
eight days on 4h bars).

### Kind legend

| kind | meaning | use as a forecast source |
|---|---|---|
| **graded** | the output grows or shrinks continuously with the strength of the signal | allowed |
| **on/off** | the output sits at 0 and jumps to a level (or between fixed levels) when a condition fires | refused (D-051, hard rule) |
| **constant** | the same value every bar | only as an offset inside a composition with a graded component |
| **regime measure** | a bounded or scale-stable measurement of the market state, not a bet | for regime rules and vetoes (the raw latest value is compared with a threshold) |

A graded component can be signed (long and short), one-sided, or non-directional (always the same sign). The
"range & sign" column says which.

### Naming rule

A new component's name says what its output measures and how it is computed (`MovingAverageDistanceComponent`,
`MacdHistogramComponent`). It carries no word about an intended use unless the output really is that: no "Filter"
unless it switches something off, no "Breakout" unless it fires on a breakout, no "Hedge". Graded is the default, so a
graded component carries no "Graded" suffix. Existing names are kept so past configs still load; the misleading ones
are listed below with what each really is, and get clear names when the old classes are cleaned up.

| Name | What it really is |
|---|---|
| `ADXDirectionalComponent` | the +DI / -DI ratio, -1 to +1; not ADX |
| `DonchianBreakoutComponent` | where the close sits in its recent range, on every bar; not a breakout event |
| `KeltnerBreakoutComponent` | the distance from the EMA in ATR units, on every bar; not a band-break event |
| `MacroTrendFilterComponent` | the percent distance from an EMA; filters nothing (use `MovingAverageDistanceComponent`) |
| `PriceOverextensionHedgeComponent` | a contrarian z-score of the distance from the EMA; not a hedge |
| `VolumeExpansionHedgeComponent` | on/off: fires on low-volume up bars and only pushes the forecast down; not a volume expansion |
| `PriceEvolutionOnPeriodComponent` | `PriceEvolutionComponent` at `scaling_factor` 1; its own `scaling_factor` is ignored |
| `MomentumDivergenceComponent` | how aligned two horizons are (a product, no direction); its `scaling_factor` is ignored |
| `EMADiff` | the MACD line, in price units |

## Component rows

Columns: class, params (defaults), exact output, range & sign, kind, units, warmup, data & NaN, notes.

<!-- CATALOG:START -->

### Regime measures

| Class | params (defaults) | Exact output | Range & sign | Kind | Units | Warmup | Data & NaN | Notes |
|---|---|---|---|---|---|---|---|---|
| `RSquaredRegimeComponent` | `period` (48) | R-squared of a straight-line fit of the last `period` closes against the bar index: `corrcoef(index, close)` squared | 0 to 1, never negative; no direction | regime measure | dimensionless | `period` (48) | closes. A NaN close inside the window gives NaN for `period` bars; constant closes give NaN | fit is on price levels, not log prices; stateless |
| `EfficiencyRatioRegimeComponent` | `period` (24), `smooth_period` (5) | raw ER = abs(close[-1] - close[-(period+1)]) divided by the sum of abs one-bar close changes over the last `period+1` closes (0 if that sum is 0); output is the EWM (span `smooth_period`, adjust=False) of the last `3 x smooth_period` raw values | 0 to 1, never negative; no direction | regime measure | dimensionless | `period + 1` (25) | closes. A NaN close gives NaN output on some of the `period + 1` bars that follow it (the smoothing shapes which) | stateful: keeps its own short history of raw ER values; 1.0 = straight line, near 0 = choppy |
| `VolatilityPercentileRegimeComponent` | `vol_period` (20), `lookback_period` (100), `smooth_period` (5) | rolling std (window `vol_period`) of one-bar returns (close change divided by the current close); the raw value is the share of the last `lookback_period` rolling-std values that are <= the latest one; output is the EWM (span `smooth_period`) of the last `3 x smooth_period` such shares | above 0, up to 1; no direction; 1.0 = most volatile in the lookback | regime measure | dimensionless (rank) | `lookback_period + vol_period` (120) | closes. NaN rolling-std values are dropped from the rank (the output stays finite) | stateful smoothing |
| `ADXDirectionalComponent` | `period` (24) | DI ratio = (+DI - -DI) / (+DI + -DI), with +DM, -DM and true range smoothed Wilder-style (alpha = 1/`period`), the recursion seeded at the first row of the bar window the component is given | -1 to +1; positive when up-moves dominate, negative when down-moves dominate, near 0 when balanced | regime measure | dimensionless | `period + 1` (25) | high, low, close. A NaN row contaminates the recursion: NaN for as long as that row stays in the window | the name says ADX but the output is the DI ratio, not ADX. Signed and bounded, so it works as a trend-direction regime input; the exact value depends slightly on the window length |
| `VarianceRatioComponent` | `k` (5), `window` (100) | VR(k) = variance of overlapping k-bar sums of log returns (last `window` of them) divided by (`k` x variance of one-bar log returns over the last `window`, ddof 1, plus 1e-12) | 0 and up, unbounded; typically 0.5 to 1.5; above 1 = returns positively autocorrelated (trending), below 1 = mean-reverting | regime measure | dimensionless | `window + k` (105) | closes (must be positive: logs). A NaN close gives NaN for `window + k` bars | stateless. Not bounded above, but scale-stable across assets |

### Directional components

| Class | params (defaults) | Exact output | Range & sign | Kind | Units | Warmup | Data & NaN | Notes |
|---|---|---|---|---|---|---|---|---|
| `PriceEvolutionComponent` | `period` (20), `scaling_factor` (2.0) | (close[-1] - close[-(period+1)]) / close[-(period+1)] x 100 x `sf` | unbounded, signed, positive when price rose over the last `period` bars; at the defaults a 10 percent rise gives +20 | graded | percent x `sf` | `period + 1` (21) | closes. NaN only if close[-1] or close[-(period+1)] is NaN | momentum over one horizon; stateless |
| `PriceEvolutionOnPeriodComponent` | `comparison_period` (20), `scaling_factor` (20, unused) | (close[-1] - close[-(comparison_period+1)]) / close[-(comparison_period+1)] x 100 | unbounded, signed, positive when price rose | graded | percent | `comparison_period + 1` (21) | closes. NaN only if one of the two closes used is NaN | `scaling_factor` is read but never used: the output is `PriceEvolutionComponent` with `sf` = 1. Scale it with a `scale` transform |
| `RSIPullbackComponent` | `period` (14), `scaling_factor` (0.4), `long_only` (false), `entry_threshold` (0.0, no effect through a config) | (50 - RSI) x `sf`, RSI being the Wilder-style RSI (EWM alpha 1/`period`, adjust=False, of gains and losses over the bar window) | -50 x `sf` to +50 x `sf` (-20 to +20 at the default); positive when RSI is below 50, negative when above: contrarian | graded | RSI points x `sf` | `period + 1` (15) | closes. Flat prices (no gain and no loss) give NaN. Interior NaN closes are skipped by the EWM and the value carries through them | `long_only: true` clamps the output at 0, so it is positive whenever RSI < 50 (about half the bars) and 0 otherwise: continuous, not "only buys dips". `entry_threshold` does nothing in a config. A negative `sf` turns it into a trend-following (momentum) signal |
| `EMASpreadComponent` | `fast_period` (9), `slow_period` (21), `scaling_factor` (5.0) | (EMA_fast - EMA_slow) / EMA_slow x 100 x `sf`, EMAs with `span` = period, adjust=False, over the bar window | unbounded, signed, positive when the fast EMA is above the slow one | graded | percent x `sf` | `slow_period` (21) | closes. Interior NaN closes are skipped by the EWM | a continuous signed spread, not a crossover event; there is no check that `fast_period` < `slow_period` |
| `EMADiff` | `ST_EMA_period` (12), `LT_EMA_period` (26) | EMA_ST(close) - EMA_LT(close), pandas `ewm(span=...)` with its default adjust=True | unbounded, signed, positive when the short EMA is above the long one | graded | price units (quote currency) | `LT_EMA_period` (26) | closes. Interior NaN closes are skipped by the EWM | the MACD line in price units: its size scales with the asset's price, so it is not comparable across assets. No `scaling_factor`. Divide by the close with a `price_normalized` transform to make it scale-free |
| `MacroTrendFilterComponent` | `period` (200), `scaling_factor` (2.0) | (close - EMA_period) / EMA_period x 100 x `sf`, EMA with `span` = `period`, adjust=False | unbounded, signed, positive when the close is above its long EMA | graded | percent x `sf` | `period` (200) | closes. Interior NaN closes are skipped by the EWM; NaN if the latest close is NaN | the long-horizon trend reading; a signed graded signal (percent distance), not a filter that switches anything off. Old, misleading name (it filters nothing): for a new config use `MovingAverageDistanceComponent` with `average` "ema". |
| `MovingAverageDistanceComponent` | `period` (50), `average` ("sma") | (close - MA) / MA x 100, where MA is the simple mean of the last `period` closes including the current one (`average` "sma") or their EMA with `span` = `period`, adjust=False (`average` "ema") | unbounded, signed; positive when the close is above its average | graded | percent | `period` (50) | closes. An SMA window holding a NaN close, or a NaN latest close, gives NaN; an unknown `average` or a `period` below 2 raises when the engine starts | no lag: the average includes the current close. With `average` "ema" it equals `MacroTrendFilterComponent` at `scaling_factor` 1. No `scaling_factor`: scale it with transforms. Long-only: add a `clip` with `min` 0 |
| `DonchianBreakoutComponent` | `period` (48), `scaling_factor` (20.0) | (2 x pos - 1) x `sf`, where pos = (close - lowest close) / (highest close - lowest close) over the last `period` closes INCLUDING the current bar (pos = 0.5 if highest = lowest) | -`sf` to +`sf` (-20 to +20 at the default); continuous and non-zero on almost every bar; +`sf` when the close is the highest close of the window, -`sf` when it is the lowest | graded | forecast units | `period` (48) | closes only (high and low are not read). A NaN close in the window gives NaN for `period` bars | where the close sits inside its recent range; it is NOT a breakout event and never fires on a condition. A negative `sf` gives an anti-breakout (mean-reversion) signal: short near the top of the range, long near the bottom. A longer `period` widens the window; it does not make signals rarer or more selective |
| `KeltnerBreakoutComponent` | `ema_period` (20), `atr_period` (20), `atr_multiplier` (1.5), `scaling_factor` (20.0) | osc = (close - EMA) / (`atr_multiplier` x ATR), clipped to -1.2 .. +1.2, times `sf`; EMA has `span` = `ema_period` (adjust=False), ATR is the simple rolling mean of the true range over `atr_period` | -1.2 x `sf` to +1.2 x `sf` (-24 to +24 at the default); continuous; positive when the close is above the EMA | graded | forecast units | `max(ema_period, atr_period) + 1` (21) | high, low, close. A NaN ATR gives an oscillator of 0, so the output is 0.0 (a silent zero) for `atr_period` bars | continuous every bar, not an event that fires on a band break. A negative `sf` is a pure sign flip on every bar. `atr_multiplier` only rescales the magnitude (and moves where the 1.2 clip binds); it does not make signals rarer |
| `MomentumDivergenceComponent` | `short_period` (5), `long_period` (20), `scaling_factor` (1.5, unused) | short_trend x long_trend, each in percent: short_trend = (close[-1] - close[-short_period]) / close[-short_period] x 100, long_trend likewise with `long_period` (the two spans are 4 and 19 bars, because of close[-p]) | unbounded; positive when the two trends have the same sign (both up or both down), negative when they disagree; carries no direction | graded | percent squared | `long_period` (20) | closes. NaN only if close[-1] or one of the two lookback closes is NaN | `scaling_factor` is read but never used. Because the product is positive in both a rally and a sell-off, it says how aligned the two horizons are, not which way to trade |
| `MacdHistogramCrossoverComponent` | `fast_period` (12), `slow_period` (26), `signal_period` (9), `scaling_factor` (10.0) | +`sf` on the bar the MACD histogram (MACD line minus its EMA-`signal_period` signal line) changes from <= 0 to > 0, -`sf` on the bar it changes from >= 0 to < 0, 0 on every other bar | three values: -`sf`, 0, +`sf`; non-zero on a few percent of bars | on/off | forecast units | `slow_period + signal_period` (35) | closes. Interior NaN closes are skipped by the EWMs | stateful: remembers the previous bar's histogram sign, so the output on a bar can depend on which bar the run started seeing data; the first ready bar never fires. An event pulse, not a level. Graded version: `MacdHistogramComponent`. |
| `MacdHistogramComponent` | `fast_period` (12), `slow_period` (26), `signal_period` (9) | (MACD - signal) / close x 100, where MACD = EMA_fast - EMA_slow of the closes and signal = EMA_`signal_period` of MACD; EMAs with `span` = period, adjust=False, over the bar window | unbounded, signed; positive when the MACD line is above its signal line | graded | percent of price | `slow_period + signal_period` (35) | closes. Interior NaN closes are skipped by the EWMs; a NaN latest close gives NaN | the graded version of `MacdHistogramCrossoverComponent`: the histogram's level on every bar, not its zero-crossing pulse; stateless. The EWMs start at the first bar of the window, so the value depends slightly on the window's length. Not `EMADiff` (the MACD line itself, in price units): this is the MACD line minus its own EMA, divided by the close. No `scaling_factor`: scale it with transforms |
| `SmaTrendLongOnlyComponent` | `lookback_L` (100), `scaling_factor` (10.0) | `sf` if the PRIOR bar's close was above the prior bar's SMA(`lookback_L`), else 0 | two values: 0 and +`sf`; never negative | on/off | forecast units | `lookback_L + 1` (101) | closes. A NaN SMA makes the comparison false: 0.0 | one-bar lag on both the close and the SMA (the engine fills at the bar close, so this approximates a next-bar entry). Long or flat only; stateless. Graded alternative: `MovingAverageDistanceComponent` (`average` "sma", `period` e.g. 100; a `clip` with `min` 0 keeps it long-only). |
| `GatedSmaTrendLongOnlyComponent` | `lookback_L` (100), `scaling_factor` (10.0), `er_period` (20), `gate_threshold` (0.30) | `sf` while an episode is open, else 0. An episode opens on the bar the SMA signal (prior close above prior SMA) turns on AND the raw Kaufman ER(`er_period`) of the prior bar is >= `gate_threshold`; it stays open while the SMA signal stays on, whatever ER does, and closes when the signal turns off. A rejected entry is not retried until the signal turns off and on again | two values: 0 and +`sf`; never negative | on/off | forecast units | `max(lookback_L + 1, er_period + 2)` (101) | closes. A NaN SMA makes the signal false: 0.0 | stateful; the output can depend on the first ready bar (an SMA signal that is already on when the component first becomes ready is treated as a fresh transition, so the ER gate is applied to it). One-bar lag like `SmaTrendLongOnlyComponent` |
| `BuyAndHoldStrategy` | none | +10 on every bar, from the first bar; needs no history | constant +10 (allocation +1.0) | constant | forecast units | 0 | reads no column | ignores every param. Use it only as an offset in a composition (see the design guide, "Composing a signal"); on its own it is the buy-and-hold baseline, not a signal |

### Hedges and filters

| Class | params (defaults) | Exact output | Range & sign | Kind | Units | Warmup | Data & NaN | Notes |
|---|---|---|---|---|---|---|---|---|
| `PriceOverextensionHedgeComponent` | `period` (21), `scaling_factor` (2.0) | -z x `sf`, z = (close - EMA_period) / rolling std of the closes over `period` (z = 0 if that std is 0); EMA has `span` = `period`, adjust=False | unbounded, signed; contrarian: negative when the close is above its EMA, positive when below | graded | z-score x `sf` | `period` (21) | closes. A NaN close in the window makes the rolling std NaN, which reads as "not above 0": the output is 0.0 for `period` bars | a mean-reversion reading of the distance from the EMA; a negative `sf` turns it into trend-following. The name "hedge" describes the intended role, not a different mechanism |
| `VolumeExpansionHedgeComponent` | `vol_period` (24), `scaling_factor` (20.0) | only on UP bars (close above the previous close) whose volume is BELOW its `vol_period` average (the average includes the current bar): -(1 - volume / average) x `sf`; on every other bar 0 | -`sf` to 0; never positive; zero on most bars (-`sf` is reached only at zero volume) | on/off | forecast units | `vol_period + 1` (25) | volume and close. If the average volume is 0 or NaN the comparison is false: 0.0 | the name is misleading: it fires on LOW-volume up-moves (a weak-volume rally), not on a volume expansion, and it can only push the forecast down. It sits at 0 and steps to a level when the condition fires |
| `VolatilityFromStdDevComponent` | `vol_period` (20), `scaling_factor` (1.0, unused) | population standard deviation (ddof 0) of the last `vol_period - 1` one-bar returns (close change divided by the current close), times 100 | 0 and up, unbounded; never negative; no direction | graded | percent | `vol_period` (20) | closes. A NaN close gives NaN for `vol_period` bars | `scaling_factor` is read but never used. Always non-negative, so as a forecast it is a long position that grows with volatility; its natural use is as a regime input (a rule such as "volatility above a level"). Its level depends on the timeframe |

### Feed-based components (non-OHLCV data)

| Class | params (defaults) | Exact output | Range & sign | Kind | Units | Warmup | Data & NaN | Notes |
|---|---|---|---|---|---|---|---|---|
| `FundingRateMeanReversionComponent` | `threshold` (0.001), `scaling_factor` (10.0) | -sign(funding_rate) x `sf` on a bar whose UTC hour is divisible by 8 (hour 0, 8 or 16) when abs(funding_rate) > `threshold`; 0 on every other bar. `threshold` 0.0 fires on every such bar whatever the size | three values: -`sf`, 0, +`sf` (clipped to +/-20); contrarian: negative when funding is positive | on/off | forecast units | 2 | needs the `funding_rate` column and `timestamp`. A MISSING funding column gives 0.0 silently (not NaN). A NaN funding value on a settlement bar gives NaN | the timing test is the hour only (no minute check): on 1h bars 1 bar in 8, on 4h bars hours 0, 8, 16 (1 bar in 2), on 1d bars (timestamp hour 0) EVERY bar qualifies. The output is one of two levels, so `threshold` 0.0 is still not graded. Funding values are per-8h rates (0.001 = 0.1 percent) Graded version: `FundingRateComponent`. |
| `FundingRateComponent` | none | -funding_rate x 10000 on every bar: the latest funding print in basis points, sign flipped | unbounded, signed; contrarian: negative when funding is positive (longs pay); a print of 0.0001 (0.01%) gives -1 | graded | basis points of one print (Binance: 8h prints; Kraken Futures: hourly) | 2 | `funding_rate`, carried forward between prints (the latest print at or before the bar; on 1d bars the day's last print). A missing column, None or NaN gives NaN | the graded version of `FundingRateMeanReversionComponent`: no threshold, no `scaling_factor`, stateless; scale it with transforms |
| `FearGreedContrarianComponent` | `fear_threshold` (25.0), `greed_threshold` (75.0), `scaling_factor` (10.0) | +`sf` if the Fear and Greed value (prior day's, the feed applies the +1 day shift) is below `fear_threshold`, -`sf` if above `greed_threshold`, else 0; evaluated only on bars whose UTC hour is 0 | three values: -`sf`, 0, +`sf` (clipped to +/-20); contrarian | on/off | forecast units | 2 | needs the `fear_greed` column and `timestamp`. A MISSING column gives 0.0 silently. A NaN value on an hour-0 bar gives NaN | the timing test is the hour only: on 1h bars 1 bar in 24, on 1d bars every bar. The index is 0 to 100. Graded version: `FearGreedComponent`. |
| `FearGreedComponent` | none | 50 - fear_greed on every bar (the prior day's index value: the feed is used one day after its date) | -50 to +50; contrarian: positive in fear (index below 50), negative in greed | graded | index points | 2 | `fear_greed`, carried forward between daily values. A missing column, None or NaN gives NaN | the graded version of `FearGreedContrarianComponent`: no thresholds, no `scaling_factor`, stateless; scale it with transforms |
| `WhaleLargeTradeImbalanceComponent` | `persistence_bars` (3), `min_abs_imbalance` (0.5), `scaling_factor` (10.0) | when `whale_lt_imbalance` holds ONE sign with abs value >= `min_abs_imbalance` on each of the last `persistence_bars` consecutive attested bars: mean(`whale_lt_imbalance`) x `sf` (continuation, sign NOT inverted); 0.0 when the whole window was measured but the imbalance was not sustained; NaN (abstain) if any bar of the window is unattested or unmeasured, or a needed column is absent | NaN, 0, or a value of magnitude between `min_abs_imbalance` x `sf` and `sf` with the imbalance's sign | on/off | forecast units | `persistence_bars` (3) | needs the `whale_lt_imbalance` and `whale_attested` columns, which are reserved feeds (see the feeds section below). A missing column gives NaN | NaN is deliberate (abstention) and propagates: a NaN component value makes the whole regime forecast NaN for that bar. Do not flip its sign with a negative `sf` or `negate`: that inverts the hypothesis it encodes. Stateless |

<!-- CATALOG:END -->

## Variant patterns (graded use)

- **Default direction.** Trend-following at a positive `scaling_factor`: `EMASpreadComponent`, `PriceEvolutionComponent`,
  `PriceEvolutionOnPeriodComponent`, `MacroTrendFilterComponent`, `DonchianBreakoutComponent`,
  `KeltnerBreakoutComponent`, `EMADiff`. Contrarian by default: `RSIPullbackComponent`,
  `PriceOverextensionHedgeComponent`.
- **Reversing a direction.** The `negate` transform reverses any graded component. A negative `scaling_factor` works only
  on the classes that use it: it is ignored by `PriceEvolutionOnPeriodComponent`, `MomentumDivergenceComponent` and
  `VolatilityFromStdDevComponent`, and `EMADiff` has none.
- **Magnitude.** `scaling_factor` multiplies the output; it does not change when the sign changes. Under the
  `ratio_to_mean`, `zscore` and `percentile` transforms a component's `scaling_factor` cancels and only its sign
  survives (see the design guide, "Transform ops").

## Feeds (non-OHLCV data)

A component that reads a column which is not in the plain OHLCV bars declares it in a class attribute,
`consumes_feeds`. The engine collects those declarations across the whole config (every regime, active or not)
into the list of feeds the run needs, and the backtest refuses to start if a required feed is not registered. Every
registered feed is merged onto the bars of every backtest, so these columns are on the bars whether or not a
component reads them (unless the run explicitly drops a feed; that is a run option, not a config key):

| Feed name | Column it adds | How it is merged |
|---|---|---|
| `funding_rate` | `funding_rate` | backward as-of join of the 8h funding print onto the bar timestamps |
| `fear_greed` | `fear_greed` | backward as-of join of the daily index, with a +1 day shift already applied so a bar never sees a value published after it |

Consumers: `FundingRateMeanReversionComponent` reads `funding_rate`; `FearGreedContrarianComponent` reads
`fear_greed`; so do their graded versions `FundingRateComponent` and `FearGreedComponent`. The two originals are on/off (see the kind column) and cannot be a forecast source; the graded versions can.

The whale-footprint columns are RESERVED, not merged by default: a caller must opt in by name, and the campaign
data policy must carry a committed designation for the window, otherwise loading them raises `ReservedDataError`.
`WhaleLargeTradeImbalanceComponent` needs two of them, `whale_lt_imbalance` and `whale_attested`, and abstains
(NaN) when either is missing.

The top-level `aux_feeds` key of a strategy config is NOT what gives a component its data: the engine ignores it.
It is read only by the research tooling: listing a feed there makes the pipeline's data-availability gate check that feed's coverage of the test windows and lets
the campaign tools know which feeds a config depends on. An entry is a feed name, for example
`"aux_feeds": ["fear_greed"]`, or a mapping with a `name` key. A config that uses a feed-based component should
list its feed there.

## Other names a config may use (names only)

For a reader that does not have the design guide. The guide defines each one; this lists the complete sets, so a
name outside them is invented.

- **Regime names** (the only four): `trending`, `mean_reversion`, `chop`, `unknown`.
- **Transform ops** (the only fifteen). History ops, which must come first in a pipeline: `identity`, `percentile`,
  `negate_percentile`, `zscore`, `ratio_to_mean`, `ema`. Scalar ops: `scale`, `threshold_filter`, `clip`, `sigmoid`,
  `negate`. Data-aware ops: `vol_normalize`, `vol_adjusted`, `price_normalized`, `volume_filter`.
- **Regime-rule operators**: `gte`, `gt`, `lte`, `lt`, `between` (with `low` and `high`).
- **Regime detector modes**: `threshold_rules`, `score`, `score_product`.
