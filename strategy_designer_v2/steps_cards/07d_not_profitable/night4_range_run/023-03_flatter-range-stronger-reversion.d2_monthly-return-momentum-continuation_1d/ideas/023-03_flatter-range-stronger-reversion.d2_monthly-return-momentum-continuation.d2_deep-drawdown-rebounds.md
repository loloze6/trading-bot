---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation
line: 7.d not profitable
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's close stands below its highest close of the past 60 days, the larger its rise over the next 5 days.
Consequence: A coin that has already fallen far from its 2-month high is a reason to refuse a short and lean long for the coming days.
Why:
- F3: The short side is a net drain over the whole record: it lost in 16 of 24 windows (for example −0.138 in w5 and −0.107 in w3), and it gained clearly in only two (+0.218 in w2, +0.284 in w14).
- F4: Shorts lose most when the coin is already deep below its 60-day high: in the deepest fifth (43 % to 70 % below it) shorts earned −0.243 % per bar (t −2.44, 868 bars); in the fifth 15 % to 24 % below it they earned +0.145 %. Likewise shorts after a 90-day fall of 40 % to 82 % earned −0.186 % (t −1.08, 427 bars).
