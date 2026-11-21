---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.b1_slow-cloud-fall-more-coins
line: 7.d not profitable
backtest: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.b1_slow-cloud-fall-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes below its Ichimoku cloud and the cloud is falling, its return over the next 26 days is negative, and more negative the more slowly the cloud has fallen over the past 26 days and the thinner the cloud is relative to the price.
Consequence: A trader shorts a coin below a thin, gently falling cloud and refuses the short below a thick cloud, where the coin tends to rebound.
Why:
- F1: The book loses because the coins rose after the signal: over the 26 days after a grid case, the coin's mean return was +3.90 % (t 2.49, 353 independent cases), against its normal drift of +5.66 %, so the short's total move is -1.86 % per case. The trade cost is 0.22 %, so cost is not the cause. The 1398 short trades lost 3.23 % each on average after fees and won 39 % of the time.
- F4: The slow-fall gradient holds in raw returns. The slowest-falling quarter of the cloud (slow_fall 0.19 to 0.98) was followed by -5.3 %, the two fastest quarters by +9.6 % and +10.2 % (88 to 89 cases each), and slow minus fast is -10.0 % (Welch t -3.21, 137/137). It is strongest where the coin's 26-day return is also below its median: slow fall there gives -6.6 % (72 cases), while fast fall with an above-median 26-day return gives +12.4 % (72).
- F5: The thickest cloud quarter (thickness 30 % to 142 % of the price) was followed by a rise of 27.3 % over 26 days (24 cases). The three thinner quarters were followed by -5.6 %, -15.3 % and -3.0 % (23 to 24 cases each).
