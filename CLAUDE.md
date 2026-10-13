# CLAUDE.md

## Repository overview
This repository contains:
- `trading-bot/`: the executable trading bot and existing backtest framework
- `strategy-research/`: research workflow, artifacts, schemas, skills, and orchestration for strategy refinement

## Primary objective
When working on strategy research or iteration, prefer integrating with the existing `trading-bot` architecture rather than proposing new infrastructure.

## Key commands
From repository root:
- Backtest flow is implemented under `trading-bot/`
- Main simulation entry point: `python trading-bot/main.py simulate`

## Important constraints
- Prefer minimal code changes.
- Reuse the existing forecast -> allocation -> rebalance pipeline.
- Do not propose replacing the full bot architecture unless explicitly requested.
- Keep changes testable and reversible.

## Project guidance
- Use `strategy-research/CLAUDE.md` for the research workflow and artifact-based process.
- Use local folder context before inventing new abstractions.

## Hard rules
- Never commit secrets or venvs. If you see keys, stop and tell the operator; never echo values.
- No lookahead: a bar's decision uses only data timestamped at or before that bar's close. Every new feature or data source needs a "why this can't leak" note.
- Every experiment that touches market data is a trial and gets a row in the trial ledger, including failures and abandoned ideas.
- The sealed holdout is used very rarely. Refer to its dates only through `strategy-research/config/campaign_data_policy.yaml`; never write them out. Its store is the literal directory `local_data/holdout_sealed/`.
