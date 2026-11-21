---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues
line: 7.b inconclusive
backtest: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes below its Ichimoku cloud and the cloud is falling, its return over the next 26 days falls short of the coin's normal drift, and by more the more slowly the cloud has fallen over the past 26 days, the coin's slowest-falling clouds giving the largest shortfall.
Consequence: A coin sitting below a gently drifting cloud is a reason to short it against its usual rise, while a coin below a cloud that has collapsed fast is a reason to refuse the short, because those cases rebound hardest.
Why:
- F2: The idea's graded part is clear, and it points where the idea says. The slow-fall half earns +7.32 % beyond drift (t 3.06, 78 cases, strength 0.29), the fast-fall half -4.30 % (t -1.20, 78 cases). Their difference is +11.6 % with Welch t 2.70, and regressing the excess on log slowness gives slope 0.075 (t 2.91, 156 cases). By slowness quartile, from fastest to slowest fall, the excess runs -7.5 %, -1.1 %, +6.8 % (t 1.95) and +7.8 % (t 2.36).
- F3: The forecast's own size orders the outcome the same way. The most-short quartile earns +8.3 % (t 1.71) and the least-short quartile -7.2 % (t -1.36), 39 cases each. The main measure averages strong slow-fall cases with fast-fall cases that go against the short, and that mix is what keeps its t low.
- F4: The effect depends on the market's own moves by year. The short pays in 2018 (+20.0 %, t 4.86, 34 cases), 2019 (+5.5 %, t 2.44) and 2025 (+9.1 %, t 1.92). It loses badly in the bull years 2020 (-32.8 %, t -3.00, 7 cases) and 2021 (-35.3 %, t -2.91, 12 cases), and those losses come almost entirely from fast-fall cases (-38.4 % and -58.6 %).
