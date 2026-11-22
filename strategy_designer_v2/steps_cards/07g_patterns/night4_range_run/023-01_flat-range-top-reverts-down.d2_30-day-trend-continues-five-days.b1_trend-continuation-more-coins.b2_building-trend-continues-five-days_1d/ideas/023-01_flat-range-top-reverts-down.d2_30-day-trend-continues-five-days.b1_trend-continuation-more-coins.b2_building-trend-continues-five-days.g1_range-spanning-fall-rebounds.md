---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b2_building-trend-continues-five-days
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b2_building-trend-continues-five-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's 30-day fall has carried it, and the closer that fall comes to spanning its whole 30-day high-low range, the more the coin rises over the next 5 days.
Consequence: A trader would refuse to short a coin after a deep fall that spans its monthly range, and would lean long it for the following 5 days instead.
Why:
- F1: Coins after the deepest 30-day falls rebound instead of continuing down. In the bottom twentieth of 30-day returns (falls of 35 % to 43 %, mean −42.6 %), the next 5 days' drift-excess return was +2.78 % (median +1.03 %, 55 % positive, t 3.15, 272 non-overlapping cases). The next tenth was −2.5 % worse (Welch t 3.53), and 16 of the 19 coins had a positive mean in that bottom twentieth.
- F2: Among 30-day falls, the rebound grows as the fall covers more of the 30-day high-low range. The next 5 days' excess was −1.01 % at share 0.6–0.8 (t −2.20, n 584), +1.29 % at 0.8–0.9 (t 1.16, n 117) and +9.06 % at 0.9–1.0 (t 2.97, n 32). The book's shorts at share 0.8–1.0 lost −1.12 % per 5-day cell (t −2.43, n 151).
- F3: The coins that had fallen most from their 30-day high also rebounded. In the deepest tenth of drawdowns, the next 5 days' excess was +1.19 % (t 2.12, n 544), against −1.07 % to −1.96 % in the next four tenths (t −2.2 to −4.0).
