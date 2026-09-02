# E-028 — Realized allocation must reflect strategy intent, not gate state

**State:** new
**Owner:** Jeremy (operator decision required before any dispatch)
**Updated:** 2026-08-21

## Why

The engine has no way to say "no opinion". It has only "target allocation zero",
and zero means sell.

When the active regime has no strategy block, `strategies/strategy_engine.py`
`forecast()` returns a hard `0.0`. `ForecastManager.forecast_to_allocation()`
divides by 10, giving a target of `0.0`. `core/trading_bot.py` computes the
delta against the held position and rebalances whenever it is nonzero at all —
there is no drift gate. The position is sold.

But an unallocated regime does not mean "we want to be flat here". It means **we
have not yet found a strategy good enough to trade this regime**. Liquidating on
entry to it is a safety default being executed as a trading decision, and it is
recorded, costed, and graded as one.

The same divergence runs the other way through the risk layer.
`risk/risk_manager.py:_ctrl_min_allocation_change` refuses any change smaller
than its threshold, so a position the strategy wants to trim by less than the
minimum is left where it is. Both directions produce the same thing: a realized
position that is not what the strategy asked for, with nothing recording the
gap.

### Measured

`engineering/roadmap/E-027/artifacts/` (shared evidence; script and raw output
live there). Every APPROVED allocation move across all 31 run directories that
carry a `bars.csv`:

```
approved allocation moves          : 51848
  open_from_flat    : 5342 (10%)
  full_exit_to_zero : 5094 (10%)
  sign_flip         : 8335 (16%)
  partial_reduce    : 17760 (34%)
  increase          : 15317 (30%)
moves with a NONZERO forecast      : 46754 (90%)
rebalance attempts / refused       : 91122 / 39274 (43%)
```

Two things matter here, and the first is a caution against overstating the
second. **The engine is not mostly doing this.** 90% of moves are made while the
strategy holds a nonzero view — reversing (8,335), trimming (17,760), adding
(15,317). The forecast-to-allocation path works, and the strategy expresses
changes of mind continuously rather than only by going flat.

**The 10% that goes to exactly flat is the exposure.** Realized allocation can
only reach zero when the forecast is zero, so every unallocated-regime bar and
every not-ready-component bar lands in that bucket alongside genuine
ensemble-zero decisions. 5,094 moves is therefore an *upper bound* on
gate-driven liquidation, not a measurement of it — sizing the real number needs
E-027's S1 first, which is why this epic is sequenced behind it.

The second exposure is the risk band: 39,274 of 91,122 intended adjustments were
refused outright (`run_034`: 5,595 of 14,296; `run_059`: 2,273 of 2,972, 76%).
That divergence between intent and realized position is recorded nowhere.

Per-run shape, illustrating both directions:

| run | strategy off | switches | opens | full exits to zero | refused |
|---|---|---|---|---|---|
| run_026 | 90% of bars | 399 | 171 | 168 | 60% |
| run_030 | 31% of bars | 465 | 151 | 140 | 36% |
| run_023 | 14% of bars | 44 | 22 | **0** | 39% |
| run_059 | 100% of bars | 98 | 98 | 0 | 76% |

`run_023` opens 22 positions, takes none of them to flat, and has 5,569
adjustments refused. `run_059` spends every bar in an unallocated regime.

### Prior art checked (amendment 9) — this changes the available fix

`engineering/improvements/done/design_and_docs/AMENDMENTS_01-06.md` §A2.3
records that **the flicker itself has already been attacked and the attack
failed**:

> The one permitted retune cycle (48-cell grid, hysteresis + dwell) established
> analytically that stateless ER-family detection on BTC/ETH 1h is Pareto-blocked:
> activation within [10%, 40%] and transitions/window ≤ 4 cannot be satisfied
> simultaneously (best achievable ~18 transitions/window at dwell=24). Verdict:
> `unusable_for_this_symbol_timeframe`.

Standing policy A2.3(1) then forbids building a replacement detector until an
ungated edge exists. §A2.2 had already noted that a gate labelling ~1% of bars
makes any gated strategy "dark by construction".

So making the regime stop flickering is a closed lane, by measurement and by
policy. **The only remaining lever is what the engine does in response to a
flicker** — which is this epic, and which the prior art does not cover. Nothing
in `AMENDMENTS_01-06.md`, `USER_GUIDE.md` or the roadmap addresses the
forced-liquidation behaviour; a tree-wide grep for `hysteresis|dwell|flat-out|
forced close` returns only that retune record, E-012's end-of-window force-close,
and a `persistence_score` metric definition.

## Done when

Not yet written — **this epic opens on a decision, not an implementation**
(E-026 precedent). At least three defensible policies exist for "the active
regime has no strategy", and they are not equivalent in risk, cost, or honesty:

- **Hold.** Keep the existing position untouched until a mapped regime returns.
  Cheapest, but it holds risk no strategy is managing, and an unmapped regime can
  persist for thousands of bars (`run_059`: 100% of bars).
- **No new risk, decay out.** Open nothing, and reduce the existing position on a
  declared schedule. Costs turnover but bounded, and it is the honest reading of
  "we have no strategy here".
- **Keep today's behaviour, but record it.** Liquidate as now, and mark the trade
  as gate-driven so it is never graded as a signal decision. Zero behaviour
  change, and E-027 alone delivers it.

Writing a Done-when before that call would presume the answer. S1 produces the
evidence; the decision follows; the criterion is written then.

## Stories

- [ ] S1 — **Characterize, do not build.** For each of the three policies,
      establish what changes: which `file:line` sites are involved, whether the
      change is expressible in config or needs engine code, what happens to the
      risk layer's minimum-change refusal under each, and what the bit-identity
      story is. Include the `run_059`-shaped case (unmapped 100% of bars) and the
      `run_023`-shaped case (never closes). No code changes.
- [ ] S2 — (blocked on S1) The operator decision, with reasoning recorded, not
      just the verdict.
- [ ] S3 — (blocked on S2) Implement off-by-default with a test proving
      byte-identical default output, per the fork's bit-identity rule. Any
      change to default output invalidates prior baselines and must be declared
      loudly — including the pass rules pinned to `run_054`.
- [ ] S4 — Decide the minimum-change refusal separately: 43% of intended
      adjustments are silently dropped today. Options are lowering the
      threshold, accumulating the unexecuted remainder, or recording the
      divergence as a first-class metric. Do not fold this into S3 by reflex —
      it is a different control with a different failure mode.

## Relationship to other epics

- **E-027** must land first. Deciding what a gate-driven close *should* do while
  the artifacts still label it `signal_flip` means deciding without being able
  to see the result.
- **E-012** (two-bars loop defect) also force-closes positions, at end of window
  rather than on regime change. Both change recorded exits; sequence them so the
  baselines move once, not twice.
- **E-014 / E-010** (cost model, slippage): the cost attributed to these closes
  is real money in the recorded results. Whatever is decided here changes what
  the cost model is measuring.
- **E-026** (cross-sectional): sequence after this. Breadth multiplies exits.

## Log

- 2026-08-21 — `new`. Opened from a research-system-evolution review, on the
  operator's framing: a close caused by a regime having no allocated strategy is
  a security default, not a strategic decision. Prior art search found the
  flicker-side fix (hysteresis + dwell) already measured and closed as
  `unusable_for_this_symbol_timeframe`, which narrows this epic to the response
  side and is why it is worth opening now rather than being a duplicate.
