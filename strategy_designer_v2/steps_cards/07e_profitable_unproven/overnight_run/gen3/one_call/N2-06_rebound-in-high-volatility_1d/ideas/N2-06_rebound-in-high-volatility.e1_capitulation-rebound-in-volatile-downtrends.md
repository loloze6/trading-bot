---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-06_rebound-in-high-volatility
line: 7.e profitable but not proven
backtest: N2-06_rebound-in-high-volatility_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20-day volatility sits in the upper half of its 100-day history and whose price is below its 50-day average, a one-day fall larger than about 1.5 of its recent daily sd is followed by a next-day rise that is large relative to that sd.
Consequence: A trader can buy the close of a sharp down day only when the coin is already volatile and in a decline, and pass on the same drop in quiet markets.
Why:
- F3: The book earns in the high-volatility state: P&L is 23.9 in "trending" (volp ≥ 0.5, 8,219 bars) against 5.9 in "unknown" (9,161 bars).
- F4: After a drop of at least 1.5 of the 60-day sd, the next day's rebound is larger in high-volatility bars than in quiet ones, but it is not more frequent: the vol-normalised next return is +0.31 sd (t = 4.75, n = 402) in high volatility against +0.03 sd (t = 0.37, n = 397) in quiet bars, while the up share is 65 % against 60 %, which matches the verdict's z = 0.10 on frequency.
- F5: The high-volatility rebound is strongest when the coin is already falling: drops with price below its 50-day average return +1.76 % next day (66.7 % up, t = 3.93, n = 255), and drops with negative 20-day momentum return +1.84 % (t = 4.13, n = 244); the same quiet below-50-day drops return +0.03 % (t = 0.11, n = 319), and high-volatility below-50-day big-position bars carry 14.4 of the 28.6 big-position P&L.
- F6: The high-volatility drop rebound is not one coin or one period: its mean next return is positive in all six coins (+0.9 % to +2.8 %, n = 56 to 72 each) and in all eight years, though it is weak in 2022 (t = 0.57, n = 34) and 2025 (t = 0.38, n = 45); 20 of 24 windows end positive.
