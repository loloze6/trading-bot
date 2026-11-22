---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only
line: 7.b inconclusive
backtest: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just fallen in an unbroken streak of four-hour periods, and the volume across the streak has been declining, it rises over the next three days, only when the streak's loss is several times the coin's typical four-hour move over the past 30 days. Here the loss is counted directly in that typical move, not against the sizes of the coin's other recent streaks. Beyond that, the larger the loss relative to that typical move, the larger the rise.
Consequence: A trader buys only the rare fading-volume down-streaks that are several typical moves deep, expecting a rebound of a few percent over three days that clears trading costs many times over, and refuses the common shallow ones.
Why:
- F1: The test's bets mostly missed the idea's situation. Their median down-streak loss is 1.57 of the coin's mean absolute 4h move over 30 days, only 9.9 % of the 6,727 fading-volume bets exceed 4 such moves and only 3.1 % exceed 6. The bet forecast also sits at its cap of 20 in forecast quintiles 2 to 4, so the "several times" condition and the grading never act, and the bets' mean excess 18-bar return is +0.013 % (t 0.10, 4,331 cases).
- F2: Recomputed on the bars, the idea's own situation shows a large move. Fading-volume down-streaks whose loss exceeds 4 usual 4h moves are followed by an 18-bar excess return of +2.15 % (t 6.16, 846 cases, one per grid cell), a strength of 0.26 of the usual move. That is about 11 times the 0.19 % cost of a trade, against 0.1 times for the test's bets.
- F3: The rise is graded by the relative loss. By loss band it is +1.48 % (t 3.21) at 4–5 usual moves, +1.45 % (t 2.55) at 5–6, +3.77 % (t 3.60) at 6–8 and +3.45 % (t 3.26) above 10. The slope is +0.34 % per usual move (t 2.06, 846 cases), while ordinary fading streaks of at most 2 moves are followed by −0.35 % (t −2.54, 3,313 cases).
- F4: Fading volume adds to the rebound, as the brief claims. At losses of 6–8 usual moves, fading streaks give +2.83 % over 18 bars (t 3.08, 229 cases) against +0.04 % (t 0.10, 569 cases) when volume did not fade. Above 8 moves the figures are +1.95 % (t 2.52, 114 cases) against +0.45 % (t 0.89, 395 cases).
- F5: Above 6 usual moves the rebound is positive in all six coins, from +1.34 % in LTC to +6.88 % in ZEC, and in every year but one. It is strong in 2019, 2020, 2021 and 2025 (+5.0 % to +7.0 %) and weak in 2018, 2022 and 2023 (+0.9 % to +1.1 %, t below 1); 2024 is +0.41 % (strength −0.007, t 0.26).
- F7: The test's mostly ordinary bets just follow the market's year. Their mean excess 18-bar return swings from −1.56 % in 2018 (t −3.63) and −1.16 % in 2022 (t −3.52) to +1.48 % in 2021 (t 3.36). That is why their overall mean nets to near zero.
