---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over the 24 hours up to the 20:00 UTC close, the more it rises over the next 24 hours, only while its hourly volatility over those 24 hours is high relative to its hourly volatility over the past 30 days.
Consequence: An evening long after a deep daily fall is worth taking only after a turbulent, burst-like day; after a quiet slide it pays fees and rides the market's falls without a rebound to show for it.
Why:
- F1: The book makes 0.000368 a day against 0.001179 for holding the coins, with a Sharpe of 0.50 against 0.55. Its deepest fall is -54%, a 463-day episode across w12–w16 that summed -0.69 while the coins summed -0.81. On the coins' worst fifth of days the book still loses -0.0114, so it is long into the coins' falls.
- F2: Across 6,958 trades the mean is -0.60% before fees and -0.70% after them, with 0.43% of commission per trade and 49% winners. The trades that carry no edge are paying fees.
- F4: The rebound appears only when the past 24 hours were turbulent compared with the past 30 days. In each coin's top quartile of 24h-to-720h hourly volatility, the long bars earn 0.0049 of next-24h excess (t 3.60, n 1,620), against -0.0021, -0.0006 and -0.0009 in the other three quartiles. Yet the book holds 0.34–0.48 of allocation in those losing quartiles.
- F5: Inside the high-turbulence half (above each coin's median volatility ratio), the excess return rises with the vol-scaled fall: slope t 3.89, n 3,236, mean excess 0.0020. In the calm half the slope is t -0.80 (n 3,240) with a mean excess of -0.0013. The graded effect exists only in the turbulent state.
- F6: The coins' long-term level of volatility does not separate wins from losses. Across quartiles of 720h volatility the mean excess runs 0.0011, -0.0008, 0.0002 and 0.0009, with no clean ordering. What matters is the recent burst relative to the coin's normal, not high volatility as such.
