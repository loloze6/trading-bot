---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days.b1_bounce-regime-gap-more-coins
line: 7.d not profitable
backtest: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days.b1_bounce-regime-gap-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin, the 20-day return after a one-day rise of several usual daily moves (its day's return over the standard deviation of its last 20 daily returns) is lower when its 90-day return is negative than when it is positive, and the gap widens as the rise gets larger. In a coin down over 90 days, the fall over the next 20 days after such a rise is larger the more negative the coin's 20-day return before the rise.
Consequence: A trader would fade a sharp bounce in a coin down over 90 days only when it is still deep in a 20-day fall, more firmly the deeper that fall, and would refuse the short when the coin has risen over the past 20 days.
Why:
- F1: The book fails because its shorts lose. Bars held short sum to -17.37 of gain over 17,339 bars, while bars held long sum to +29.00 over 17,632 bars. The 1,913 SHORT trades average -15.4 % net (median -10.0 %, 30.4 % won), against +12.8 % for the 1,417 LONG trades. The book's Sharpe is 0.43 against holding's 0.60, and its deepest fall is -88.7 % against holding's -82.0 %.
- F2: The idea was confirmed as a relative gap, not as an absolute fall. Its short cases (777) end 20 days later 1.6 % below the coin's normal 20-day drift of +3.15 % (t 1.80), but their raw 20-day return is still +1.55 %. A short on a bounce in a coin down over 90 days therefore loses before costs, even though the bounce does fade relative to the coin's drift.
- F3: Short holding pays only when the coin has already fallen hard over 20 days, and the result is graded. Short bars in the lowest quintile of the coin's 20-day return (mean -25.7 %) gain +0.274 % per bar. The middle quintiles gain -0.009 % and -0.063 %, the next -0.153 %, and the highest quintile (mean +32.5 %) loses -0.422 % per bar, over about 2,949 bars each.
- F4: The book's falls come from shorts squeezed in coins that were already rising. The worst 2 % of bars include 445 short bars summing -80.8, on which the coin rose 11.9 % the next day after a mean 20-day return of +22.0 % and a 5-day return of +8.5 %. The long bars among them sum only -37.5.
- F6: The fades are short-side losses spread over many periods. Short-side gain is deeply negative in w4 (-7.65), w6 (-12.58), w16 (-4.74) and w21 (-7.21), all windows where holding the coins rose (+0.51, +0.76, +0.63, +0.85 summed). The book lost in those same windows (-0.48, -0.38, -0.87, -0.03).
