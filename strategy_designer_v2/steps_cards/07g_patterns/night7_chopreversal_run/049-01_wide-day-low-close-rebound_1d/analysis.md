---
line: 7.g patterns
backtest: 049-01_wide-day-low-close-rebound_1d
idea tested: 049-01_wide-day-low-close-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3928 USD
---
## Findings
- **F1:** The low-close rebound is real but small, and it is not exactly the brief's two-sided claim. On wide days (top width tercile), closes in the bottom fifth of the range were followed by a next-day excess return of +1.117 % (t 2.74, day-clustered, 569 bars). Closes in the top fifth of wide days were followed by only -0.146 % (t -0.41, 592 bars). On narrow days every close-location fifth sits between -0.43 % and -0.07 % (all |t| ≤ 1.21).
- **F2:** The effect lives in falling markets, not rising ones. The slope of next-day excess return on (0.5 − close location) × width multiple is 2.025 % in falling markets (t 1.83, 2,063 bars) and 1.509 % in choppy markets (t 1.75, 654 bars). In rising markets it is -0.049 % (t -0.09, 1,652 bars). Agitation separates it less: 0.634 % agitated (t 0.87) against 0.332 % calm (t 0.58).
- **F3:** The effect is broad across coins and years. The slope is positive for all six coins (t 2.6 to 4.5, except XRP at 0.309 %, t 0.71) and in every year 2018 to 2021 (t 2.8 to 4.8).
- **F4:** The signal is hard to tell apart from a plain large down day. Today's volatility-scaled return, bottom fifth, gives +0.703 % next day (t 2.38, 1,436 bars). In a joint regression, the close-location × width term keeps a coefficient of 0.998 % but its t falls to 1.65, and the scaled return's term goes to 0.029 % (t 0.13). The two carry the same one-day reversal.
- **F5:** The reversal is gone after one day. On the non-overlapping 3-day grid, the five signal fifths give excess returns from -0.144 % to +0.309 %, all with |t| < 0.5 (about 470 cases each). Holding longer does not enlarge the move against the 0.19 % trade cost.
- **F6:** The book mostly carries the coins' own moves rather than the timing. Its daily return correlates 0.805 with the coins' mean daily return; it averages +1.242 % on coin-up days and -1.162 % on coin-down days. Its top 5 % of days make 224 % of its total gain, its bottom 5 % take away 217 %. This explains the failed Calmar despite a confirmed signal.
- **F7:** The cell that runs against the brief does not stand out from chance. In agitated markets, narrow days closing in the upper half of their range were followed by -1.467 % (t -2.91, 198 bars). That is one of about 60 cells examined, so I do not count it as a finding.

## Ideas
- `049-01.g1_falling-market-wide-day-low-close-rebound` (from F2, F1, F3): In a falling market, the lower a coin closes in its day's high-low range, and the wider that day's range is against the coin's usual daily range over the past 30 days, the larger its rise over the next day.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `049-01.g2_scaled-one-day-fall-rebound` (from F4, F5): The larger a coin's fall over the day against its usual daily swing over the past 30 days, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
