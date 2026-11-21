---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.b1_below-cloud-short-more-coins
line: 7.g patterns
backtest: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.b1_below-cloud-short-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes below its falling Ichimoku cloud, its return over the next 26 days is more negative the larger its own fall over the past 26 days has been.
Consequence: A trader shorting a coin below a falling cloud would size the short with the coin's own 26-day decline, and avoid the short where the coin has barely fallen.
Why:
- F3: On the active bars (close below a falling cloud, 353 grid cases), the coin's own 26-day return grades what follows. The two terciles with the largest past falls end -7.2 % and -10.6 % below drift (strengths -0.21 and -0.32, t -3.0 and -4.4, 91 and 86 cases). The tercile with the smallest fall ends +5.1 % above (strength +0.18, 97 cases). Top minus bottom Welch t 3.1.
- F5: Overall, active bars end -1.8 % below the coin's drift (353 cases), while inactive bars end +0.8 % above it (843 cases). The coin did tend to lag under the cloud. Even so, the book's 995 shorts lost 4.5 % each on average after fees, with only 37 % of them winning. The book's mean daily return is -0.004 %, against a 26-day unusual move of +4.23 %, which is 18.9 times the cost of a trade.
