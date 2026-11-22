---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation
line: 7.d not profitable
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 30-day return, the larger its rise over the next 5 days, the more so the closer the coin's close stands to its highest close of the past 60 days.
Consequence: A trader leans long on monthly strength most when the coin is at or near its 2-month high, and trusts monthly weakness least when the coin has already fallen far from that high.
Why:
- F1: The Calmar failure comes from one long fall: the book's daily chain reached its deepest fall of −55.6 % by w10 against a yearly return of only 23.2 % over 7.9 years, and the fall built steadily from −22.8 % in w1 to −54.0 % in w8 and −53.2 % in w9, while its worst fall inside any single window was only −8.8 % to −27.5 %.
- F3: The short side is a net drain over the whole record: it lost in 16 of 24 windows (for example −0.138 in w5 and −0.107 in w3), and it gained clearly in only two (+0.218 in w2, +0.284 in w14).
- F4: Shorts lose most when the coin is already deep below its 60-day high: in the deepest fifth (43 % to 70 % below it) shorts earned −0.243 % per bar (t −2.44, 868 bars); in the fifth 15 % to 24 % below it they earned +0.145 %. Likewise shorts after a 90-day fall of 40 % to 82 % earned −0.186 % (t −1.08, 427 bars).
- F5: Longs gain in step with closeness to the 60-day high: +0.512 % per bar within 1.5 % of it (t 2.92, 909 bars), +0.350 % at 1.5 % to 5 % below it (t 2.94), down to +0.026 % and +0.101 % in the two deepest fifths.
