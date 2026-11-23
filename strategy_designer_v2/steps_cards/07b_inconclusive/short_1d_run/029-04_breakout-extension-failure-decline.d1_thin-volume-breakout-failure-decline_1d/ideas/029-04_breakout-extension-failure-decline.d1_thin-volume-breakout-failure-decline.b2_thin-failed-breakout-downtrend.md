---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline
line: 7.b inconclusive
backtest: 029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its prior 20-day high, reaches further above it within the next 3 days, and then closes back below the old high, the coin falls over the next 5 days, only while its 60-day return is negative, and the lower the breakout day's volume was against its 20-day average volume, the larger the fall.
Consequence: Short thinly traded failed breakouts that come inside a coin's 60-day decline, and refuse those that come during a 60-day rise.
Why:
- F3: The effect shows in downtrends and is absent in uptrends. Cases where the coin's 60-day return was negative gave +2.97 % with t 2.17 over 48 cases; cases after a positive 60-day return gave −0.93 % with t −0.47 over 22.
- F4: The idea's grading by thinness is barely there. Across terciles of thinness the cases gave +1.57 % (low), +1.66 % (mid) and +2.00 % (high), all with t under 1.2, and the plan's Spearman is only 0.045.
- F5: Recomputed from prices, all failed 20-day breakouts together (321 cases) do not fall; they rise slightly more than usual (short-signed −1.19 % over 5 days, t −1.62; −2.66 % over 10 days, t −2.41). The heavy-volume quartile carries that rise (−4.29 %, t −2.01 over 5 days; −7.83 %, t −2.96 over 10 days) while the thinnest quartile is flat (+0.37 %, t 0.35). This supports the idea's consequence of refusing heavily traded failures.
