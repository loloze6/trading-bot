---
brief: 023_range-reversion-when-no-trend
source-idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues
line: 7.g patterns
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move is down and large against its 30-day high-low range, the deeper its 10-day fall, while that fall stays within its usual 10-day moves of the last 60 days, the more it keeps falling over the next 5 days.
Consequence: A declining coin that slides moderately within its usual pace is a short to take, sized up with the depth of the slide, while declining coins whose slide has exceeded their usual pace are refused as shorts.
Why:
- F4: In coins with a clear 30-day decline (signed 30-day net move below −0.3 of its high-low range), a moderate 10-day fall keeps falling over the next 5 days. A fall of 0.5 to 1 usual 10-day moves is followed by −2.81 % unusual (t −3.51, 168 cases); one of 0 to 0.5 usual moves by −1.92 % (t −2.89, 159). Falls beyond one usual move rebound instead (+1.48 %, +2.12 %, +0.96 %, all t below 1.9).
- F5: That downtrend continuation holds in 5 of 6 coins (LTC t −2.71, XRP t −2.85, ZEC t −2.68; XMR +0.49 %) and in 7 of 8 years (2022 the exception, +3.39 %, t 2.73). Its total 5-day move is −1.79 % (t −3.43, 327 cases), about 9 times the cost of a trade.
- F6: The tested flat-range short has no grading. Quartiles of forecast from most to least negative give long-side unusual moves of −0.29 %, −1.13 %, −2.30 %, −0.66 % (109 each), and the step-5 half check is −0.77 %. Across windows the active cases split 14 negative to 10 positive (w18 −16.4 %, w11 +11.6 %), and ZEC alone carries a t of −2.99.
