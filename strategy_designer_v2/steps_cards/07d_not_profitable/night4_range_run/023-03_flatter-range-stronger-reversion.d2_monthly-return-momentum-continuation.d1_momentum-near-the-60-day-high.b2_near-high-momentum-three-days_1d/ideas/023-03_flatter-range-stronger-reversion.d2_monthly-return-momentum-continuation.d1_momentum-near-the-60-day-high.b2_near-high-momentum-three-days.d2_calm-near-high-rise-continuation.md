---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b2_near-high-momentum-three-days
line: 7.d not profitable
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b2_near-high-momentum-three-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 30-day rise, the larger its rise over the next 3 days, the more so the closer the coin's close stands to its highest close of the past 60 days, only while its daily moves over the past 60 days have been calm, and the calmer they have been the larger the rise.
Consequence: A trader leans long on calm monthly strength near the 2-month high, and takes no short side on monthly weakness, which lost money in the bear windows.
Why:
- F6: Longs earn most when the coin's daily moves over the past 60 days are calmest: +0.400 % per bar (t 3.52, 1169 bars) in the lowest 60-day-volatility quintile, against −0.000 % to +0.102 % (t ≤ 1.74) in the other four.
- F4: The short side, monthly weakness, carries nothing: shorts summed −0.34 over 5086 bars (mean −0.007 %). No distance-from-high tercile of shorts has |t| above 0.61.
- F2: In w1–w8 the book earned nothing on its longs (mean bar gain +0.015 %, t 0.33, 3134 bars) and lost on its shorts (−0.101 %, t −2.39, 1918 bars). Its longs were also its largest there (mean position 0.54 against 0.35 in later windows). Later, the longs earned +0.178 % per bar (t 5.33, 7209 bars).
- F1: The book fails on its falls, not its gain: its yearly return is 22.0 % against a deepest fall of 46.4 % (Calmar 0.47). That fall built up over 887 days across windows w1 to w8, while the coins fell 56.6 %; the other falls are 27.0 % (w12–w14, coins −58.8 %) and 18.5 % (w21–w22).
- F3: The book's gain sits in longs whose close is near its 60-day closing high. Longs in the nearest quintile summed 9.13 of the 13.31 total long gain (mean +0.37 % per bar). Longs in the other four quintiles earned between +0.007 % and +0.039 % per bar.
