---
line: 7.g patterns
backtest: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.b1_below-cloud-short-more-coins_1d
idea tested: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.b1_below-cloud-short-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5181 USD
---
## Findings
- **F1:** Across all coins, the coin's own 26-day return grades its next 26 days on the 26-day grid (about 900 non-overlapping cases). The quartile with the largest past fall ends -5.7 % below the coin's drift (strength -0.17, t -3.3, 228 cases). The quartile with the largest past rise ends +6.5 % above it (strength +0.15, 226 cases). Top minus bottom: Welch t 3.4, Spearman 0.10. The top-minus-bottom gap of about 12 % over 26 days is more than 50 times the 0.22 % cost of a trade. The relationship is not steady by year: Spearman is -0.29 in 2018 and -0.14 in 2024, and +0.24 in 2021 and +0.15 in 2022.
- **F2:** The 52-day return grades the same way, though less sharply. The top quartile ends +11.1 % above drift (strength +0.29, t 2.9, 152 cases), against +0.4 % for the bottom quartile (152 cases); top minus bottom Welch t 2.0.
- **F3:** On the active bars (close below a falling cloud, 353 grid cases), the coin's own 26-day return grades what follows. The two terciles with the largest past falls end -7.2 % and -10.6 % below drift (strengths -0.21 and -0.32, t -3.0 and -4.4, 91 and 86 cases). The tercile with the smallest fall ends +5.1 % above (strength +0.18, 97 cases). Top minus bottom Welch t 3.1.
- **F4:** On the same active bars, the recorded cloud slope grades what follows. The tercile with the gentlest fall ends -8.7 % below drift (strength -0.27, t -3.8, 124 cases). The tercile with the steepest fall ends +3.7 % above (strength +0.16, 118 cases). Welch t -3.7.
- **F5:** Overall, active bars end -1.8 % below the coin's drift (353 cases), while inactive bars end +0.8 % above it (843 cases). The coin did tend to lag under the cloud. Even so, the book's 995 shorts lost 4.5 % each on average after fees, with only 37 % of them winning. The book's mean daily return is -0.004 %, against a 26-day unusual move of +4.23 %, which is 18.9 times the cost of a trade.
- **F6:** Two other patterns showed up, and neither yields a graded idea.

## Ideas
- `021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.b1_below-cloud-short-more-coins.g1_26-day-momentum-continues` (from F1, F2): A coin's return over the next 26 days is higher the higher its own return over the past 26 days, both above its normal drift after its largest 26-day rises and below its drift after its largest 26-day falls.
- `021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.b1_below-cloud-short-more-coins.g2_below-cloud-fall-keeps-falling` (from F3, F5): When a coin closes below its falling Ichimoku cloud, its return over the next 26 days is more negative the larger its own fall over the past 26 days has been.
- `021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.b1_below-cloud-short-more-coins.g3_gentle-cloud-fall-continues` (from F4, F5): When a coin closes below its falling Ichimoku cloud, its return over the next 26 days is more negative the more gently the cloud's midpoint has fallen over the past 26 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
