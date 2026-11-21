---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.b1_below-cloud-short-more-coins
line: 7.g patterns
backtest: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.b1_below-cloud-short-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's return over the next 26 days is higher the higher its own return over the past 26 days, both above its normal drift after its largest 26-day rises and below its drift after its largest 26-day falls.
Consequence: A trader would lean long a coin in proportion to its 26-day rise and short it in proportion to its 26-day fall, holding about 26 days, and refuse to fade a strong 26-day move.
Why:
- F1: Across all coins, the coin's own 26-day return grades its next 26 days on the 26-day grid (about 900 non-overlapping cases). The quartile with the largest past fall ends -5.7 % below the coin's drift (strength -0.17, t -3.3, 228 cases). The quartile with the largest past rise ends +6.5 % above it (strength +0.15, 226 cases). Top minus bottom: Welch t 3.4, Spearman 0.10. The top-minus-bottom gap of about 12 % over 26 days is more than 50 times the 0.22 % cost of a trade. The relationship is not steady by year: Spearman is -0.29 in 2018 and -0.14 in 2024, and +0.24 in 2021 and +0.15 in 2022.
- F2: The 52-day return grades the same way, though less sharply. The top quartile ends +11.1 % above drift (strength +0.29, t 2.9, 152 cases), against +0.4 % for the bottom quartile (152 cases); top minus bottom Welch t 2.0.
