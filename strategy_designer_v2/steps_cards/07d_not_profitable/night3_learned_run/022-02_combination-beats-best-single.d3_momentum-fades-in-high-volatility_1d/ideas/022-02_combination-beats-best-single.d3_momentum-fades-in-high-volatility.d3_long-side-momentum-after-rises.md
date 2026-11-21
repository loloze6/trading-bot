---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility
line: 7.d not profitable
backtest: 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 28-day return, the higher its return over the next 20 days, only while that 28-day return is above zero, the more so the larger the rise.
Consequence: A trader should keep the momentum bet on the long side after rises and stop shorting coins after their falls, since those shorts lost most of what the longs earned.
Why:
- F4: The book's short side destroys what its long side earns. Long bars summed +12.18 of gain before costs over 8198 bars, short bars -5.96 over 9124 bars. Short trades averaged -6.12 % net with 31 % winners (2146 trades), long trades +10.82 % net with 49 % winners (1506 trades).
- F6: The book trails holding because it is short in rising years. In 2020 it earned 0.00103 a day against the coins' 0.00423, in 2021 0.00014 against 0.00409, and in 2023 it lost 0.00169 while the coins gained 0.00150 (overall mean 0.00032, below the 0.0005 floor).
- F5: The failing Calmar of 0.066 comes from a deep, long fall. The chained pooled book reached falls of -59 % to -65 % through windows 5 to 10, while its mean daily return there was between -0.0015 and +0.0026.
