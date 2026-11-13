---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-08_twenty-day-momentum
line: 7.d not profitable
backtest: N1-08_twenty-day-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin's daily bars, a positive 60-day return is followed by daily returns that stay above the coin's average for several weeks, so the gain lives in the slow trend rather than in the 20-day swings.
Consequence: A trader keeps a long position through the slow trend and ignores short-term reversals of the 20-day move, which cuts the many short, losing trades.
Why:
- F2: The size of the forecast earns nothing: the pooled non-overlapping slope has t 0.06 (n 827), the bottom forecast fifth has a higher forward 20-bar excess return (+4.0%) than the top fifth (+2.3%) with the middle fifths negative (−1.7% to −2.6%), and trade gain by entry |forecast| quartile is flat (1.79%, 2.18%, 1.33%, 2.40%).
- F3: The book churns on the fast part of the signal: the forecast changes sign 1.87 times per 20 bars, trades held up to 7 days lose about 3% each before fees (n 5,987 trades), and only trades held over 20 days pay (+31.9% mean, n 1,131); flip days average −4.7 bp of book return against +23.8 bp on other days (805 vs 7,935 days).
- F4: Fees are not the cause: total commission (about 2,403 percentage points) is small next to the long side's gross 21,229, so the shortfall comes from the short side and from short trades.
- F5: Almost all the book's daily gain comes from being long while the 60-day return is positive: +53.3 bp per day (t 4.02, n 3,040 days), against +9.2 bp for long in a 60-day decline, +7.1 bp for short in a 60-day rise and +0.2 bp for short in a 60-day decline (all t < 0.8).
