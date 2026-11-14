---
line: 7.d not profitable
backtest: N2-02_capitulation-rebound_1d
idea tested: N2-02_capitulation-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3571 USD
---
## Findings
- **F1:** Fees are not why the book fails: the 593 trades, all long, earn 4.18% before fees and 4.08% after, against 0.33% commission each, with 69% winners. The book is simply small and rarely invested: it holds a position on 19.9% of days, at a mean size of 0.54 when it does, so its mean daily return is 0.000465, below the 0.0005 bar.
- **F2:** A larger forecast earns more. Trade gross gain rises with entry forecast: 1.52% for forecasts 1–5 (n=113), 3.16% for 5–10 (n=173) and 5.74% for 10 and above (n=307). On non-overlapping 10-bar excess returns, forecasts 0–5 are negative (−0.0145, t −1.36, n=137; −0.0134, t −1.10, n=87) and forecasts of 10 and above are positive (+0.0206, t 0.90, n=69).
- **F3:** The Calmar failure comes from two falling-market years. Trades lost before fees in 2018 (−0.74%, n=88, 51% winners) and 2022 (−0.41%, n=197, 61% winners). In those years the mean window drawdown was −0.16 and −0.21, with the worst at −0.53 and −0.74. In 2020 trades made +24.7% (n=63), and in 2023–2024 about +6.1%.
- **F4:** The rebound pays only near a fresh low. Active bars within 3% of their 5-day low have a mean 10-bar excess return of +0.0061 (t 0.49, n=170). Bars already more than 8% above that low have −0.0234 (t −1.96, n=93). Bars after a rising 3-day close have −0.0117 (t −1.17, n=145), against +0.0008 after a falling 3-day close (n=191).
- **F5:** The rebound is short-lived. Trades held 2 days or less gain 4.56% before fees with 85% winners, and trades held 5–15 days gain 5.62%. Trades held 15–40 days gain only 2.43% with 49% winners (n=101), and trades held over 40 days gain 1.15% with 48% winners (n=48).
- **F6:** The book earns most when volatility is highest. In the top tercile of prior 20-day volatility, the mean in-position book return is 0.0041 per day (n=1008). The low and middle terciles give 0.0011 and 0.0018.

## Ideas
- `N2-02_capitulation-rebound.d1_rebound-starts-at-fresh-low` (from F2, F4): When a coin's close is extremely far below its 200-day average, it rises over the next one to two weeks while the close is still within a few percent of its 5-day low. Once the close has already bounced well off that low, it tends to fall instead.
- `N2-02_capitulation-rebound.d2_capitulation-rebound-fades-fast` (from F1, F5): The rise after a capitulation close comes in the first one to two weeks; after that, the coin's return falls back to an even coin-flip.
- `N2-02_capitulation-rebound.d3_panic-flush-rebound-only` (from F3, F6, F2): Extreme depth below the 200-day average is followed by a rise mainly when the coin's recent daily volatility is in its highest range, that is, during a true panic flush rather than a slow grind lower like those of 2018 and 2022.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
