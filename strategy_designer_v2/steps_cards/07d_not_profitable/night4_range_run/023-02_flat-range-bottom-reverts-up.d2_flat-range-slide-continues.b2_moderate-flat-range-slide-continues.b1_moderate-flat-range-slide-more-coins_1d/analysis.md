---
line: 7.d not profitable
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues.b1_moderate-flat-range-slide-more-coins_1d
idea tested: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues.b1_moderate-flat-range-slide-more-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4592 USD
---
## Findings
- **F1:** Each case's move does not pay for a trade. Over 5 days the unusual move is +0.55 % per case, but the coin's normal drift against the short is -0.79 %, so the total move is -0.24 % against a cost of 0.22 %. On the 928 grid cases the short's total move is +0.21 % (t 0.62), and the book's mean daily return is -0.0078 %, of which the market's own rise accounts for -0.0146 % a day.
- **F2:** The book holds the short long after the signal has gone. 65 % of short bars have a forecast of 0, and they lose -0.036 % per bar, while short bars with a negative forecast gain +0.011 %. Trades last 8.2 days on average, and the 249 trades held over 20 days lose -25.1 % gross on average (median +3.8 %).
- **F3:** The effect is absent where the book is largest. In the narrowest quarter of 30-day range width (high-low over close), the unusual move is -0.47 % (strength -0.05) with a total move of -1.23 % (t -2.58, 167 cases), and the short there averages an allocation of -0.43. In the three wider quarters the unusual move is +1.8 % to +2.1 % (strength 0.13 to 0.18) with a total move of +1.1 % to +1.3 %.
- **F4:** Volatility grades the move the same way. In the calmest quarter of 20-day volatility the unusual move is +0.01 % (total -0.73 %, t -1.55, 192 cases). In the third quarter it is +3.0 % (total +2.2 %, t 2.97, 191 cases).
- **F5:** The total move turns positive when the coin's 60-day return is weakest. In the lowest quarter of 60-day return the unusual move is +2.9 % and the total move +2.0 % (t 2.29, 107 cases).
- **F6:** The edge has faded over time. The unusual move is +1.3 % to +3.0 % per case in each year from 2018 to 2022, then -0.53 % in 2023, -0.28 % in 2024 and +0.33 % in 2025 (470 cases together), and the total move in 2023 is -1.26 % (t -2.69).

## Ideas
- `023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues.b1_moderate-flat-range-slide-more-coins.d1_wide-range-flat-slide-continues` (from F1, F3, F4): In a coin whose 30-day net move has been small relative to its 30-day high-low range and whose close sits below the middle of that range, the more its 10-day return is negative, the more it falls over the next 5 days, only while that fall is moderate rather than extreme against its own recent 10-day moves, and the wider that 30-day high-low range is against its close, the larger that fall.
- `023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues.b1_moderate-flat-range-slide-more-coins.d2_flat-slide-in-falling-coin` (from F1, F5): In a coin whose 30-day net move has been small relative to its 30-day high-low range and whose close sits below the middle of that range, the more its 10-day return is negative, the more it falls over the next 5 days, only while that fall is moderate rather than extreme against its own recent 10-day moves, and the more negative its 60-day return, the larger that fall.
- `023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues.b1_moderate-flat-range-slide-more-coins.d3_flat-slide-fades-after-days` (from F2, F1): In a coin whose 30-day net move has been small relative to its 30-day high-low range and whose close sits below the middle of that range, the more its 10-day return is negative, the more it falls, and that fall shows within the next 5 days and is gone after them.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
