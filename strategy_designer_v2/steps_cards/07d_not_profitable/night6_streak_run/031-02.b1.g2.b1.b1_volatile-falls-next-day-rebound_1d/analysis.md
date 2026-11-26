---
line: 7.d confirmed, not profitable
backtest: 031-02.b1.g2.b1.b1_volatile-falls-next-day-rebound_1d
idea tested: 031-02.b1.g2.b1.b1_volatile-falls-next-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6637 USD
---
## Findings
- **F1:** The book failed only on Calmar (0.43 against 0.75), and its deepest fall was one stretch in w16 (2020): 19 days, the book down 40.1 % while holding the coins fell 55.6 %. In that window the book's position averaged 0.26, and its coins' 60-day return averaged −17 %.
- **F2:** Inside w16 the strong case still paid: deep falls (≤ −3 %) while 20-day volatility was above 60-day volatility were followed by +1.62 % next day (98 cases). The losses came from the other signal bars: deep falls with falling volatility gave −1.95 % (56 cases), and shallow down days with rising volatility gave −1.49 % (208 cases).
- **F3:** On signal bars the next-day excess return grows with the ratio of 20-day to 60-day volatility, from −0.38 % (t −3.85, 2426 cases) in the lowest fifth to +0.52 % (t 4.50, 2426 cases) in the highest. Taken alone, with no signal, the same highest fifth earns −0.08 % (t −0.69, 2679 cases), so the ratio is no effect of its own.
- **F4:** Deep falls (≤ −3 %) with the volatility ratio at or above 1 give +0.64 % excess next day (t 5.11, 2381 cases). Deep falls with a falling ratio give +0.08 % (t 0.75, 2554 cases). Rising volatility without a deep fall gives −0.01 % (t −0.24, 8316 cases).
- **F5:** The idea's measured size is a total move of +0.20 % per case against a cost of 0.22 % per trade. Only the strong end of the signal clears that cost:
- **F6:** Trading only the bars where the fall is at least 3 % and the volatility ratio is at least 1 changes the failing measure:
- **F7:** Trading only on the volatility ratio at or above 1 lifts Calmar to 0.56 (deepest fall −29.4 %, Sharpe 0.88).
- **F8:** Adding to that condition a close far from its 50-day mean on either side (≤ −16.7 % or ≥ +0.6 %) lifts Calmar to 0.90, with the deepest fall at −19.2 % and Sharpe 1.10.

## Ideas
- `031-02.b1.g2.b1.b1.d1_volatile-falls-rising-turbulence-rebound` (from F2, F3, F4, F6, F7): The larger a coin's percentage fall on its latest day, the more it rises over the next 1 day, and this rebound is larger the higher the coin's volatility over the past 60 days and the more its 20-day volatility exceeds its 60-day volatility.
- `031-02.b1.g2.b1.b1.d2_deepest-volatile-falls-rebound` (from F1, F5, F6): The larger a coin's percentage fall on its latest day, the more it rises over the next 1 day, larger the higher its 60-day volatility, with the rebound concentrated in the deepest falls, so that the next-day rise grows faster than in proportion to the day's fall.
- `031-02.b1.g2.b1.b1.d3_stretched-turbulent-falls-rebound` (from F3, F4, F8): The larger a coin's percentage fall on its latest day while its 20-day volatility exceeds its 60-day volatility, the more it rises over the next 1 day, and this rebound is larger the farther the coin's close sits from its 50-day average.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
