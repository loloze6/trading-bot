How a strategy config turns its components into a forecast, and so into a position. Given to step 3 (which writes the
config) and step 5 (which checks the backtest against its plan); written after step 5 judged correct backtests a
mismatch by guessing what `standardise` does (the step 5 mismatch analysis, 2026-11-17). From the engine's code
(`trading-bot/strategies/strategy_engine.py`, `registry.py`), 2026-11-17.

**In one line:** at each bar's close, each component gives a raw value; its transforms turn it into a value on the
forecast scale; the regime's forecast is the weighted mean of those values, clipped to -20..+20; the position is that
forecast divided by 10, scaled by the coin's volatility.

1. **The regime.** The regime detector chooses the bar's regime. A regime with no strategy (`null`) gives forecast 0
   (flat) on its bars.
2. **A component's raw value** at bar t: what the component computes from the bars up to t (the catalogue's "exact
   output"). Recorded as `debug_info.components.<id>.last_history_value`.
3. **Its transforms**, in order, on the component's past raw values. The one every config uses first:
   - `standardise`: value(t) x 10 / (the mean of the absolute values of its last `window` raw values, bar t left out),
     capped at -20..+20; 0 until `min_periods` past values exist, and 0 when that mean is 0.
   - **It scales; it does not centre.** The sign is kept: a component that is always negative (the distance below a
     high) stays always negative after it, about -10 on average; one always positive (a volume ratio, a share) stays
     always positive, about +10. A constant (`BuyAndHoldStrategy`, +10) stays +10.
   - So "above its usual level" is not what `standardise` gives. A component's sign after it is its raw sign.
   The value after all its transforms is recorded as `debug_info.components.<id>.post_pipeline_value`.
4. **The forecast** = the sum of (weight x value after transforms) over the regime's components, divided by the sum of
   the weights, clipped to -20..+20. Its sign is the sign of that weighted mean, so it depends on the components' sizes,
   not only on their signs: the mean of an always-negative component (about -10) and an always-positive one (about
   +10) is near 0, and its sign flips from bar to bar.
5. **Centring on a usual level** needs an offset: a constant (`BuyAndHoldStrategy`, standardised: +10, or -10 with
   `negate`) of the opposite sign, at the same weight as the measure:
   - an always-positive measure (a volume ratio) + the constant at -10: the forecast is positive when the measure is
     larger than its past mean size (heavier than usual), negative when smaller;
   - an always-negative measure (the distance below the high) + the constant at +10: positive when it is smaller in
     size than its past mean (nearer the high than usual), negative when larger.
   A check of the forecast's sign uses the values after transforms (`post_pipeline_value`), or rebuilds them exactly
   as above from the raw values (`last_history_value`): never the raw value plus the constant.
6. **The position** (`postRebalance_current_allocation`) = forecast / 10 x (the target volatility / the coin's realised
   volatility), capped; a trade too small to matter is skipped, so the position can keep its previous sign for a few
   bars after the forecast changes sign.
7. **The holding period** (2026-11-19, operator; `topics/30_why-hourly-ideas-rarely-pay.md`). An idea claims a move
   over its horizon ("it rises over the next 24 hours"), so its book holds the position it takes for that horizon:
   `strategies.min_holding_bars` = the idea's horizon in bars. After the book trades, it does not trade again for that
   many bars, whatever the forecast does meanwhile; then it follows the forecast again. The horizon is the idea's own,
   never a value chosen from the data (a longer hold also collects the market's drift). Why: on hourly bars, books that
   followed the forecast every hour held a 24-hour idea for 1 hour, or re-sized every hour, and paid their costs
   without earning the move (topic 30: 0.3 to 4.6 bps earned per unit traded, against about 10 of cost).
