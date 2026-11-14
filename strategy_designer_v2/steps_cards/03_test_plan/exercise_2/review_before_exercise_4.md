# Exercise 2 (one call): a second critical review, before exercise 4

Two passes over the 12 one-call plans of exercise 2. The first pass is the config against the engine. The second is the criterion against the data it will meet. Facts I checked are marked as checked; the rest is reading.

## Pass 1: the configs

1. **Class and parameter names are clean.** Checked: every class and every `params` key, in all 30 configs of exercises 1 to 3, exists in the catalogue. A misspelt key would be silently ignored by the engine, so this matters, but it has not happened yet.
2. **"Fading after the event" cannot be built.** `standardise` must be the only history op in `transforms` (V15), and `ema` is a history op. A history op in `history_transforms` sees one value. So, under the standardise-first rule, no config can hold or fade a position after the situation ends. Every event idea becomes "a position while the situation lasts". The models half know it: exercise 1 deviations said "fading"; exercise 2 deviations say "while". The prompt's own example, "while X, fading", suggests something that cannot be built.
3. **The position is often shorter than the horizon.** 003-01 holds a short for one bar; its criteria look 1 or 5 bars ahead. The RSI plans hold while RSI stays high and look 5 bars ahead. A criterion on the portfolio's gain then measures something else than a criterion on the forward return after the signal bar. Some plans mix both in one criterion.
4. **The forecast is rescaled against its own recent past** (`standardise`, 60 bars). So "the top decile of the forecast" is not "the highest RSI readings": the same RSI gives different forecasts in a calm stretch and a busy one. Several criteria treat the two as the same. The record also holds each indicator's raw value per bar (`bars.csv`), but the model is not told so.

## Pass 2: the criteria against the data they will meet

5. **The models do not know how much data the test has.** Checked: the default (fold A, 1d bars) is six separate windows of about 120 daily bars each, 730 bars per coin. The plans ask for things this data cannot give:
   - **002-01:** "upward crosses" of a 50/200 average pair, about one every year or two. Six 4-month windows hold perhaps two or three.
   - **001-01:** "the top decile" of a daily RSI is about 70 bars per coin, in a handful of overlapping episodes.
   - **002-01, 002-05:** 20-bar horizons give about 6 independent blocks per window.
   - **Several inconclusive lines:** they guess the sample ("fewer than about 30 bars", "about ten crosses in the BTC daily history"). They don't know the test sees only six short windows.
6. **One idea, several tests.** The prompt asks for "the one result that would confirm". Most criteria hold three or four conditions joined by "and", or rejections joined by "any of". More conditions mean more ways to fail by chance, and a verdict that is harder to read.
7. **The bar of evidence varies** (t ≤ -2, one standard error, p < 0.05, "clearly"), and overlapping returns are counted only in some plans. This is still open for your ruling.
8. **Each idea is tested on BTC alone when its header names no coin.** For 003 (thin-volume moves), the brief itself says thin books are typical "outside the largest coins". BTC, the deepest book, is the least favourable coin for that idea. This is not a fault of the plans: it comes from the default data. It is noted here for your later ruling.

## Improvements that can be tested together in exercise 4

Each one leaves a mark that can be seen in the output, so their effects can be read one by one even when tested together.

| # | Change | Where | Fixes | Seen in the output as |
|---|---|---|---|---|
| A | First write the exact forecast the idea needs, in plain words; then the config; if the config cannot come close, answer "untestable" | prompt, plus a `forecast:` line in the output | divergence forced (exercise 3) | 005-01 untestable; a `forecast` line to compare with the config |
| B | Tell the model the data's size and shape: "N separate windows of about M bars each, per coin" (no dates) | script, data block | point 5 | criteria and minimum counts that fit 730 bars |
| C | Tell the model what the record holds: per bar, the forecast, each indicator's value, the position, the price and the portfolio's value; and that a position lasts only while the forecast is not zero (nothing can hold or fade it after) | prompt | points 2, 3, 4 | criteria read forward returns from the signal bars, or bucket on the indicator, not on the standardised forecast; no "fading" |
| D | One main measure, and at most one supporting check | prompt | point 6 | shorter confirm and reject lines |
| E | State the evidence required as a number, and count overlapping returns once | prompt | point 7 | a number in every confirm line (needs your ruling) |
| F | Check class and param names against the catalogue in code, and refuse an unknown one | script | point 1, before it happens | a refusal line in the log, if any |

**Not proposed now:**
- Changing the default data (point 8): that's your ruling.
- Removing the prompt's two examples: it would change too much at once.
