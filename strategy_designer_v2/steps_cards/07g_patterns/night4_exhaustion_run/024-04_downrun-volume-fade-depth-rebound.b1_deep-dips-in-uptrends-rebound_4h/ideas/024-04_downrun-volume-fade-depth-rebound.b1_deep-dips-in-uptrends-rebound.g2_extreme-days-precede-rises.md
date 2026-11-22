---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound
line: 7.g patterns
backtest: 024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The larger the coin's 1-day move in either direction, measured in its typical moves over the past 30 days, the more the coin rises over the next three days.
Consequence: A trader goes long after unusually large 1-day moves of either sign, sized by how extreme the move is, and stays out after ordinary days.
Why:
- F3: The 1-day return, in usual moves, has a U-shape against the next 3 days. Its lowest decile is followed by +1.26 % unusual (t 3.58, 515 cases) and its highest by +1.07 % (t 2.43, 515 cases). Deciles 2 to 8 are all negative, from −0.24 % to −0.69 %.
- F1: The rebound is concentrated in the deepest down streaks. With the coin's 30-day return positive, streaks of more than 5 usual moves are followed by +6.45 % unusual 18-bar moves (t 4.23, 47 cases) and streaks of 3–5 usual moves by +2.21 % (t 2.13, 89 cases), while streaks of 0–3 usual moves give between −0.20 % and +0.23 % (all |t| < 0.3). With the 30-day return not positive, the deepest streaks still give +1.84 % (t 1.78, 72 cases).
