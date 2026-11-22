---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days.b1_bounce-regime-gap-more-coins
line: 7.d not profitable
backtest: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days.b1_bounce-regime-gap-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin down over 90 days, the larger its 20-day return, the more it rises over the next 20 days.
Consequence: A trader would not stay short a falling coin that has rallied strongly over the past 20 days, since the rally tends to extend rather than fade.
Why:
- F3: Short holding pays only when the coin has already fallen hard over 20 days, and the result is graded. Short bars in the lowest quintile of the coin's 20-day return (mean -25.7 %) gain +0.274 % per bar. The middle quintiles gain -0.009 % and -0.063 %, the next -0.153 %, and the highest quintile (mean +32.5 %) loses -0.422 % per bar, over about 2,949 bars each.
- F4: The book's falls come from shorts squeezed in coins that were already rising. The worst 2 % of bars include 445 short bars summing -80.8, on which the coin rose 11.9 % the next day after a mean 20-day return of +22.0 % and a 5-day return of +8.5 %. The long bars among them sum only -37.5.
- F6: The fades are short-side losses spread over many periods. Short-side gain is deeply negative in w4 (-7.65), w6 (-12.58), w16 (-4.74) and w21 (-7.21), all windows where holding the coins rose (+0.51, +0.76, +0.63, +0.85 summed). The book lost in those same windows (-0.48, -0.38, -0.87, -0.03).
