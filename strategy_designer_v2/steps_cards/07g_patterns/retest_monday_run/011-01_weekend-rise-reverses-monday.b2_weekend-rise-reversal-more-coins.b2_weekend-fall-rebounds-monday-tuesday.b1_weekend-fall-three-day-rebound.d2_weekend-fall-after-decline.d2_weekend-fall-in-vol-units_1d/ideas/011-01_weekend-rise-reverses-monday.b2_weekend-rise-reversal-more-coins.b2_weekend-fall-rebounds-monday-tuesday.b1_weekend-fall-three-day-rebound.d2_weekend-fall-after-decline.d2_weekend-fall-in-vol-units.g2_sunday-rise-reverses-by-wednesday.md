---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d2_weekend-fall-in-vol-units
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d2_weekend-fall-in-vol-units_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that rose on Sunday falls over the next 3 days. The fall is larger the larger that Sunday rise is in units of the coin's usual daily move over its past 60 days, and larger still when its 20-day return is negative.
Consequence: A Sunday rise during a 20-day decline is a reason to sell or short the coin through Wednesday rather than chase it.
Why:
- F3: Sunday rises reverse too, which the tested idea leaves out. After a Sunday rise of more than 1 usual move, the next 3 days run −1.10 % beyond drift (t −3.10, 699 cases). Only Sunday shows a strongly negative slope of the 3-day return on the day's scaled move (−0.0070, t −6.13); the other weekdays run from −0.0020 to +0.0034.
- F4: The Sunday-rise reversal is strongest in a 20-day decline. Rises in the lowest third of the 20-day return run −1.60 % (t −5.01, 537 cases), the middle third −0.88 % (t −2.69) and the top third −0.19 % (t −0.40).
