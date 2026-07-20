# Phase 1.2b — run_059 Replay Feasibility Recon (read-only)

Date: 2026-07-20
Precondition check: PASSED — HEAD=618d548. `git status --porcelain` showed three
untracked report files (`20260719_venue_survey.md`, `20260719_cost_model_recon.md`,
`20260720_cost_calibration.md`), all pre-existing docs-only artifacts from prior
dispatches (Dispatch A of this same effort already ran and stopped cleanly with no
trading-bot edits — confirmed by reading its report before proceeding). No code was
touched by this dispatch beyond the one output file below.

## Step 1 — equity-update arithmetic (`trading-bot/execution/portfolio_info.py`)

`CommonPortfolioDef.update_local_balance()` (lines 85-200), `commission = self.commission_rate`:

- **LONG (open/add)** — `portfolio_info.py:112-116`: `USDT.free -= cost` (full price×quantity, no
  discount); `received_qty = quantity * (1 - commission)` — commission comes out of the
  **asset side**, not the USDT side.
- **REDUCE_LONG (partial close)** — `:131-133`: `asset.free -= quantity` (full qty removed);
  `usdt_received = cost * (1 - commission)` — commission comes out of the **USDT side**.
- **SHORT (open)** — `:149-150`: `asset.locked += quantity` (full); `usdt_received = cost * (1 - commission)`.
- **REDUCE_SHORT (buy to cover)** — `:157-158`: `cost_to_buy = price * repay / (1 - commission)` —
  commission **inflates the USDT cost** required to repurchase the same asset quantity.
- **CLOSE** — `:172` (long side): `usdt_received = price * quantity * (1 - commission)`;
  `:188` (short side): `cost_to_buy = price * abs_quantity / (1 - commission)`.

Every branch nets the commission into the resulting USDT or asset balance immediately —
there is no deferred/batched fee accounting.

**Does next-trade sizing depend on the updated balance? Yes — confirmed structurally, not
just in principle.** Trade size is never a fixed absolute quantity; it's computed fresh each
rebalance as a fraction of *current* portfolio value:

- `trading_bot.py:163-165`: `total_portfolio_value = portfolio_info._calculate_total_portfolio_value(balances, close)` — read from the live/simulated balance dict, which is the accumulated result of every prior trade's commission deduction.
- `execution_handler.py:69-70`: `target_quantity = abs(target_allocation) * total_portfolio_value / current_price`; `additional_quantity = abs(allocation_change) * total_portfolio_value / current_price` — the exact formula that sizes every order.

I verified this empirically against a real run_059 walk-forward window trade log
(`runs/run_059/results/20260718T155944Z_d8cd6563/trades.json`, 17 trades): each trade's
`initial_portfolio_value` equals the **previous trade's `final_portfolio_value`** exactly
(e.g. trade 1 `final=1039.96` → trade 2 `initial=1039.96`), and `matched_quantity` changes
trade-to-trade as that value compounds. This is **multiplicative path-dependence, not
separable/linear**: change the commission rate, and portfolio value after trade 1 differs,
so the *quantity* sized for trade 2 differs, so its P&L differs, and so on for every
subsequent trade in the run — not merely the total fee bill.

### Adjacent finding, addressing your metrics.py concern directly
`performance/metrics.py`'s profit/portfolio formulas (`entry_commission`, `exit_commission`,
`net_profit_loss_absolute`, `net_profit_loss_percent`, lines 175-215) all read
`self.entry_execution.commission_rate` / `self.exit_execution.commission_rate` — **not** a
bare literal at the point of calculation. Traced all 4 `TradeExecution(...)` construction
sites in this file (lines 357-363, 480-486, 495-502, 542-548): every one explicitly passes
`commission_rate=self.commission_rate` (the tracker instance's rate), so the
`TradeExecution.commission_rate: float = 0.001` dataclass default (line 48) is **not
currently exercised** in the live call graph — it would only activate if some future call
site constructed a `TradeExecution` without passing the rate explicitly, which none do today.
So there is no *active* silent 0.1% override corrupting the profit/portfolio math right now.
That said, the underlying rate itself is still one hardcoded Python literal
(`launcher.DEFAULT_COMMISSION_RATE = 0.001`) duplicated as matching literal defaults in two
more places (`metrics.py:48`, `metrics.py:315` `EnhancedPerformanceTracker.__init__`) — real
drift risk (a future edit to one default without the other two would silently diverge), just
not a currently-live bug. Confirms the 2026-07-19 recon's recommendation stands: these three
defaults should collapse to a single sourced value, not three independently-hardcoded literals.

## Step 2 — `trades.json` schema (run_059)

Checked `runs/run_059/results/20260718T155944Z_d8cd6563/trades.json` (17 trades, non-empty).
Per-trade fields present: `trade_id`, `symbol`, `side`, `entry_price`, `exit_price`,
`entry_time`, `exit_time`, `matched_quantity`, `duration_minutes`, `profit_loss_percent`,
`profit_loss_absolute`, `entry_commission`, `exit_commission`, `total_commission`,
`total_commission_percent`, `net_profit_loss_absolute`, `net_profit_loss_percent`,
`net_portfolio_profit_loss_percent`, **`initial_portfolio_value`, `final_portfolio_value`**,
plus forecast/regime/confidence debug fields. So yes — entry/exit price, size, timestamp, and
pre/post-trade portfolio value are all recorded per trade.

## Step 3 — Verdict

**A standalone strategy-research-side replay script is NOT sufficient for an accurate
Kraken re-calibration of run_059.** `trades.json` has all the fields you'd need to *recompute
this run's numbers as if nothing else had changed* (e.g. re-deriving `net_profit_loss_absolute`
at a new rate for each recorded trade in isolation), but that is not the same as an accurate
recalibration: because `matched_quantity` at every trade was itself sized off a portfolio value
that already embeds the old 10bps commission's cumulative effect, any different fee rate would
have produced different portfolio values and therefore **different trade quantities from the very
first trade onward** — a different trade path, not just different fee totals on the same path.
The only accurate way to answer "what would run_059 have looked like under Kraken's fee
schedule" is to re-run trading-bot's own engine with a parameterized commission input (per the
2026-07-19 recon's recommendation to parameterize `DEFAULT_COMMISSION_RATE` / thread a
`commission_rate` argument through `run_backtest`), not a post-hoc arithmetic pass over the
existing trade log.
