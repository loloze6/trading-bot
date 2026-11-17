---
brief: 013_anchoring-to-recent-high
source-idea: 013-02_follow-through-stronger-near-high
line: 7.d not profitable
backtest: 013-02_follow-through-stronger-near-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's past 30-day rise carries on into the next 30 days more strongly the closer the coin closes to its 52-week high, and the same past rise carries on less the further the coin sits below that high, while a past 30-day fall does not carry on and is followed by a coin's ordinary or better return over the next 30 days.
Consequence: A trader would buy coins after 30-day rises, sized by nearness to the 52-week high, and would not short after 30-day falls, since in this data those shorts caused the deepest fall.
Why:
- F1: The book's deepest fall, -52.4 % of the daily-return chain, ran from w2 to w10, and in w2–w10 the shorts lost a summed -2.20 (mean -0.00097 per bar over 2256 bars) while the longs earned only +1.17 (mean +0.00045 over 2580 bars); in w11–w24 the longs earned +9.43 (mean +0.0019 over 4962 bars) and the shorts +0.29.
- F2: Over all bars the longs carry the book: mean gain +0.0014 per bar and sum +10.60 over 7542 bars, against -0.0005 and -1.90 over 3787 short bars, and short trades average -1.22 % after fees against +6.82 % for long trades.
- F3: Every coin's shorts lose except ZEC: BTC -0.07, ETH -0.17, LTC -0.98, XMR -0.39 and XRP -0.70 summed, against ZEC +0.42.
- F4: Past falls do not carry on. On the non-overlapping 30-bar grid the forward 30-bar return after a falling past 30 days is positive both near the high (+5.6 %, n=62) and far below it (+0.8 %, n=127), while after a rise near the high it is +8.1 % (n=131).
- F5: The long gain is concentrated near the 52-week high: longs in the shallowest depth quintile earn +0.00274 per bar (n=2166), falling steadily to +0.00077, +0.00023, +0.00011 and -0.00008 (n=650) in the deepest quintile.
- F6: Shorts lose in the shallowest depth quintiles too: -0.00112 per bar (n=284) and -0.00125 (n=548).
- F7: Removing the shorts lifts both failing measures. On a recomputed long-only book the mean daily return rises from 0.00051 to 0.00062, Calmar from 0.36 to 0.82 and the deepest fall from -47 % to -27 %. Sharpe rises from 0.78 to 1.00.
