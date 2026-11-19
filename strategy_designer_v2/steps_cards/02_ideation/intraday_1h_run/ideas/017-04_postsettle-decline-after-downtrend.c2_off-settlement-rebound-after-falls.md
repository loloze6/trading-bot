---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-04_postsettle-decline-after-downtrend
line: 7.c rejected
backtest: 017-04_postsettle-decline-after-downtrend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin with a strong 3-day run down, the return over the next 2 hours from closes away from the funding settlement times is positive, and the deeper the 3-day fall, the larger that rebound.
Consequence: Outside settlement hours, a trader should expect a deep 3-day fall to bounce briefly, and should refuse to add to shorts there.
Why:
- F3: At hours with no settlement, the same deep 3-day fall is followed by a bounce rather than a decline: the excess 2-bar return is +4.86 bp for a standardised change below -2 (n 23280), against -8.54 bp at settlements. Down-trend settlement events minus down-trend other hours give a Welch t of -4.1.
- F2: After a 3-day fall, the coin did decline over the 2 hours after settlement, and the decline grows with the fall. The mean excess 2-bar return is -8.54 bp for a standardised 3-day change below -2 (n 3275), -5.14 bp for -2 to -1 (n 10399), -2.97 bp for -1 to -0.5 and -0.67 bp for -0.5 to 0. The step-5 supporting check agrees: largest third minus smallest third is -0.000988.
