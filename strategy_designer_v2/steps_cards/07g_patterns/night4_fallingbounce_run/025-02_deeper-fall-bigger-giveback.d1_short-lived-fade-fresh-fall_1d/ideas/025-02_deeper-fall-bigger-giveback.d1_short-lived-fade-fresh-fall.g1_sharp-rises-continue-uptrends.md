---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall
line: 7.g patterns
backtest: 025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day return is positive, a one-day rise of several usual daily moves is followed by a further rise over the next 2 days, and the larger the one-day rise in usual daily moves, the larger the rise that follows.
Consequence: A trader would buy, not short, a sharp up-day in a coin that is rising over the past month, and would refuse to fade it.
Why:
- F1: In coins whose 30-day return is positive, a one-day rise of more than 2 usual daily moves is followed by a 2-day move of +1.77 % beyond the coin's drift (t 3.16, 173 non-overlapping cases) and a 5-day move of +4.74 % (t 2.37, 62 cases). This is about 9 times the 0.19 % cost of a trade. It is positive in all six coins (ETH +2.50 % t 2.84, LTC +2.51 % t 2.04, XRP +2.63 %, BTC +1.03 %, ZEC +0.99 %, XMR +0.60 %) and in both halves of the windows (w1–w12 +0.88 % t 1.53, w13–w24 +2.65 % t 2.78).
- F2: The continuation in F1 grows only weakly with the size of the rise. Over all rises above 0.3 usual moves in rising months, the Spearman correlation between the rise and the 2-day unusual move is 0.063 over 1344 cases (t about 2.3). The buckets are not monotone: 0.3–1 moves give −0.17 %, 1–1.5 give +0.50 %, 1.5–2 give −0.30 %, 2–3 give +1.92 % (t 2.87) and above 3 give +1.26 %.
- F5: Sharp rises are followed by opposite moves depending on the 30-day sign. Above 2 usual moves, the 2-day unusual move is −1.83 % (t −2.81, 78 cases) when the 30-day return is negative and +1.77 % (t 3.16, 173 cases) when it is positive. In the 5-day grid, rises of 1–2 moves give +0.89 % in falling months against +2.07 % (t 2.30) in rising months.
