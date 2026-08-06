# Maker/Limit Execution — Engine Assessment (Backlog, Not Implementation)

Cost-structure revision, 2026-07-04. This is an assessment of what maker/post-only
execution would require in the trading-bot engine — explicitly **not** an
implementation. Live execution changes are out of Phase P research scope; backtests
may assume maker fees only via the `execution_style.maker.round_trip_cost_bps_blended`
figures in `config/cost_model.yaml`, which already bake in a fill-rate haircut so no
engine change is a prerequisite for that config-level assumption to be used in
research arithmetic (e.g. the viable-space map, `11_viable_space_map.md`).

## Current state (verified against code)

`trading-bot/execution/execution_handler.py` places only synchronous market orders:

- `open_long_position` / `open_short_position`: `type=Client.ORDER_TYPE_MARKET` (lines
  187–190, 222–225). No limit price, no `timeInForce`, no post-only flag.
- `close_position`: same, `ORDER_TYPE_MARKET` (lines 255, 259).
- Fill price for every path is `data['close'].iloc[-1]` — the just-completed candle's
  close — read synchronously in the same call that submits the order. There is no
  concept of "order pending" anywhere in `BaseExecutionHandler` or `ExecutionHandler`.
- `MockExecutionHandler` (backtest path) mirrors this exactly: every order is assumed
  to fill in full, instantly, at the candle close (`portfolio_info.py:update_local_balance`
  is invoked immediately after with that same price). There is no bid/ask, no
  intrabar path, no possibility of "no fill" anywhere in the simulation.

This is a reasonable model for market orders (which do fill immediately, modulo
slippage already captured in `cost_model.yaml`) but has no analog for limit orders,
which may rest unfilled for an unknown duration or never fill at all.

## What maker/post-only execution would require

### 1. Live order type
Binance spot's post-only order type is `LIMIT_MAKER` (rejected by the exchange outright
if it would cross and take — this is what guarantees the maker fee, not just a `LIMIT`
order with `timeInForce=GTC`, which can still take if it crosses). `ExecutionHandler`
would need a new order-submission path parallel to the existing market-order calls,
plus:

- **Price selection.** The engine currently has no live order-book or best bid/ask feed
  — `data` is OHLCV candle data only (`data/data_manager.py`). Quoting at/inside the
  touch requires a ticker or depth stream that does not exist today.
- **Order-state tracking.** `self.positions[symbol]` today is written the instant an
  order returns `executedQty`. A resting `LIMIT_MAKER` order returns immediately with
  `status=NEW` and zero fill; the engine would need a pending-order table, a polling or
  websocket user-data-stream path to detect fills, and a timeout/cancel policy.
- **Unfilled-order handling.** A policy decision, not just code: cancel and re-quote at
  a new price, cancel and convert to a taker market order (chase-fill — the assumption
  used in `cost_model.yaml`'s blended cost), or leave resting past the signal's
  validity window (risking a stale fill). Each has different cost and correctness
  implications for the forecast → allocation → rebalance loop, which currently assumes
  the rebalance either fully executes or fails outright (`_execute_portfolio_rebalance`
  returns a single `(success, debug)` pair, not a partial/pending state).
- **Rebalance-loop interaction.** `ForecastManager.needs_rebalance()` and
  `RiskManager.approve_allocation_change()` both assume the portfolio's actual
  allocation is up to date at the start of each candle. A resting unfilled maker order
  means actual allocation lags target for an unknown number of candles — the gating
  logic would re-signal against a stale allocation unless it's made pending-order-aware.

  > **Correction (2026-07-28, dispatch W11).** `ForecastManager.needs_rebalance()`
  > does not exist and never did; there is no drift-threshold gate anywhere in the
  > loop. The engine rebalances toward target on every bar whenever the delta is
  > nonzero (`trading_bot.py:229`), and `config.json`'s `rebalance_threshold` is dead
  > (only reference commented out at `launcher.py:110`). See
  > `engineering/improvements/known_divergences.md` §1. The concern above is **worse** than stated, not
  > better: with no drift band at all, a stale actual-allocation reading is re-signalled
  > against on the very next bar rather than being absorbed by a threshold.

### 2. Backtest-side simulation
This is the harder problem, and it is currently **infeasible without a new feed**:

- `MockExecutionHandler` only has access to OHLCV bars (`data['close']`, etc.). Whether
  a resting limit order at a given price would have been touched within a bar requires
  either intrabar bid/ask or at minimum high/low-based touch simulation with a fill
  probability model — and even the high/low touch heuristic overstates fill likelihood
  (touching a price level doesn't guarantee a resting order at that level would have
  been filled ahead of other resting size).
- `order_book` is explicitly listed as an **unavailable feed** in
  `config/available_feeds.yaml` (routes to `feed_wishlist.yaml`). This is the same
  feed gap already tracked for order-book-imbalance hypotheses.
- Consequence: there is no way to empirically calibrate `assumed_fill_rate` in
  `cost_model.yaml` against this account's own data today. The values there
  (0.65 BTC/ETH, 0.50 SOL, 0.45 AVAX) are documented placeholder priors, not
  measurements, exactly per the cost-structure revision's requirement for an
  "explicit fill-rate haircut" — explicit meaning visible and labeled as an
  assumption, not validated.

## Backlog item (for future implementation, not now)

**Title:** Post-only maker execution path + fill-rate calibration
**Status: PARKED (2026-07-04).** No fee benefit at this account's tier (Regular/VIP0:
maker fee == taker fee, see `config/cost_model.yaml` FEE-TIER VERIFICATION). At VIP0,
the only possible maker advantage is spread/slippage avoidance, which is already
sensitivity-modeled in `execution_style.maker` with an unvalidated fill-rate haircut
— and per the `verdict_execution_style: taker` hard rule, that sensitivity number can
never drive a gate or promotion decision anyway. Building the engine support now would
have no research payoff. **Revisit only when either:** (a) the account reaches VIP1
(>= $1M 30-day volume AND >= 5 BNB), where maker fee genuinely undercuts taker fee, or
(b) an `order_book` feed is acquired, making real fill-rate calibration (rather than a
placeholder assumption) possible.
**Blocked by:** `order_book` feed acquisition (for backtest-side fill simulation);
without it, live-only maker execution could still be built and would just carry the
config-documented assumed fill rate until enough live trade history exists to
recalibrate it empirically.
**Scope when unblocked:**
1. `ExecutionHandler`: `LIMIT_MAKER` order path, pending-order state, timeout →
   cancel-and-convert-to-taker policy (matching the `unfilled_handling` assumption
   already encoded in `cost_model.yaml`).
2. `MockExecutionHandler`: intrabar fill simulation using order-book or synthetic
   depth data once available; until then, backtests may only use the blended
   (fill-rate-haircut) cost figures as a static cost assumption, never a "100% filled
   at maker fee" figure.
3. `ForecastManager` / rebalance loop: pending-order-aware gating so a resting order
   doesn't get re-signaled against every subsequent candle.
4. Recalibrate `execution_style.maker.assumed_fill_rate` in `cost_model.yaml` against
   realized live fill data once available (this is the same self-calibration loop
   already established for `cost_drag` — see `09_cost_hurdle_gate.md`'s "Interaction
   with existing cost_drag rule").

**Not in scope for Phase P research:** any of the above. Phase P research may use the
`round_trip_cost_bps_blended` figures as a cost assumption in arithmetic (e.g. the
viable-space map) but must not claim maker execution is implemented or validated.
