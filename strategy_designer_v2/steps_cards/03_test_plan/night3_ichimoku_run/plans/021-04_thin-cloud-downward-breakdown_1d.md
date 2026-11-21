---
idea: 021-04_thin-cloud-downward-breakdown
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: a31b77de3651
---
Fidelity:
- Situation: a daily close crossing down from above the cloud to below it -> adapted: "after the cross" made "while below the cloud", graded by the distance below the cloud bottom (`IchimokuCloudPositionComponent`, edge "nearest", clip max 0).
- Comparison: the thinner the cloud at the cross, relative to price, the larger the fall -> replaced: no component grows as the cloud thins, and the catalogue offers only cloud width, which grows as it thickens.
- Outcome: the coin falls over the next 26 days -> kept: a short held for 26 bars on daily bars.
- Verdict transfer: no: without a graded thinness reading, the test cannot show whether thin-cloud crosses fall more than thick-cloud ones.
Reason: The forecast must grow, inside the below-cloud regime, as the cloud thins, and every combination tried fails. `IchimokuCloudWidthComponent` standardised grows with thickness, and `negate` keeps it larger for thick clouds. A constant offset to centre it is barred inside a regime and would go long under thick clouds. Running it without a regime would short every thin cloud, which replaces the situation. A weighted sum cannot form an inverse or a product of width and the break below the cloud.
