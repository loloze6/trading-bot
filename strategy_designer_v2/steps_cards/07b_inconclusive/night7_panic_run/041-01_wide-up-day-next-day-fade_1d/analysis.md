---
line: 7.b inconclusive
backtest: 041-01_wide-up-day-next-day-fade_1d
idea tested: 041-01_wide-up-day-next-day-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3473 USD
---
## Findings
- **F1:** On the down side the brief also names, the effect is clear and graded at the widest ranges. After down-closing days in folds B and C, the next day's long-side unusual move rises from +0.12 % (t 0.43, 715 cases) in the narrowest range-in-swing quintile to +1.21 % (t 2.58, 234 days) in the widest. The top quintile beats the bottom by 1.09 %, and the slope on range is +0.0044 per swing unit, with a correlation of 0.087 over 3574 cases.
- **F2:** The widest-range down days rebound in every year and on every coin. By year they gain +0.55 % to +1.58 % (2018 to 2021, t 0.68 to 1.66). By coin they gain +0.84 % (BTC, t 1.89) to +1.61 % (XMR, t 3.17), with ETH at t 2.27. So the effect is not carried by one period or one coin.
- **F3:** On the tested up side, the move is on the predicted side but not graded. All up days fade by +0.28 % (t 1.76, 3668 cases, 894 days), against step 5's +0.15 % (t 1.69). By range quintile the move is a hump: −0.04 %, +0.37 %, +0.58 % (t 2.64), +0.13 %, +0.37 %. By forecast third it is also a hump: +0.14 %, +0.55 % (t 2.87), +0.14 %. This is why the supporting check failed (−0.07 %).
- **F4:** The up-side fade is mixed across periods and regimes. By year it goes from +1.07 % (2018, t 2.59) down to −0.16 % (2021, t −0.51). It is positive in falling (+0.58 %, t 1.77) and choppy (+0.61 %, t 1.88) 60-day trends, but reverses in rising ones (−0.36 %, t −1.27). Even outside rising markets it is not graded: by range tercile it is −0.10 %, +1.20 % (t 3.26), +0.67 %.
- **F5:** The up-side move per case is too small for the costs. Its total move of +0.12 % is 0.6 times the 0.19 % cost of a trade, so the book loses: Sharpe −0.59, −16 % a year. On the down side, the widest-range quintile moves about 1.2 % per case, several times that cost.
- **F6:** Within the largest down-day returns, a wider range still adds to the rebound. In the top tercile of down-day returns in swing units, the widest-range tercile gains +1.01 % (t 2.48, 878 cases), against +0.32 % (t 0.84) for the middle range tercile. So the range carries part of the effect beyond the size of the close-to-close return.

## Ideas
- `041-01.b1_wide-up-day-fade-all-coins` (from F3, F4): After an up-closing day, a coin falls over the next day, more so the wider that day's high-to-low range in units of its 30-day daily-return swing.
- `041-01.b2_wide-down-day-next-day-rebound` (from F1, F2, F5, F6): After a down-closing day, a coin rises over the next day, more so the wider that day's high-to-low range in units of its 30-day daily-return swing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
