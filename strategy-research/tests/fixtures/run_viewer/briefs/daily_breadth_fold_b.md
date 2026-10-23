---
# Daily breadth, fold B (D-130). Built from workflow_artifacts/templates/research_brief_new_pipeline.md.
# The first brief of the restarted loop: the pipeline's own loop (variant loop, decide-next,
# folds, operator approval, the analyst as idea source) on daily bars, branch 3 as signed
# (config/profitability_bars.yaml, D-118..D-120, D-127) as the only pass rule.
# Register only after this brief's PR is merged and master is merged into the operator's checkout.

strategy_domain: "daily_breadth"
market_universe: [BTCUSDT]
timeframe: "1d"
venue: "kraken"
product: "perp"
research_goal: >
  Daily breadth: find daily-bar signal rules (any mechanism: trend, momentum, mean reversion,
  volatility, volume, calendar; long or short) that earn more than Kraken perp costs on SPOT
  prices, on fold B (six 4-month blocks of 2018-2021), and that hold on coins of other
  categories. Each idea is tested one coin per variant: a base variant on BTC, design variants
  on BTC, and an asset variant on a coin of another category (config/coin_universe.yaml).
  Step 1a should extract several distinct ideas from this brief (one runs now, the others
  wait in the queue) rather than one. Who pays: slow flows and forced sellers on daily
  horizons; why it may survive costs: a daily signal trades rarely, so costs are paid a few
  times a year per coin. Information for step 1a (a fact about the branch-3 bars signed by the
  operator, not a rule of this brief): branch 3 caps the whole-test maximum drawdown at 20%, and
  a long-only book that targets about 40% a year volatility usually breaches 20% drawdown, so a
  single block will rarely pass branch 3 by itself; blocks that validate on their own criteria
  are registered and composed later. Lane 1 (a slow SMA-distance trend on BTC, ETH, LTC) is
  closed (D-128): its SMA 50 / 100 / 200 distance family is not a new idea here.
constraints:
  - "Criteria: this brief carries none (criteria_from: hypothesis_generation). Step 1a picks each idea's criteria from config/criterion_menu.yaml, per idea; they are usually not about profit. Branch 1 grades each idea on its own criteria and registers validated blocks. Branch 3, as signed in config/profitability_bars.yaml, is the pass rule. There is no hand-read rule and no continue rule outside branch 3."
  - "Out of scope, not even sized: funding carry, cross-sectional momentum (cross-coin ranking), cost engineering. A variant is one coin; a multi-coin variant is refused."
  - "Variants (one coin each): the base on BTC, at least one design variant on BTC (a config change), and one or two asset variants (an empty patch; the coin comes from a category other than BTC's, store_of_value). Candidate coins: LINK (defi); ADA, ZEC, XMR, LTC, TRX (altcoin_l1_verified_kraken); DOGE (memecoin) (AAVE and UNI did not trade before late 2020 and cannot cover fold B); the data-availability gate grades each window. ETH is in BTC's category and is refused as an asset variant."
  - "No lookahead: a bar's decision uses data timestamped at or before that bar's close; say in each idea why its inputs cannot leak."
available_data:
  - "Kraken daily OHLCV caches trading-bot/local_data/kraken_<COIN>USD_1d.csv for the coins above. The data-availability gate grades each window."
  - "Costs: Kraken perp fees and slippage from config/cost_model.yaml, applied to spot prices (venue kraken, product perp)."

criteria_from: hypothesis_generation

machine_constraints:
  protocol:
    symbols: [BTCUSDT]
    timeframe: "1d"
    fold: "B"
    start: "2018-05-01"
    end: "2021-12-31"
    window_months: 4
---

# Daily breadth, fold B

Prose below the closing `---` is for human readers only; the orchestrator never reads it.

Fold B is the six 4-month blocks of 2018-2021 (`config/folds.yaml`). A child run
of any idea found here is drawn onto another fold at random by decide-next (D-123), and
waits for the operator's `--approve` (operator approval is on).
