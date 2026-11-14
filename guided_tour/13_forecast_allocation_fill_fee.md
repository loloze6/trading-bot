# Stop 13: Forecast → allocation → fill → fee (the per-bar cycle)

## Speech (verbatim)

**Stop 13 of 29: Forecast → allocation → fill → fee.** Open on the side: `trading-bot/execution/forecast_manager.py`, `risk/risk_manager.py`, `core/trading_bot.py`, `execution/execution_handler.py`, `execution/portfolio_info.py`, `config.json`, `config/cost_model.json`, `core/launcher.py`.

**In one sentence.**
On every bar, the engine turns the strategy's forecast (a number between -20 and +20) into a target position, sizes it to the volatility it aims at, skips changes too small to be worth a trade, and otherwise trades at the bar's close, paying a slippage and a fee.

**Why it exists.**
A forecast is not money. Between the forecast and the result sit position size, trading frictions and costs, and these decide whether an idea survives.
The backtest must apply them exactly as live trading would, the same way for every idea, or results are not comparable and costs are underestimated.

**What comes in, what goes out.**
- In: the forecast and regime from the strategy (stop 12); the bar's prices; the account's balance; three settings files (the engine's main config, the cost table, the backtest launcher's defaults).
- Out: trades (with price, quantity, fee), an updated balance, and one recorded line per bar (stop 14).
- Next: the backtest's output files, then the three judges (stops 19-21).

**What happens here, step by step.**
1. A missing stretch of bars is checked first (the gap rule, on in every research backtest): up to 3 missing bars, nothing special; a middle gap keeps any position but blocks a new entry until the strategy has re-warmed; a large gap forces flat and restarts the strategy's warm-up.
2. The strategy reads the new bar and gives its forecast.
3. **Allocation:** the forecast ÷ 10 is the unsized signal (+10 = 100% long). With the sizing block, it is multiplied by the target volatility over the realised volatility of the last window (decision D-176), then capped at the maximum (2 times equity in run_102). Too few bars to measure volatility: flat.
4. A forecast that is not a number holds the position as it is, and is logged.
5. **The band:** a change smaller than 0.2 (20% of equity) is refused. With a sizing block, the change passes if either the signal's change or the sized change reaches 0.2.
6. **The fill:** the trade is filled at the bar's close, moved against the trader by a slippage (a buyer pays a little more, a seller gets a little less).
7. **The fee:** the account is charged the fee on each trade, as a share of the traded amount.
8. The bar's state is recorded: forecast, allocation, the band's decision, the trade, balances.
9. At the end of each test window, any open position is closed.

Example, run_102: Kraken perpetual futures fees of 5 basis points (0.05%) per trade side; BTC slippage of 2.5 basis points; a starting balance of 1,000; hourly bars; the 0.2 band; the gap rule on (`manifest.json` of each window: `gap_rule`, `fee_bps: 5.0`).

What research sets itself and what it inherits: the research backtest tool passes the coin, the exchange, the market type, the fee and the bar size; the 0.2 band and the starting balance come from the engine's defaults.

**What it costs and how long it takes.**
No AI call. The cost here is the trading cost the backtest charges: 5 bps fee per side plus 2.5 bps slippage per side on BTC (`trading-bot/config/cost_model.json`).

