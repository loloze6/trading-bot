---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-two-day-rebound
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-two-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over the 24 hours up to the 20:00 UTC close, the more it rises over the next 2 days, only while its close is above its 30-day mean price.
Consequence: An evening dip inside a coin's monthly uptrend is worth buying for two days, while one below the monthly mean is not.
Why:
- F1: The book's failure is a size problem: per case over 48 hours the unusual move is +0.10 % against a 0.19 % round trip (0.5 times), so most of what the book earns is the coin's drift (+0.27 % of the +0.37 % total). It sits in a position 73 % of the bars at a mean allocation of 0.55, and it trails holding in the bull years (2020 book 0.0013 against coin 0.0042 a day, 2021 0.0011 against 0.0041, 2024 0.0007 against 0.0024). That is where its Sharpe falls short of holding's (-0.12) and where its mean daily return falls short of the bar (0.00044).
- F4: The turbulent-fall rebound mostly holds across years. In the top turbulence tercile the 48-hour excess is positive in 7 of 8 years (+0.50 % to +1.62 %), the exception being 2022 at -1.19 %. In the bottom tercile it is negative in 5 of 8 years, including 2018 at -2.08 % (t -3.56) and 2025 at -1.37 % (t -2.73). These calm-fall losses come in the bear periods that lie under the book's deepest fall (53 %, Calmar 0.18).
- F7: Evening falls that come while the coin is above its 30-day mean rebound and those below it do not. The excess is +0.34 % over 48 hours above the mean (t 2.02, n 1601) and -0.13 % below it (t -0.86, n 2395).
