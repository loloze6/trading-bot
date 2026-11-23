---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound
line: 7.b inconclusive
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Saturday-to-Sunday close-to-close fall, measured in percent of its price, is followed by a rise over the next 3 days (Monday to Wednesday), and the deeper the percent fall, the larger that rise.
Consequence: Size a Monday-to-Wednesday long by the percent depth of the weekend fall itself rather than by the fall in units of recent volatility, whose deepest readings do not rebound most.
Why:
- F2: Deep Sunday falls measured in usual daily moves do not rebound most. Sunday z below −3 gives +5.7 % but on only 8 cases, and z from −3 to −2 gives −1.76 % (t −1.14, 63 cases). The rebound sits at z from −1.5 to −0.5: +2.40 % (t 3.35, 232 cases) and +1.28 % (t 3.75, 691 cases).
- F3: Measured in percent, the Sunday fall is cleanly graded. Excess 3-day returns are +0.95 % (t 2.7) for falls of 1.5–3 %, +1.85 % (t 3.8) for 3–5 %, +2.31 % (t 3.0) for 5–8 % and +3.11 % (t 2.3) beyond 8 %. Sunday's own return has the strongest reversal slope of any weekday on the next 3 days: −0.234 (t −7.6), against −0.10 to +0.07 on the other weekdays.
- F6: The effect is spread across coins: 17 of 19 coins have a positive mean excess return. DOGE is the exception (−2.08 %, t −2.3, 93 cases). No more data is available than the test used, which already covered all 19 coins on all four folds of daily bars.
