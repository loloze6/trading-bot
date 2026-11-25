---
idea: 058-02_agitated-rise-swing-scaled-giveback
brief: 058_rising-agitated-overextension-gives-back
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 27e35f604dd2
---
Fidelity:
- Situation: in a rising, agitated market, the close stands above its 20-day average -> kept: code adds the rising-agitated profile; inside it the forecast is graded by the distance.
- Comparison: the distance measured in units of the coin's daily swing over the last 20 days -> replaced: no component divides the distance from a 20-day average by the 20-day standard deviation of daily returns.
- Outcome: the coin falls over the next 5 days, more the further above it stands -> kept: a short sized by the distance, held 5 bars.
- Verdict transfer: no: the stand-ins measure a different stretch, so a verdict on them would not settle the idea.
Reason: The idea needs the close's distance above its 20-day simple average divided by the standard deviation of the last 20 daily returns. No component computes this, and no composition gives it, because no op divides one component by another per bar. The nearest stand-ins each change what is measured: `PriceOverextensionHedgeComponent` uses an EMA and the spread of price levels, `KeltnerBreakoutComponent` uses an EMA and ATR and is clipped, and `vol_normalize` divides by the 24-bar spread of closes in price units.
