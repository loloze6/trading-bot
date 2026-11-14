---
idea: 005-06_bullish-divergence-downtrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price at a new low while RSI makes a higher low -> replaced: no catalogue component measures RSI's current low against its earlier low.
- Comparison: RSI's current low against its prior low, within the same window as the price low -> replaced: RSI is only available as a level (50 - RSI), never as a position against its own recent extremes.
- Outcome: price keeps falling to further lows -> kept: a negative, short forecast whose gain is measured over the following bars.
- Verdict transfer: no: a test of "price near its low and RSI not oversold" is a different situation from "RSI makes a higher low".
Reason: The divergence compares where price sits in its recent range with where RSI sits in its own recent range. The catalogue gives the price side (`DonchianBreakoutComponent`) but only a raw RSI level (`RSIPullbackComponent`), and no weighted sum of those reproduces "RSI above its own recent minimum". With an RSI range-position component, the forecast would be the standardised Donchian minus the standardised RSI position, clipped at max 0 to keep only the bullish-divergence case. That is a graded short that grows as price sits lower in its range while RSI sits higher in its own.
