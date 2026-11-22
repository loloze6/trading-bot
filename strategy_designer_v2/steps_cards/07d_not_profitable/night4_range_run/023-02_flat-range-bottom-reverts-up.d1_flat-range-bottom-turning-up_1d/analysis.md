---
line: 7.d not profitable
backtest: 023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up_1d
idea tested: 023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3715 USD
---
## Findings
- **F1:** The book earns 0.0088 % a day against the 0.05 % required, because it is rarely in the market: the mean_reversion regime covers 18.5 % of bars, each coin holds a position on 16 % to 30 % of bars, the mean allocation while in is 0.14 to 0.31, and over 2898 days only 71 % of days show any book move.
- **F2:** Within that small exposure most of the gain is the coins' own rise: per coin the book's mean bar gain is 0.0013 % to 0.019 %, the market part is 0.003 % to 0.007 %, and timing is near zero or negative (BTC 0.0016 %, XRP 0.0007 %, LTC −0.0015 %), with only XMR (0.014 %) and ZEC (0.008 %) adding clearly.
- **F3:** The tested forecast does not grade the next 5 days. On 168 independent grid cases its unusual move is 0.81 % (t 1.02), strength 0.083, and the slope's t is 1.20. Its quartiles are U-shaped rather than rising: drift-removed 5-day returns are +2.78 %, −0.66 %, −0.94 % and +2.07 % from weakest to strongest.
- **F4:** Trade costs are not the cause. The 604 trades gross 2.41 % and net 2.31 % (about 9 days each, 61 % winners), and the cases' total 5-day move of 1.41 % is about seven times the 0.19 % cost of a trade.
- **F5:** The falls come from a few large losing trades, not from fees. The worst trade lost 58.2 % and one trade in ten lost more than 9.3 %. The 20 worst book days average −1.42 %, carried mostly by XMR (−0.44 %) and ZEC (−0.35 %). The deepest fall is −8.3 % (w24), against a Calmar of 0.37.
- **F6:** In flat coins below the middle, only the strongest turns carry the effect. By 10-day-return quintile the drift-removed 5-day returns are +0.25 %, −2.53 %, −0.40 %, −0.00 % and +1.95 % (strength 0.20 for the top quintile, mean 10-day rise +7.8 %), giving a slope t of 2.41 on 467 cases.
- **F7:** The brief's reversion toward the middle is not in flat coins. The reversion toward the middle is +0.13 % (t 0.33, n 511) in the flattest net-move quintile, and the 5-day excess return regressed on range position in flat coins has t −0.42 (n 835). Coins of middling trend (net/range about 0.44) move away from the middle (−1.28 %, t −2.87).
- **F8:** In trending coins the 10-day move grades the next 5 days strongly, in two opposite ways. Above the middle, a larger 10-day rise is followed by a larger 5-day rise (slope t 4.17, n 879, mean excess +0.83 %). Below the middle, a larger 10-day fall is followed by a larger 5-day rise (slope t −3.52, n 841).
- **F9:** Within flat coins below the middle, closes nearest the middle do best. By range-position quartile the drift-removed 5-day returns are +0.18 %, −1.43 %, −0.25 % and +0.94 % from deepest to nearest the middle (strength 0.10 for the nearest).

## Ideas
- `023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up.d1_flat-range-turn-nearing-middle` (from F3, F6, F9): In a coin whose 30-day net move has been small relative to its 30-day high-low range and whose close sits below the middle of that range, the larger its rise over the past 10 days and the closer that rise has carried its close back to the middle, the more it rises over the next 5 days.
- `023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up.d2_trending-top-momentum-continues` (from F1, F2, F8): In a coin whose 30-day net move is large relative to its 30-day high-low range and whose close sits above the middle of that range, the larger its rise over the past 10 days, the more it rises over the next 5 days.
- `023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up.d3_trending-bottom-sharp-fall-rebound` (from F1, F7, F8): In a coin whose 30-day net move is large relative to its 30-day high-low range and whose close sits below the middle of that range, the larger its fall over the past 10 days, the more it rises over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
