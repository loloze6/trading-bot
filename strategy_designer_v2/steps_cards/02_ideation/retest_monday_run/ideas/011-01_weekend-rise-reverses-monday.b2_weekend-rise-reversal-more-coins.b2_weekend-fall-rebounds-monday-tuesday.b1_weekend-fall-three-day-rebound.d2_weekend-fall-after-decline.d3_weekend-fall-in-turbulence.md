---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 3 days (Monday to Wednesday), the larger the weekend fall, the larger the rise, and the rise is larger the higher the coin's 20-day volatility stands against its 60-day volatility.
Consequence: Favour weekend-fall buys when the coin has turned turbulent, and keep them small in calm stretches where the rebound barely shows.
Why:
- F4: The rebound is larger when the coin's last 20 days were turbulent against its last 60. The top quartile of the 20-day/60-day volatility ratio gives +3.33 % excess (t 5.86) and the bottom quartile +0.57 % (t 0.67). The same quartiles on Sundays without the signal earn −0.30 % (t −0.69) and −1.56 % (t −4.14), so turbulence alone does not earn. Cases above the median ratio cut the case-book's deepest fall from 17.1 % to 4.8 %, with the same gain-to-fall ratio (8.6). The 20-day volatility level grades the same way, from +0.32 % (t 0.62) to +4.03 % (t 5.37).
- F5: The 20-day decline already grades the rebound inside the active cases, but it does not keep the book out of crashes. The quartile with the deepest 20-day fall gives +3.38 % (t 5.14) against +0.88 % (t 1.54) for the shallowest. The worst falls nonetheless come from broad sell-offs. The worst single Sunday had 12 coins active at once, a mean excess of −30.4 % and a summed position loss of 2.82. The worst-decile Sundays carried larger positions (mean allocation 0.71 against 0.55).
- F1: The check failed on Calmar alone (0.568 against 0.75). A yearly return of +14.5 % meets a deepest fall of 25.6 %, built over 48 days from window w1 into w2 while the coins fell 59.5 %. In w2 the 73 active weekend-fall cases lost against the coin's drift (mean excess 3-day return −5.12 %, t −3.17), and in w17 the 30 cases did the same (−7.54 %, t −3.31). The other falls were 13.8 % (w17–w18), 11.7 % (w15–w16) and 10.5 % (w11–w13).
