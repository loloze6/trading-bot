---
idea: 005-06_bullish-divergence-downtrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Untestable: A bullish divergence compares RSI at the current price low with RSI at the earlier price low it undercuts. The config keeps no memory of past turning points or of the indicator values at them, so it cannot tell whether RSI's low is higher than before. No catalogue component gives RSI's position within its own past range either. Any config built from these components would drop the RSI-versus-earlier-low comparison that is the idea, and would test only "price near its range low", which is a different idea.
