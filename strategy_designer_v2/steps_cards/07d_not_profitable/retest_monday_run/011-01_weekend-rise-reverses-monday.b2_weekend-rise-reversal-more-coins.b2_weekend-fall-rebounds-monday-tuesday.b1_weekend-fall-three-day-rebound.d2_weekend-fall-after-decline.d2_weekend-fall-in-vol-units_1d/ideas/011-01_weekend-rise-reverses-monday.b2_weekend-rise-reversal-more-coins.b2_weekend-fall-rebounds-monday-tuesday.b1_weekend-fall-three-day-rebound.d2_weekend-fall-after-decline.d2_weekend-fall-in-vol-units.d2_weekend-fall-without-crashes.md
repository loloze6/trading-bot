---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d2_weekend-fall-in-vol-units
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d2_weekend-fall-in-vol-units_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 3 days (Monday to Wednesday), and the rise is larger the larger that fall is measured in units of the coin's usual daily move over its past 60 days, except when the fall is more than twice that usual daily move.
Consequence: Size weekend-fall buys by the fall up to two usual moves and leave out the crash-sized weekend falls that continue lower and carried the book's deepest fall.
Why:
- F1: The Calmar fails because of one long fall: the book's chain reaches a deepest fall of −38.1 %, while it earns only +11.3 % a year. The fall opens in w3 (window minimum −35.3 %, book sum −21.5 %, worst days −15.6 % and −11.2 % against the coin's −18.7 % and −14.3 %). It is still not recovered through w9 (window minimum −38.1 %). From w11 to w24 no window falls deeper than −11 %.
- F2: The book's losses come from the largest Sunday falls. Above 2 usual daily moves (143 cases), the excess 3-day return is +0.9 % (t 0.45), −2.3 % (t −1.26) and +0.1 % (t 0.06) across the three bands. Between 1 and 2 usual moves it is +2.3 % (t 4.2) and +4.0 % (t 4.4). The forecast is capped at 20, so these largest falls carry the largest position (allocation 0.87 to 1.01, against 0.36 to 0.61 for 0.5 to 1.5 moves). Their mean 3-day low is −11 % to −15 %, against about −6 % for smaller falls.
- F3: The big-fall cases fill the worst trades. 14 of the 20 worst case results are falls above 2 usual moves, and 13 of the 20 lie in w3 and w9 (3-day returns down to −57 % at full allocation). The big falls lose in w1–w10 (excess −5.8 % with t −2.3 and −5.5 % with t −2.2). They gain only in w18–w24 (+3.3 %, t 2.2).
- F4: Leaving out the falls above 2 usual moves keeps all the gain and cuts the risk. Summed case result: 12.82 against 12.79. Standard deviation per case: 0.036 against 0.046. Sum of the 20 worst cases: −2.71 against −4.76.
