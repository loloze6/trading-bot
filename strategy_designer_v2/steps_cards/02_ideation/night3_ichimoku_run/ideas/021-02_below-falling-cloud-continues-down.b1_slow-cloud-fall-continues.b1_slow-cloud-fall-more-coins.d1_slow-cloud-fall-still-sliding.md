---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.b1_slow-cloud-fall-more-coins
line: 7.d not profitable
backtest: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.b1_slow-cloud-fall-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes below its Ichimoku cloud and the cloud is falling, its return over the next 26 days is negative, and more negative the more slowly the cloud has fallen over the past 26 days, only while the coin's own 26-day return is still negative and has not turned into a recovery.
Consequence: A trader shorts a coin below a gently falling cloud only while the coin is still sliding, and refuses the short once its past 26 days show a rebound.
Why:
- F1: The book loses because the coins rose after the signal: over the 26 days after a grid case, the coin's mean return was +3.90 % (t 2.49, 353 independent cases), against its normal drift of +5.66 %, so the short's total move is -1.86 % per case. The trade cost is 0.22 %, so cost is not the cause. The 1398 short trades lost 3.23 % each on average after fees and won 39 % of the time.
- F2: The result depends on the year. The cases fell in 2018 (-16.0 %, 34 cases) and 2025 (-9.9 %, 61 cases), and the book's window Sharpes there were up to 2.9 (w14) and 2.6 (w24). The cases rose in 2020 (+23.9 %, 13), 2021 (+36.4 %, 23), 2023 (+25.9 %, 44) and 2024 (+11.9 %, 35). In those years windows w4, w10, w11, w16 and w21 had book Sharpes of -3.1 to -3.7, which is why the lowest Sharpe with one window left out is -0.20.
- F3: The coin's own 26-day return sorts the outcome. When the coin had already recovered (its 26-day return in the top quarter, -3.5 % to +31 %), it rose a further 14.3 % over the next 26 days (69 cases). When it had fallen moderately (-24 % to -13 %), it went on to fall 6.0 % (68 cases). On the book's short bars, only the -18 % to -6 % quarter of the 26-day return earned (+10.1 bps per bar); the other three quarters earned -0.1, -2.8 and -3.3 bps.
- F4: The slow-fall gradient holds in raw returns. The slowest-falling quarter of the cloud (slow_fall 0.19 to 0.98) was followed by -5.3 %, the two fastest quarters by +9.6 % and +10.2 % (88 to 89 cases each), and slow minus fast is -10.0 % (Welch t -3.21, 137/137). It is strongest where the coin's 26-day return is also below its median: slow fall there gives -6.6 % (72 cases), while fast fall with an above-median 26-day return gives +12.4 % (72).
- F6: Cases far below the cloud whose 26-day return was above its median rose 56.4 % over the next 26 days (11 cases). Far-below cases whose 26-day return was below its median fell 11.5 % (36 cases).
- F7: Shorts carried past the end of the situation lost money. On bars in the regime the book held -0.29 of its value and earned +0.93 bps per bar (10556 bars). On bars outside it, it still held -0.10 and earned -0.50 bps per bar (25550 bars).
