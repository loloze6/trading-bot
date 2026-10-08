# CLAIM_TESTS_TRADE.md: the trade-level test family (E-075 PR-3, CUL-420)

**Not shown to any prompt yet.** This file is the gated companion of `CLAIM_TESTS.md`. It is
added to an analyst's inputs only where `orchestrator.analyst.enabled` is wired (E-075 PR-5),
and `tools/claim_card.check_claim(..., trade_tests=True)` is the only call that accepts what it
describes. `CLAIM_TESTS.md` is unchanged, so every flag-off prompt is byte-identical.

The bar tests of `CLAIM_TESTS.md` select bars. A claim about what the **strategy did** (how it
exits, how long it holds, which entries pay) needs trades. One family covers it:

> **On these trades** (selector), **what the trade returned, or what the market did after its
> exit,** (outcome) is different from **the other trades** (baseline), **measured like this**
> (statistic).

A trade is one LIFO-matched lot of the run's `trades.json`
(`docs/DATA_DICTIONARY.md`, section 2): a partial reduction closes a lot, so several trades can
share an entry bar. Trades never cross windows. The test is measured on the variant's own
`trades.json` and `bars.csv`.

## The slots

| kind | parameters | meaning |
|---|---|---|
| selector `trade` | `where`: 1 to 4 clauses `{field, op, value}`, all of which must hold | the trades matching every clause |
| outcome `trade_net_return` | none (no `horizons`) | the lot's net return, a fraction (0.01 = 1%), after fees and slippage of both legs |
| outcome `post_exit_return` | `horizons`: distinct ints >= 1, in bars | the market's move from the exit bar's close to the close h bars later, signed by the trade's side (positive = the market kept moving the trade's way) |
| baseline `other_trades` | none | every other trade of the same window (a trade with a missing field is in neither group) |
| statistic `mean_diff` | none | mean outcome of the selected trades minus the baseline's mean |
| statistic `hit_rate` | none | share of selected trades whose outcome points the claimed way, minus the baseline's share |

`direction`, `floor` and `consistency` are as in `CLAIM_TESTS.md`. A floor unit counts trades
(`min_events`), windows with a selected trade (`min_windows`) or independent blocks
(`min_blocks`). The result gives the effect pooled over all windows and **each window's own
value**, as the bar tests do.

What the counts mean, so a floor is not met by one market move counted many times:

- `trade_net_return`: `min_events` counts selected lots; a block is one **stretch of
  overlapping trades** (trades whose entry-to-exit intervals overlap or touch, per window), so
  lots opened and closed together are one block.
- `post_exit_return`: lots that close on the **same bar on the same side** carry the same market
  move, so they are **one event** (the first of them, in `trades.json` order; the values are
  identical, so taking one or averaging is the same number), in the selected group and in the
  baseline alike. Blocks are counted on the **exit** bars, in blocks of `max(h, 1)` bars.
- `trade_net_return` records the return basis of each window (`all_costs`, or
  `net_of_fees_and_slippage` when the window has no complete cost record) as
  `per_window[...].basis` and `bases`. Windows with different bases are **not pooled**: the test
  is `not_measured` (reason `mixed_return_basis`).
- A trade test has an effect size and **no p-value, so no verdict**: the claim card marks it
  `verdict_possible: false`.

## The closed field list

| field | values | known | meaning |
|---|---|---|---|
| `side` | `long`, `short` | entry | the lot's side |
| `entry_hour` | 0 .. 23 | entry | UTC hour of the entry bar's start |
| `entry_weekday` | 0 (Monday) .. 6 | entry | UTC weekday of the entry bar |
| `regime_at_entry` | a regime label | entry | the regime of the entry bar (`regime` in `bars.csv`) |
| `entry_forecast` | a number | entry | the forecast of the entry bar (`forecast` in `bars.csv`) |
| `exit_cause` | `end_of_window`, `flip`, `to_zero`, `reduction`, `same_sign_flat`, `unknown` | exit | why the lot was closed (below) |
| `holding_bars` | an int >= 0 | exit | bars from the entry bar to the exit bar |

Ops: `==`, `!=`, `in` (a list) for `side`, `regime_at_entry` and `exit_cause`; those and
`>=`, `>`, `<=`, `<` for the numbers. Nothing else may be selected on: not MAE, MFE or
efficiency (they use the entry bar's own high and low or later bars: audit finding A6).

**The two exit-time fields describe what the strategy did; they are known only at the exit.**
A claim may select on them. A strategy change built from a confirmed claim may act only on the
five entry-time fields.

## `exit_cause`: the interim classifier (E-074 PHASE_A 4.2)

Per lot, in this order, from the lot's `exit_forecast` (known at the exit bar's close) and the
exit row's `postRebalance_current_allocation`:

1. `unknown`: the exit bar is not a row of `bars.csv`.
2. `end_of_window`: the exit bar is the window's **last bar** (timestamp equality). The last
   calendar day of a window is **not** enough: `run_protocol`'s own `exit_reason` labels the
   whole last day (audit finding A5; CUL-417), this one does not.
3. `unknown`: no `exit_forecast`.
4. `flip`: `exit_forecast` has the opposite sign to the lot's side.
5. `to_zero`: `exit_forecast` is exactly 0 (not ready, an error, or a filter that outputs 0).
6. `reduction`: same sign, and the position is still open on that side after the bar (a partial
   close by the rebalance).
7. `same_sign_flat`: same sign, and flat after the bar (what a gap large-tier flatten looks
   like; unexplained until E-029 records the decision).
8. `unknown`: anything else.

E-029 will replace this function with the recorded decision.

## Example

```yaml
- name: reductions_return_less
  selector:  {kind: trade, where: [{field: exit_cause, op: "==", value: reduction}]}
  outcome:   {kind: trade_net_return}
  baseline:  {kind: other_trades}
  statistic: mean_diff
  direction: less
  floor:     {min_events: 100, min_windows: 4}
```

```yaml
- name: shorts_exited_by_flip_keep_falling
  selector:  {kind: trade, where: [{field: side, op: "==", value: short},
                                   {field: exit_cause, op: "==", value: flip}]}
  outcome:   {kind: post_exit_return, horizons: [1, 6, 24]}
  baseline:  {kind: other_trades}
  statistic: hit_rate
  direction: greater
  floor:     {min_events: 100, min_windows: 4}
```
