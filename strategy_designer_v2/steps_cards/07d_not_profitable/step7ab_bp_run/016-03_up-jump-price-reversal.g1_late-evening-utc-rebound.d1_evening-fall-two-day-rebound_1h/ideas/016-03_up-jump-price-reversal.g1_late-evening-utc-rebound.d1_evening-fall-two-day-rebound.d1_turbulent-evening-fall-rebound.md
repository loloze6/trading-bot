---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-two-day-rebound
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-two-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over the 24 hours up to the 20:00 UTC close, the more it rises over the next 2 days, only while its hourly volatility over those 24 hours is high against its hourly volatility over the past 30 days; the higher that ratio, the larger the rebound.
Consequence: An evening long after a deep fall is worth taking when the day was unusually turbulent for the coin, and refused when the fall came on a calm day, where it tends to continue.
Why:
- F1: The book's failure is a size problem: per case over 48 hours the unusual move is +0.10 % against a 0.19 % round trip (0.5 times), so most of what the book earns is the coin's drift (+0.27 % of the +0.37 % total). It sits in a position 73 % of the bars at a mean allocation of 0.55, and it trails holding in the bull years (2020 book 0.0013 against coin 0.0042 a day, 2021 0.0011 against 0.0041, 2024 0.0007 against 0.0024). That is where its Sharpe falls short of holding's (-0.12) and where its mean daily return falls short of the bar (0.00044).
- F2: The rebound after an evening fall is graded by how turbulent the last 24 hours were against the last 30 days. Measured as 24-hour hourly volatility over 30-day hourly volatility, the 48-hour excess of fall evenings rises across the quintiles of this ratio: -0.62 % (t -2.49), -0.09 %, -0.12 %, +0.46 % (t 1.79), +0.67 % (t 2.38), with about 800 independent cases each.
- F3: Depth and turbulence together carry the idea. Deeper-than-median falls in the top turbulence tercile earn +0.95 % excess over 48 hours (t 3.42, n 800), strength 0.13, total move +1.22 %, which is 6.4 times the cost. The same deep falls in the bottom tercile lose -0.69 % (t -2.58, n 568), strength -0.10.
- F4: The turbulent-fall rebound mostly holds across years. In the top turbulence tercile the 48-hour excess is positive in 7 of 8 years (+0.50 % to +1.62 %), the exception being 2022 at -1.19 %. In the bottom tercile it is negative in 5 of 8 years, including 2018 at -2.08 % (t -3.56) and 2025 at -1.37 % (t -2.73). These calm-fall losses come in the bear periods that lie under the book's deepest fall (53 %, Calmar 0.18).
- F6: The idea's horizon is right; its move does not outlast 2 days. The fall evenings' excess is +0.22 % over 96 hours (t 0.94, n 2144) and -0.13 % over 168 hours (t -0.34, n 1158).