**What is switched off or not used here.**
- Funding payments (the periodic fee between long and short perpetual holders) are not charged: the engine setting is off and fails below daily bars.
- The portfolio risk gate (an extra kill-switch layer) is off unless a caller passes one; research does not.
- The indicator fill for gaps (filling missing bars in the strategy's memory) is a separate switch, off.
- The engine trades one coin per backtest; several coins are refused.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Forecast to allocation | `trading-bot/execution/forecast_manager.py:21`, `:58-126` | forecast / 10; sizing by realised vol; cap; flat when vol unknown |
| The band | `trading-bot/risk/risk_manager.py:28-88` | 0.2 threshold; signal-or-sized with a sizing block (`:71-88`) |
| Per-bar cycle | `trading-bot/core/trading_bot.py:326-662` | Gap check (`:353-402`), signal, allocation (`:446-463`), NaN hold (`:466-490`), risk gate, large-gap flatten (`:507-585`), middle-gap block (`:519-526`), band and rebalance (`:590-623`), record (`:637-650`) |
| One coin only | `trading-bot/core/trading_bot.py:89-95` | Refuses several symbols |
| End of run | `trading-bot/core/trading_bot.py:665-789` | Close all positions |
| Order handler | `trading-bot/execution/execution_handler.py:46-135` | Live / mock interface |
| Mock fills | `trading-bot/execution/execution_handler.py:281-423` | Slippage (`:332-362`), buy/sell/close fills (`:364-423`) |
| Fee charged | `trading-bot/execution/portfolio_info.py:85-200` | `update_local_balance` with `commission_rate` |
| Mock portfolio | `trading-bot/execution/portfolio_info.py:381-398` | Starting balance |
| Engine config | `trading-bot/config.json` | `interval: 3600`, `min_allocation_change.threshold: 0.2`, empty API keys |
| Cost table | `trading-bot/config/cost_model.json` | Kraken futures fee 5 bps, slippage per coin |
| Backtest entry | `trading-bot/core/launcher.py:619-1044` | `run_backtest`; balance 1000 (`:31`); gap rule default (`:600-616`, `:629`); fee resolution (`:876-886`); params (`:154-186`, `:243-306`) |
| Example | `runs/run_102/variants/base/results/<ts>_<hash>/manifest.json` | `gap_rule`, `fee_bps`, `slippage_bps` |

Remarks: send them as "stop 13: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

Stop 14. 
The indicator fill for gaps is off ?? 

(Guide's note: sent labelled "Stop 14"; recorded here because the indicator fill for gaps is described in this stop, section 6.)

## Inspector notes

### (1) Design and mechanism

1. The band is two thresholds in two units, and the signal one decides. With a sizing block the band passes when `|forecast/10 - signal at last fill| >= 0.2` OR `|sized target - position| >= 0.2` (`risk_manager.py:71-84`; the held signal is reset only on a successful fill, `trading_bot.py:539-541`, `:613-621`). A sized change of 0.2 is 20% of equity; a signal change of 0.2 is 2 forecast points, which on a standardised forecast of typical size 10 (stop 12a note 1.2) is a fifth of a typical value. On hourly BTC the sized allocation is `forecast/10 x 0.2/realised` with realised annual vol usually well above 0.2 (`forecast_manager.py:109`), so the sized change is a fraction of the signal change and the signal path passes first almost always. Consequence for the goal: trades fire whenever the forecast drifts 2 points from the last fill, which a standardised rank signal does often; turnover and the cost bar (stop 20) follow from this line, not from the idea. The D-176 review chose "either path" deliberately (`:29-44`); the effect is that the band no longer filters in money terms.
2. Costs are charged consistently and conservatively, in a model. Fill at the bar's close moved by the venue's per-symbol slippage (`execution_handler.py:368-369`, `:384`, `:410-413`; Kraken futures 5 bps fee, BTCUSD 2.5 bps slippage, `cost_model.json:6`, manifest `:76-87`), the fee on every leg (`portfolio_info.py:104-199`; taken in asset on a buy `:115`, in cash on a sell `:133`, grossed up on a short cover `:158`), a sign flip as a close plus an open (`execution_handler.py:97-122`: two trades, two fees, two slippages), a forced close at every window end (`trading_bot.py:697-790` via `stop() :691`). What the model leaves out is also consistent: no funding (`model_funding` default off; every Kraken brief is a perp, stop 03b note 1.5), no margin interest on the borrowed quote (`portfolio_info.py:120-124`), no liquidation (equity can go through zero; the menu notes "no liquidation in the engine", stop 08), no partial fills, no latency. "Exactly as live trading would" (the speech) is the same cost rule for every idea, not the live venue's economics.
3. The whole per-bar body is one `try/except Exception` that logs and moves on (`trading_bot.py:343`, `:658-662`). With 12b note 1.3 that makes three fail-open layers: a component error (counted), a forecast error (forecast 0, uncounted), a per-bar error (bar skipped, logged only). A bar lost here is not in `portfolio_states.csv` and not in any count the conformance check reads; the result looks like "no trade". For an engine whose output is read by code, not eyes, the third layer should count like the first.
4. The gap rule's tiers are keyed to `required_bars`, which is ~2x the component period (stop 12b note 1.1): on run_102 a "large" gap is one of 288 or more missing hourly bars (`:319`, 12 days), and a "middle" gap (4 to 287 missing) blocks every new entry for the next 288 real bars (`:401`, `:526-530`). Kraken hourly bars omit candles with no trades (`launcher.py:604-605`), so a 4-bar hole in a quiet 2018 night costs 12 days of entries. How many bars run_102 lost this way is in `metrics.json`'s `data_quality` block (stop 14); the folds file chose B/C to avoid known holes (stop 06), which says the effect was felt. The tier thresholds are the right idea with the wrong unit: "bars to flush the indicator" is the component's window, not the engine's doubled warm-up.
5. The NaN policy is HOLD (`:481-491`, operator 2026-10-01), counted and sampled; the root `CLAUDE.md` says CUL-274 "now raises immediately on `math.isnan(target_allocation)`". The code is the newer one; the orientation document is stale on a safety rule.
6. What research inherits from the live bot's `config.json` is more than the speech lists: the 0.2 band (`config.json:27`) and, for every 1h protocol, the bar interval itself (`run_protocol.py:2549-2550` passes `interval_seconds=None`, `launcher.py:854-857` reads `trading.interval: 3600`). A change to the live bot's interval would reach every hourly research backtest. The balance of 1000 is a constant (`launcher.py:31`, `:939`, `:997`), not a config value. Sound today; a coupling between the live config and the research record.
7. The order and portfolio code is Binance-era under a Kraken campaign: the quote is hard-coded `USDT` (`portfolio_info.py:100`, `:268`, `:322-323`, `:339`), `base_asset = symbol.replace('USDT', '')` leaves a Kraken `BTCUSD` unchanged, and the balance dict is keyed by the symbol so it still works (`:324`). The run's `manifest.json` records the venue and fees (`:76-87`), so the provenance is right; the labels in the ledger are not.

### (2) Legacy or simplifiable (leads)

1. `ForecastManager`'s docstring (`forecast_manager.py:17-18`, `:32-37`): "allocation percentages (-200% to +200%)" and "the caller (`trading_bot.py:305`)": the band and the call site have moved (`trading_bot.py:587-593`); the E-055 correction paragraph (`:39-55`) is a decision log inside a class.
2. `trading_bot.py:110-199`: ninety lines of constructor comments (the gap tiers twice, the per-indicator variant rejected, CUL-359 recovery) that `launcher.py:602-616` and `:771-801` repeat a third time.
3. `hasattr(self, 'portfolio_state_tracker')` (`:635`, `:754`) is always true (set in `__init__ :70`); a `None` tracker would raise into the per-bar `except` and lose the bar, not "skip state recording" as the `else` (`:655-656`) says.
4. `_execute_position_transition`'s "too small to close/open" warnings at `1e-8` (`execution_handler.py:103-120`) and `_round_quantity`/`_round_price` on the live handler (`:278-279`): live-venue precision rules the mock never applies.
5. `MockPortfolioInfo`'s `#48 F2` comment block (`portfolio_info.py:389-394`) and `PortfolioInfo`'s (`:352-356`): the same shared-default story twice.
6. `risk_gate` (`PortfolioRiskGate`, `launcher.py:184-185`, `trading_bot.py:437-438`, `:499-505`, `:561-563`) and `risk_controls` (`launcher.py:739-752`, `:949-957`): built only from a `portfolio_controls` block `config.json` does not have and research never passes. The kill-switch bypass pattern it introduced is reused by the gap flatten (`:558-560`), so the plumbing stays; the gate is weight on the research path.
7. `model_funding`/`funding_daily`/`apply_funding` (`trading_bot.py:97-108`, `:424-427`, `portfolio_info.py:204-252`): daily-bars only, off, blocked on E-014; the one modelling gap that bears on every perp brief (note 1.2).
8. The `interval` inheritance for 1h protocols (note 1.6): pass `interval_seconds` always, so a research run never reads the live bot's interval.

### (3) Disagreements between the speech and the element

1. Step 1, the gap tiers: correct (`:318-324`, `:387-391`, `:401`, `:513-515`, `:526-530`; `ignore_max_bars: 3` at `launcher.py:615`, manifest `:72`). Not stated: "large" is 288+ missing bars on run_102 and "middle" blocks entries for 288 bars (note 1.4).
2. Step 3, "the forecast / 10 ... multiplied by the target volatility over the realised volatility of the last window, then capped ... Too few bars: flat": `forecast_manager.py:92`, `:105-113`; correct.
3. Step 5, the band: correct; the dominance of the signal path (note 1.1) is not stated.
4. Step 7, "the fee on each trade, as a share of the traded amount": correct in magnitude; it is taken from the asset on a buy and from the cash on a sell (`portfolio_info.py:115`, `:133`), which the speech need not say.
5. "What research sets itself ... the fee and the bar size": the bar size is passed only when the protocol's timeframe is not `1h` (`run_protocol.py:2549-2550`); for run_102 it was inherited from `config.json` (note 1.6). Half right.
6. Section 6: all four facts correct (`model_funding` default `launcher.py:625`, not passed at `run_protocol.py:2682-2688`; `risk_gate` from an absent config block; `indicator_fill` default `:631`, `:928-932`; one symbol `trading_bot.py:89-95`).
7. Example: 5 bps, 2.5 bps BTC, 1,000, hourly, 0.2, gap rule on: manifest `:69-87`, `:94`; `launcher.py:31`; `config.json:11`, `:27`; correct. The manifest also records that the `funding_rate` feed was dropped for this run (`:107-109`), which the speech does not mention.
8. Reading-map ranges verified: `forecast_manager.py:21`, `:58-126`; `risk_manager.py:28-88`, `:71-88`; `trading_bot.py:326-662` with `:353-402`, `:446-463`, `:466-490`, `:507-585`, `:519-530` (map says `:526`), `:590-623`, `:637-650`; `:89-95`; `:665-789`; `execution_handler.py:46-135`, `:281-423`, `:332-362`, `:364-423`; `portfolio_info.py:85-200`, `:381-398`; `config.json`; `cost_model.json`; `launcher.py:619-1044`, `:31`, `:600-616`, `:629`, `:876-886`, `:154-186`, `:243-306`; the run_102 base manifest (one of six, `20261026T201743Z_a781f42e`).
