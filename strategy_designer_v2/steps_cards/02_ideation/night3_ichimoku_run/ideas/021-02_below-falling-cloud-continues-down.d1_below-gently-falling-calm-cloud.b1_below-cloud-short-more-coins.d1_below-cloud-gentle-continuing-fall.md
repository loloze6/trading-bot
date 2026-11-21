---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.b1_below-cloud-short-more-coins
line: 7.d not profitable
backtest: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.b1_below-cloud-short-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes below its Ichimoku cloud and the cloud is falling, its return over the next 26 days is negative, and more negative the slower the cloud has fallen over the past 26 days and the more the coin itself has fallen over its 26-day return, only while that 26-day return is negative.
Consequence: A trader would short a coin below a falling cloud only after the coin has itself fallen over the past 26 days under a gently sloping cloud, and would refuse the short after the coin has recovered or the cloud has dropped steeply.
Why:
- F1: The book's loss comes from shorting coins that kept rising. On the 26-day grid, coins below a falling cloud gained +3.90 % over the next 26 days (t 2.49, 353 cases), and the 995 short trades lost a mean of -4.49 % net of fees, with only 37 % winners and a book mean daily return of -0.000067 against the coins' +0.001409.
- F2: The idea's size is real on the unusual move but the wrong sign on the total. Per case the unusual move is +4.23 % (18.9 times the 0.22 % cost of a trade), but the coins' normal drift is -5.65 % in the short's direction, so the total move is -1.42 %; no holding, sizing or threshold of a short can turn that positive.
- F4: The gentle-fall grading holds, and the gentlest cloud falls are the only cases where the coin actually fell. By cloud-slope quartile, the forward 26-day return is -5.3 % on the gentlest falls (t -2.05, 88 cases) and +1.0 % on the next. It is +10.2 % (t 3.20) and +9.6 % (t 2.60) on the two steepest.
- F6: A coin below a falling cloud that has itself risen over the past 26 days rises strongly next. The top quartile of past 26-day return (mean +3.3 %) gained +14.3 % over the next 26 days, against -0.5 % to -6.0 % in the other quartiles; the Spearman correlation of past 26-day return with the forward return is +0.198.
- F7: Combining the two, gently falling clouds where the coin has also fallen over the past 26 days give the strongest continuation. That group returned -6.6 % over the next 26 days (unusual move -11.8 %, 72 cases), while steep clouds where the coin had not fallen returned +12.4 % (72 cases).
