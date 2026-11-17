---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin whose last day's move was large relative to its 20-day volatility moves the opposite way over the next 1 day, and the reversal is larger the larger that scaled move and the higher the coin's 20-day volatility stands against its own history.
Consequence: After a violent day in a turbulent market, fade it for one day whatever the weekday; in a calm market, do not.
Why:
- F1: Across all days, the next day's excess return falls with the day's own volatility-scaled move only when volatility is high: in the top volatility tercile the slope is -0.00709 (t -8.05, n 5075), in the middle tercile it is -0.00045 (t -0.72), and in the bottom tercile it is +0.00115 (t 2.36), so the day-ahead reversal is a high-volatility effect, not a weekend one.
- F2: The Sunday 3-day reversal the idea tested follows the same volatility grading: the slope of the Sunday-to-Wednesday excess return on Sunday's scaled move is -0.00085 (t -0.30, n 708) in the low-volatility tercile, -0.00779 (t -2.18, n 707) in the middle tercile and -0.01502 (t -3.23, n 708) in the high-volatility tercile, while weekend volume adds nothing (z×volume-ratio t 0.89).
- F3: The 1-day reversal is not limited to the weekend; its slope is about as negative after Tuesday (t -3.32), Wednesday (t -3.35) and Saturday (t -4.65) bars as after Sunday bars (t -3.21), which contradicts the brief's claim that weekend moves reverse more.
