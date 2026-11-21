---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins
line: 7.d not profitable
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 10 days, and the more such past turning-up lows lie just above the close, the larger the fall, only while the coin has not already lost a large share of its value over the past 90 days.
Consequence: A close under a support that held several times is a reason to be short for about ten days, unless the coin has just collapsed, when the short should be refused.
Why:
- F1: The book fails mainly because it is short against coins that rise. It is short on 77 % of bars, with a mean position of -0.46. The position held times the coins' mean daily return costs it -0.066 % a day. Its timing adds back about +0.025 % a day, so the book loses -0.040 % a day overall. The coins' drift sinks 18 of 19 coins (DOGE -0.22 %/day, TRX -0.12 %/day).
- F2: The forecast separates cases, but on its active side the coin still rises before costs. Over 5 days the active grid cases (n 4943) return +0.41 %, against +1.53 % when flat (n 2185). That makes the unusual move a short gains -0.34 %, while the total move a short earns is negative (-0.46 % per case against a 0.22 % round trip).
- F3: Active cases where the coin is already down hard rebound and carry the short's loss. In the deepest quarter of the 90-day return (mean -51 %, n 282), active cases rise +1.92 % over 5 days (excess +1.15 %, strength -0.10). In the other three quarters they fall -0.73 % to -1.05 % (strength 0.11 to 0.13), which is 3 to 5 times the cost.
- F5: Outside the deep-fall quarter, the move grows with the horizon much faster than the cost. Active cases' raw return goes from -0.7 to -1.05 % at 5 days, to -2.5 to -2.7 % at 10 days, to -1.5 to -6.2 % at 20 days (n 36 to 37 per quarter). Strength rises from 0.13 to 0.21 to 0.30 in the middle quarters, and pooled strength from 0.024 at 5 days to 0.045 at 10 days.
- F6: The grading by the forecast holds only after a 90-day decline. Where the 90-day return is negative, the slope t is 2.18 at 5 days (n 820) and 2.95 at 20 days (n 97). Where it is positive, the slope t is -0.62 (n 306), although those cases still fall -0.69 % over 5 days.
