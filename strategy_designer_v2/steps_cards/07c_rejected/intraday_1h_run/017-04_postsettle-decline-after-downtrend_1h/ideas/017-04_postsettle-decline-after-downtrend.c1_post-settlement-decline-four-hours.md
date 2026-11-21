---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-04_postsettle-decline-after-downtrend
line: 7.c rejected
backtest: 017-04_postsettle-decline-after-downtrend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin with a strong 3-day run down, the return over the 4 hours after each funding settlement time (00:00, 08:00 and 16:00 UTC) is negative, and the stronger the 3-day fall, the larger that post-settlement decline.
Consequence: A trader can short a falling coin across the settlement and hold it for four hours, which earns more per round trip than the 2-hour hold whose fees ate the gain.
Why:
- F1: The rejection comes from a sign error in the measure, not from the market: the per-event gain was taken as -(forecast/10) × excess return, which counts a short as winning when the coin rises. On the actual short position, the gross gain per active bar is positive at every settlement holding hour: +2.04 bp at the 01:00 close (t 2.57), +1.31 bp at 09:00 (t 2.08), +2.06 bp at 16:00 (t 2.45) and +2.42 bp at 17:00 (t 3.36), and the summed gross gain is +6.19.
- F2: After a 3-day fall, the coin did decline over the 2 hours after settlement, and the decline grows with the fall. The mean excess 2-bar return is -8.54 bp for a standardised 3-day change below -2 (n 3275), -5.14 bp for -2 to -1 (n 10399), -2.97 bp for -1 to -0.5 and -0.67 bp for -0.5 to 0. The step-5 supporting check agrees: largest third minus smallest third is -0.000988.
- F4: The post-settlement decline lasts beyond 2 hours and stays graded at 4 hours. At settlements the excess 4-bar return is -6.96 / -6.94 / -5.01 / -3.19 bp from the deepest to the mildest down bin. At other hours it is +5.22 / -0.38 / -1.76 / -2.15 bp. By 8 hours it is gone (+0.41 bp in the deepest bin).
- F5: Fees, not direction, sank the book. Total fees were 28.07 against a gross gain of 6.19, because every settlement brings an entry and an exit (about 0.71 per coin at the 00, 02, 08, 10, 16 and 18 closes). The result is a mean daily book return of -0.00124 and a Sharpe of -2.79.
- F6: The effect sits in falling markets and is spread across coins. The down-trend settlement excess 2-bar return is -16.7 bp in 2018 (t -4.04) and -11.4 bp in 2022 (t -5.04), but +3.0 bp in 2025 (t 1.18). By coin it is negative everywhere, from -2.1 bp for XMR to -7.7 bp for ETH (t -3.49).
