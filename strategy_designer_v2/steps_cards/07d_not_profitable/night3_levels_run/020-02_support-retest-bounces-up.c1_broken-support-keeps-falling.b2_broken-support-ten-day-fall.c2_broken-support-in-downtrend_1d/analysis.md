---
line: 7.d not profitable
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c2_broken-support-in-downtrend_1d
idea tested: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c2_broken-support-in-downtrend
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3610 USD
---
## Findings
- **F1:** The book loses because it is short against coins that rise. It is short on 61 % of days, while the coins drift up by 0.07 to 0.16 % a day. Its gain from the market's own rise is negative on every coin (-0.030 to -0.065 % a day). Its timing (+0.004 to +0.069 % a day on 5 of 6 coins, -0.026 on XRP) does not cover that, so the book earns -0.029 % a day. Per case, the unusual move (+0.58 %, 3.0 times the 0.19 % cost of a trade) is outweighed by the 10-day drift against the short (-1.19 %), which leaves a total move of -0.61 %.
- **F2:** The forecast's size grades the outcome, and its weak end loses. By |forecast| quartile, the 10-day short-direction total move per case is -2.10 %, -0.45 %, -0.24 % and +1.43 % (809 cases). Per short bar, the daily gain is -0.155 % at |forecast| 0 to 5 (1540 bars), +0.067 % at 5 to 10, +0.167 % at 10 to 15 and +0.243 % at 15 to 21 (1166 bars).
- **F3:** The book keeps its shorts well past the idea's horizon, and those days lose. Trades last 19.0 days on average against a 10-day horizon. The 989 short bars held after the forecast returned to 0 lose -0.217 % a day. The 2482 short trades average -2.99 % after fees.
- **F4:** Shorts after a sharp 10-day move lose in both directions. After a 10-day fall of more than 10 %, the total move is -2.26 % (t -1.93, 118 cases, smaller-forecast half) and -1.41 % (83 cases, larger half). After a 10-day rise of more than 5 %, it is -2.74 % (t -2.10, 76 cases) and -2.10 % (77 cases). After a flat 10 days, the larger-forecast half earns +1.46 % (t 1.67, 204 cases). Inside a deep 60-day decline (below -30 %), a 10-day rise of more than 5 % is followed by -8.51 % for the short (t -2.97, 23 cases).
- **F5:** The effect lives in mild 60-day declines. With a 60-day return between -15 % and 0, the larger-forecast half earns +2.90 % per case (t 1.99, 78 cases). In the top quartile of 60-day return (mean -5.8 %), the excess move is +3.74 % per case, against +0.95 %, -0.13 % and +0.51 % in the three deeper quartiles. The mild-decline, flat-10-day cell earns +2.78 % (t 1.96, 78 cases).
- **F6:** The result is spread thin across periods: only 8 of 24 windows have a positive Sharpe (from 0.25 to 1.83), and the other 16 run from -0.10 to -2.00.

## Ideas
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c2_broken-support-in-downtrend.d1_broken-support-in-shallow-downtrend` (from F1, F2, F4, F5): When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 10 days, and the more such past turning-up lows lie just above the close, the larger the fall, only while its 60-day return is negative. The fall is larger the closer that 60-day return is to zero and the smaller the coin's move over the past 10 days.
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c2_broken-support-in-downtrend.d2_strong-support-cluster-only` (from F1, F2, F3): When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 10 days, and the more such past turning-up lows lie just above the close, the larger the fall, only while its 60-day return is negative. The fall is larger the more lows cluster there and the nearer the close sits under them, by enough that the strongest clusters outweigh the coin's usual 10-day rise.
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c2_broken-support-in-downtrend.d3_rebound-in-deep-decline-continues` (from F4): When a coin whose 60-day return is deeply negative has risen sharply over its past 10 days, it tends to keep rising over the next 10 days, and the larger that 10-day rise, the larger the further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
