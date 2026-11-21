# Component wish list

One block per idea that needs components the catalogue does not have.

## 020-02_support-retest-bounces-up.d1_support-bounce-in-uptrends_1d
- Component: SupportRetestTrendWeightedComponent: computes the nearness-weighted count of swing lows from `low` (period 90, side 2, band 1.5, gated on close below close 5 bars ago) times max(0, close[t]/close[t-90] - 1) x 100 from `close`. It is 0 with no retest or a non-positive 90-day return, and grows with the touch count, the closeness to the level and the size of the 90-day rise | measures: situation

## 020-03_resistance-breakout-continues-up.d1_held-breakout-keeps-rising_1d
- Component: HeldResistanceBreakDepth: from closes, find L, the highest close-based swing-high level of the 90 bars before the break that close[t-3] <= L < close[t-2] crossed, and N, the number of swing highs within a 2 % band of L; output N x (min(close[t-1], close[t]) - L) / L x 100 when both close[t-1] and close[t] are above L, else 0; it grows with the level's touch count and with how far above the level the 2 later closes held | measures: comparison

## 020-04_support-breakdown-continues-down.d1_support-break-after-mild-decline_1d
- Component: FallDampedSupportBreakDepth: from low and close, the touch-weighted depth of the close below a 90-day swing-low level (as `TouchWeightedSupportBreakDepthComponent`), divided by (1 + max(0, -10-day close return in percent)). It is 0 with no break, grows with the touch count and the depth below the level, and shrinks as the prior 10-day fall deepens. | measures: situation
- Component: FallDampedSupportBreakDepth (same component, its damping factor): 1 / (1 + max(0, -(close[t]/close[t-10] - 1) x 100)), from closes, falling from 1 toward 0 as the 10-day fall deepens. | measures: comparison

## 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b1_breakout-continues-within-uptrend_1d
- Component: ResistanceBreakMomentumComponent: N x (close[t] - L) / L x 100 (as in `ResistanceBreakTouchCountComponent`: period 90, side 2, band 2, cross_period 1, from closes) times max(0, (close[t] / close[t-30] - 1) x 100); it is 0 with no recent upward break or a 30-day return of 0 or less, and grows with the level's touch count, the close's margin above it and the size of the 30-day rise | measures: situation

## 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.d1_resistance-break-with-rising-trend_1d
- Component: ResistanceBreakMomentumComponent: from closes, computes N x (close[t] - L) / L x 100 x max(0, (close[t] - close[t-20]) / close[t-20] x 100). L is the highest close-swing-high level with close[t-1] <= L < close[t] in the last 90 bars, and N is its touch count within the band. The value is 0 with no break or after a 20-day fall, and it grows with the touches, the margin above the level and the prior 20-day rise. | measures: comparison

## 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.d2_resistance-break-near-highs_1d
- Component: ResistanceBreakHighProximityComponent: the `ResistanceBreakTouchCountComponent` output from closes (period 90, side 2, band 2, cross_period 1) times (1 / (1 + D))^power, where D is the percent distance of close[t] below the highest of the last 60 closes. It is 0 with no break, and grows with the level's touch count, the close's margin above the level, and its nearness to the 60-day high. | measures: comparison

## 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d2_fresh-breakout-carries-further_1d
- Component: BreakoutAgeWeightedDistanceComponent: from closes, find the most recent bar b at which close[b] first exceeded the highest of closes b-90..b-1 and after which every close stayed above that level L. Output max(0, (close[t] - L) / L x 100) x (1 / (1 + (t - b)))^power, and 0 when no such run is live. It grows with the margin above the breakout level and shrinks as the breakout ages | measures: situation
- Component: BreakoutAgeComponent: from closes, the number of bars t - b since the close first broke its prior 90-day closing high in the current run above that level, as a graded freshness weight such as 1 / (1 + t - b). It is larger the younger the breakout and 0 outside a run | measures: comparison
