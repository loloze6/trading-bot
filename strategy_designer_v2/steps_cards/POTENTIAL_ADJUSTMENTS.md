# Potential adjustments (parked)

Items noted while designing the steps, not started. Each waits for the operator's go.

## Parked: why the backtest engine refuses some valid strategy configs at warm-up
Added on the operator's instruction, relayed from the "Known data defects" session. The brief is the operator's, unchanged:

> In loloze6/trading-bot, branch ccr-6624e33e-aakrpv, find out why the backtest engine refuses some valid strategy configs at warm-up. Do not change any file.
>
> Symptom: strategy_designer_v2/steps_cards/04_backtest/backtests/ has five plans that did not run, for example 003-01_low-volume-up-move-reverts_1d (see its run.md and config.json). Each stops in trading-bot/core/launcher.py: "warmup_prefetch: strategy not ready after 48 prefetch bars ... required_bars=24". All five have a regime detector with one component, BuyAndHoldStrategy, a veto applying volume_filter to it, no rules, and a flat default regime. Similar configs ran fine: for example 003-02_low-volume-down-move-reverts_1d, whose veto is on PriceEvolutionComponent.
>
> Read the code path: launcher.run_backtest warm-up, strategies/main_strategy.py is_ready, the regime engine and strategies/strategy_engine.py is_ready. You may run that one backtest through strategy_designer_v2/steps_cards/04_backtest/helper/run_backtest.py.
>
> Report in plain words:
> 1. the exact cause;
> 2. whether the config or the engine is at fault;
> 3. the smallest change to the config pattern that avoids it.
> Name periods by fold id only; never write dates.

The other session noted that running that backtest touches market data, so under the repository's hard rules it is a trial and gets a trial-ledger row, even if it only reproduces the refusal.

Since then, the refreshed plans give the refusal on one plan only: `003-02_low-volume-down-move-reverts_1d` (see `04_backtest/backtests/REVIEW.md`). After the symmetric-criteria rewrite: two plans, `003-01` and `003-02`, with the same pattern.

## Other parked items
- **Step 2: the bar size.** An idea's bar size comes from the brief, or from the idea's time scale, or else a default value. Today step 3 applies the default (1d).
- **Step 3: details only a plan can settle.** A plan should state how its non-overlapping samples are drawn, which test it uses, and what each case is ("sharp-move bars": up moves only, or every labelled bar?). Step 5's conventions cover the common cases.
- **Step 3: one judgement differs by bar size.** The same volume idea was "adapted" on daily bars and "replaced" on hourly bars (`03_test_plan/plans/REVIEW.md`). It also differs between mirror ideas: in the symmetric-criteria rewrite, 003-05 (up move) keeps an above/below-average volume split as "adapted", and 003-06 (down move) calls it "replaced" (missing-components).
- **Step 2: two ideas give the same forecast.** 002-01 (after the cross) and 002-05 (from cross to cross) become the same config in step 3.
- **The default data** (BTC/USDT, 1d, fold A): small samples, so many verdicts come out inconclusive.
- **Coins without data on the reachable venue** (BNB): parked with the quality of the backtest output.
