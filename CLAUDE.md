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