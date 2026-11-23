---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Sunday close-to-close move, a fall or a rise, is partly undone over the next 3 days, and the thinner the weekend's volume against the coin's usual 20-day volume, the larger the share of the move that is undone.
Consequence: A trader would fade a Sunday move into the start of the week, leaning harder the thinner the weekend's volume was, and would refuse to fade Sunday moves made on heavy volume.
Why:
- F1: On the Sunday bar, a coin's 1-day move reverses over the next 3 days, and it reverses most when weekend volume was thin. Over all Sundays the slope of the standardised excess 3-day return on the Sunday z-score is −0.085 (t −3.76, 4041 cases; t −1.75 when the coins are averaged per date over 338 dates). On Sundays whose two-day weekend volume is below the coin's median, the date-clustered t is −2.36 over 298 dates, against −1.37 over 316 dates for the high-volume half.
- F2: In the thin-volume Sundays the reversal is graded across the whole range of the move and covers rises as well as falls. By Sunday z-quintile, the excess 3-day return runs +1.36 %, +1.27 %, −0.41 %, −1.26 % and −1.12 % (about 398 cases each). In a regression over all Sundays, the term z × log(weekend volume ratio) is +0.065 (t 1.93): the thinner the weekend, the stronger the reversal.
- F3: The thin-weekend reversal is broad across coins and years. Its slope is negative in 15 of 19 coins (79 %; in LINK t −3.93, AAVE −2.94, NEAR −2.37, ETH −2.17). It is negative in 7 of 8 years, with 2022 the exception (+0.018, t 0.12). No single year is significant on its own (|t| at most 1.29).
- F4: On weekdays there is no such reversal. On Monday-to-Thursday bars the slope on z is +0.008 (t 0.68), and its interaction with volume is +0.022 (t 1.57). The slope on z is negative only on Sunday; Wednesday, Friday and Saturday show positive slopes (t 2.86, 3.79, 3.26 unclustered).
- F5: The tested idea's volatility leg is not supported: Sunday falls rebound no more when recent volatility is high. Within Sunday falls, the slope is −0.35 (t −2.82) in the calmest volatility tercile and −0.24 (t −1.74) in the most agitated, with 271–272 cases each. Over all bars, weekend slopes are −0.02, −0.08 and −0.03 across calm, mid and agitated terciles.
