---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins
line: 7.g patterns
backtest: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: Among 24-hour stretches where a coin's range is several times its 30-day average and the coin fell, the deeper the coin's fall over those 24 hours, the higher its return over the following 14 days.
Consequence: A trader buys after a panic in proportion to how far the coin fell during it, rather than waiting for a bounce.
Why:
- F1: Among the 492 panic stretches (24-hour range at least 3 times its 30-day mean, coin down; first one per 84-bar cell), a deeper 24-hour fall is followed by a higher 14-day excess return. The pooled slope of excess return on the 24-hour return is -0.325 (t -2.45). The deepest quartile (mean fall -22 %) earns +5.9 % excess (t 3.11, 123 cases), against -1.3 %, +0.2 % and +2.0 % for the shallower quartiles.
- F2: The depth effect in F1 is fragile. Averaged by day (171 panic days) its slope t falls to -1.65. Measured in units of the coin's own volatility, the slope is +0.003 (t 0.34, 455 cases). The slope is negative in each year from 2018 to 2023 (t -2.38 in 2021, -2.39 in 2022) but positive in 2024 (+0.22) and 2025 (+0.11). It is negative in only 65 % of the 17 coins.
- F3: Panic stretches as a whole earn a 14-day excess of +1.7 % over the coins' normal drift (t 1.67, 492 cases). The excess is not graded by the panic's range multiple: by quartile it is -1.4 %, +4.3 %, +4.1 % and -0.2 %. It is not graded by the prior 7-day return either: +5.8 %, +1.1 %, -4.2 % and +5.8 %.
