---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.d2_fading-run-in-volatility-burst
line: 7.d not profitable
backtest: 024-02_fading-volume-downrun-rebound-size.d2_fading-run-in-volatility-burst_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just fallen in an unbroken streak of four-hour periods, and the volume across the streak has been declining, it rises over the next three days, only while its price stands above its 30-day average. The rise is larger the further the price stands above that average, and the higher the coin's volatility over the past 5 days against its volatility over the past 30 days.
Consequence: A trader takes the rebound bet in a coin stretched above its monthly average during a volatility burst, and stays out once the price is below that average, where the cases lose.
Why:
- F3: The cases lose when the coin's 30-day return is mildly negative and win when it is strongly positive. With a 30-day return between -17 % and -4.5 %, the mean excess is -0.71 % (t -2.77, 677 cases); above +22 %, it is +0.95 % (t 2.56, 678 cases). The same split shows on the distance to the 30-day average: -0.73 % (t -2.91) between -9.7 % and -3.1 %, against +1.11 % (t 3.00) above +10.5 %.
- F4: Crossing the 30-day trend with the volatility ratio, the falling-trend, low-volatility-ratio cases lose -0.56 % (t -2.47, 915 cases). The rising-trend, high-volatility-ratio cases gain +0.48 % (t 1.71, 949 cases), and the top volatility-ratio quintile alone gains +0.88 % (t 2.43, 678 cases).
- F5: Held bars lose in falling 30-day and 90-day trends and earn in strong rises. With a 30-day return between -17 % and -4.5 %, the summed gain is -2.34 against +6.90 above +22 %. With a 90-day return between -29 % and +12 %, the two middle quintiles sum -0.77 and -1.80, against +2.45 above +42 %.
- F6: The book stays long almost as much in its fall windows as elsewhere, and it loses there. In the fall windows (w1–w3, w12–w14, w21–w22) the share of bars held is 0.756 against 0.807 elsewhere, and the mean gain per held bar is -0.002 % against +0.023 %. The 30-day return is negative on 43 % of bars in those windows against 34 % elsewhere.
