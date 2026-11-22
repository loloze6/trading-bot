---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends.b1_bounce-fade-all-coins
line: 7.d not profitable
backtest: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends.b1_bounce-fade-all-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, a one-day rise that is large relative to its 20-day standard deviation of daily returns is followed by a fall over the next 5 days. The more negative the coin's 365-day return, the larger the fall that follows.
Consequence: A trader would fade bounces in coins whose fall extends over the past year, and refuse to fade bounces in coins that are only dipping inside a rising year.
Why:
- F1: The fade is real against the coin's drift but not in price: over the 2419 short cases the coin's 5-day move in the short direction is −0.19 % in total (t −0.84) and +0.55 % unusual (t 2.50). The book pays the total move, and that sits below zero before the 0.22 % cost of a trade, so the book loses (Sharpe −0.32, mean daily return −0.0002).
- F2: The losses come from years when the coins were rising. Short cases lost −4.10 % over 5 days in 2020 (t −4.50, n 141), −2.25 % in 2021 (t −2.24) and −2.03 % in 2023 (t −4.12). The coin's mean daily return in those years was +0.44 %, +0.54 % and +0.32 %. The cases gained in 2018, 2022 and 2025 (+0.74 %, +0.46 %, +2.19 % with t 4.37), when the coin's mean daily return was −0.35 %, −0.24 % and −0.03 %.
- F4: Net trades average −2.72 % (median −1.19 %, 4228 trades). Their mean length is 9.4 days against the 5-day horizon, and the cases' total short move worsens from −0.19 % at 5 days to −0.35 % at 10 days. Holding past the horizon adds loss.
