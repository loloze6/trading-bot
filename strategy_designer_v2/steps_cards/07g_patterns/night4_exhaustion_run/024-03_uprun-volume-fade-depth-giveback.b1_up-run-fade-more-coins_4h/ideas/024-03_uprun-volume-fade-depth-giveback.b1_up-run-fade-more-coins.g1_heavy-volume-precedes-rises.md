---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-03_uprun-volume-fade-depth-giveback.b1_up-run-fade-more-coins
line: 7.g patterns
backtest: 024-03_uprun-volume-fade-depth-giveback.b1_up-run-fade-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: The heavier a coin's traded volume over the past day relative to its average daily volume over the past 30 days, the higher the coin's return over the next 3 days. The lighter the volume, the more it lags its normal drift.
Consequence: A trader leans long a coin after unusually heavy one-day volume and refuses longs after unusually thin volume.
Why:
- F1: Over the next 3 days (18 bars, non-overlapping grid, coin drift removed), the coin's return rises steadily with its past-1-day volume against its 30-day mean volume. The bottom quintile (0.34× usual volume) gives −0.83 % (t −3.91, 2128 cases) and the top quintile (2.25×) gives +0.85 % (t +3.73, 2127 cases). In a joint regression with the past 1-day move and the down-streak loss, log relative volume keeps its slope (coefficient +0.0080, t +5.54). The top quintile beats the bottom on every coin (share 1.0) and in 6 of 8 years.
- F2: The gradient in F1 shows on both sides of the past day's move. After a 1-day fall, the volume quintiles run from −0.53 % to +1.39 % (top t +4.39, 995 cases). After a 1-day rise, they run from −0.88 % (t −3.77) to +0.60 % (t +1.86).
- F4: The past 1-day move on its own adds nothing once volume and the down-streak loss are in the regression. Alone, its lowest quintile gives +0.94 % (t +4.88), but its joint coefficient is −0.0001 (t −0.41).
