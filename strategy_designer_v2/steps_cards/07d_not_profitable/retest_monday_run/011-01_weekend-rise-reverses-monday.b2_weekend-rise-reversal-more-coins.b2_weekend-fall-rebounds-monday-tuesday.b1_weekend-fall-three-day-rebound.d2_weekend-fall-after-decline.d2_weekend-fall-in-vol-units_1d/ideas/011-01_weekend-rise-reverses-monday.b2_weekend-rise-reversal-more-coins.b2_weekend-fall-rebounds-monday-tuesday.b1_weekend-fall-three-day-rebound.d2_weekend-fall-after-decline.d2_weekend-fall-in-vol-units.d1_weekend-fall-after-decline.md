---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d2_weekend-fall-in-vol-units
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d2_weekend-fall-in-vol-units_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 3 days (Monday to Wednesday), and the rise is larger the larger that fall is measured in units of the coin's usual daily move over its past 60 days, only while the coin's 20-day return is negative.
Consequence: Buy weekend falls in proportion to their size only in coins already down over 20 days, and stay out after weekend falls that interrupt a 20-day rise, which held the book's crash losses.
Why:
- F1: The Calmar fails because of one long fall: the book's chain reaches a deepest fall of −38.1 %, while it earns only +11.3 % a year. The fall opens in w3 (window minimum −35.3 %, book sum −21.5 %, worst days −15.6 % and −11.2 % against the coin's −18.7 % and −14.3 %). It is still not recovered through w9 (window minimum −38.1 %). From w11 to w24 no window falls deeper than −11 %.
- F3: The big-fall cases fill the worst trades. 14 of the 20 worst case results are falls above 2 usual moves, and 13 of the 20 lie in w3 and w9 (3-day returns down to −57 % at full allocation). The big falls lose in w1–w10 (excess −5.8 % with t −2.3 and −5.5 % with t −2.2). They gain only in w18–w24 (+3.3 %, t 2.2).
- F5: The rebound depends on the coin's prior 20 days. For Sunday falls in the two lower quartiles of the 20-day return (below about −2.3 %), the excess is +2.2 % (t 5.3) and +2.0 % (t 3.8). In the upper two quartiles it is +0.04 % (t 0.10) and +1.05 % (t 1.8). Big falls after a 20-day rise lose (−7.4 % and −1.7 %, 21 cases each), while big falls after a 20-day decline still gain +2.1 % (74 cases). The big falls average a 20-day return of −10.1 %, against +1.9 % for the others.
- F6: A falling 20 days is not an upward effect on its own. Sunday rises in the same two lower 20-day quartiles are followed by excess 3-day returns of −1.24 % (t −3.2) and −1.34 % (t −4.3), against +2.2 % and +2.0 % after Sunday falls. The gain comes from the weekend fall itself; a decline already under way only makes it a liquidity overshoot, as the brief's theory expects, rather than a break. The effect is large enough to trade: its total move is 6.1 times the 0.22 % cost of a trade.
