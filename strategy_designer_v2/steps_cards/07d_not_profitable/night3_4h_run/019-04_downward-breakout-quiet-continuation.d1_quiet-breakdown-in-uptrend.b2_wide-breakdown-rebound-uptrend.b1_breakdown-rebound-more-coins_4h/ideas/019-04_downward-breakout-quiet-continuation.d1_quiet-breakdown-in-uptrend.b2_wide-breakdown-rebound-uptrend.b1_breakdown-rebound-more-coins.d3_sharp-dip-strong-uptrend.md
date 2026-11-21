---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend.b1_breakdown-rebound-more-coins
line: 7.d not profitable
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend.b1_breakdown-rebound-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes below the lowest low of a coin's preceding two-day stretch while the coin's 30-day return is positive, the coin rises over the next three days. The larger that 30-day return is against the coin's typical 30-day move, and the sharper its fall over the past day, the larger the rise.
Consequence: Concentrate the rebound buys on sharp drops in strongly trending coins, where the rebound is largest, and leave weakly rising coins with mild breaks, which keep sliding.
Why:
- F1: The two failing measures sit together: the mean daily return is 0.00028 against the 0.0005 asked, and the Calmar is 0.48 against 0.75. The deepest fall is 20.5 %, running 308 days from w1 to w3. In those windows both the book (mean daily -0.00066, -0.00042, -0.00041) and the coins (-0.0028, -0.0034, -0.0017) lost, and the windows' own falls reached 8 %, 14 % and 21 %.
- F2: The rebound depends on the coin actually rising around the case. Cases in windows where the coins' 18-bar mean was negative lost -1.51 % of unusual move (-1.06 % total, 639 cases). Cases in the other windows gained +1.62 % (+2.09 % total, 1349 cases). This split is not known at a bar's close, so it explains the falls but cannot be traded directly.
- F3: The sharpness of the coin's past-day fall, against its 30-day typical 4h move, separates the cases much more strongly than the range width does.
- F6: Weakly rising coins with a mild or middling break lose money.
