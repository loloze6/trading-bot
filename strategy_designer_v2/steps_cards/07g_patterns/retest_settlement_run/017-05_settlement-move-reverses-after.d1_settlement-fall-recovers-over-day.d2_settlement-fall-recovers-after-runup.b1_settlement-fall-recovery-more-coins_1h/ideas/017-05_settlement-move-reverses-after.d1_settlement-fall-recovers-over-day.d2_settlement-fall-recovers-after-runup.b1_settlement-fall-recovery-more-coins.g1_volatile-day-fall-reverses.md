---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours, a coin rises after falling over the past 24 hours, by more the larger that fall is against its usual 24-hour move. The rise is larger the higher the coin's hourly volatility over the past 7 days.
Consequence: A sharp day-long fall in a volatile coin is a reason to be long for the next day, sized by the fall and the volatility. The same fall in a calm coin is not.
Why:
- F1: On a non-overlapping daily grid over all coins and windows, a coin's 24-hour return, counted in its usual 24-hour moves, correlates −0.067 with its excess return over the next 24 hours (t −12.7, 35 122 cases). The reversal sits in the coin's most volatile third of its 7-day hourly volatility: corr −0.125 (t −13.6), and among falls alone corr −0.161 (t −12.4), with a mean next-day excess of +0.115 usual moves. In the calmest third, falls have −0.042 usual moves and corr +0.027.
- F2: This day-long reversal is broad and has weakened over time. Ten coins show it with t below −3.5: XMR −6.8, ETH −5.5, TRX −5.0, BTC −4.6, LTC −4.5, ADA −3.9, ZEC −3.8, UNI −3.7, LINK −3.5, XRP −3.5. Among falls in the volatile third, corr is −0.227 (t −12.6, 2 931 cases) in 2018–2021 and −0.043 (t −2.3, 2 881 cases) in 2022–2025. It is near zero on AVAX, INJ, NEAR, SOL, DOGE and TAO.
- F4: The tested signal is not tied to the funding clock. At closes of 00:00 and 16:00 UTC its next-day excess has t 0.57 and 2.67. At non-settlement closes it is as strong or stronger: 01:00 at t 5.0, 02:00 at t 4.9, 15:00 at t 3.7, 12:00 at t 3.3. This is the brief's own third falsifier, and the tested gain looks like the general reversal in F1.
- F7: Size against cost. A fall in the volatile third earns +0.115 of a usual 24-hour move (about 5.5 %), which is about 0.6 % per case, near 2.9 times the 0.22 % cost of a trade. The tested idea's strength was 0.024 (an unusual move of 0.6 times the cost).
