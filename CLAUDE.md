# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the bot

All commands are run from the `trading-bot/` subdirectory:

```bash
cd trading-bot

# Live trading
python main.py run_bot

# Backtest simulation (dates hardcoded in simulate() in main.py)
python main.py simulate

# Strategy parameter optimization (grid search, dates hardcoded in optimize_strategy())
python main.py optimize_strategy

# Analyze historical data and plot regime chart
python main.py analyze_past_data

# Fetch and validate historical data continuity
python main.py visualize_data

# Portfolio utilities (requires live Binance connection)
python main.py get_value_portfolio
python main.py get_portfolio_converted
python main.py sell_all_assets_to_target
```

## Configuration

- **`trading-bot/config.json`** — main runtime config (created on first run with defaults if absent). Sections: `api`, `trading`, `strategy`, `risk_management`, `logging`.
- **`.env`** — Binance API keys. `USE_TESTNET=True/False` switches between testnet and live. Keys read in `trading-bot/config/settings.py`.
- Backtest date ranges and `initial_balance` are hardcoded directly in `main.py` (`simulate()`, `optimize_strategy()`, `analyze_past_data()`).
- `logger.strategy_refinement` (set in `utils/logger.py`) is a custom flag that gates verbose per-component forecast logging in strategies.

## Architecture overview

The bot follows a **forecast → allocation → rebalance** pipeline. Every candle completion drives the full cycle.

### Core flow

```
DataManager (live ticks) ──► CandleBuilder
                                   │
                         candle_completion_callback
                                   │
                           TradingBot._process_symbol_candle_completion()
                                   │
              ┌────────────────────┼────────────────────┐
              ▼                    ▼                     ▼
         Strategy.update()   ForecastManager      PortfolioInfo
         Strategy.generate_signals()
              │
              ▼
         forecast (-20..+20)
              │
         ForecastManager.forecast_to_allocation()  → target_alloc (-1..+1)
              │
         ForecastManager.needs_rebalance()          → bool + Δ
              │
         RiskManager.approve_allocation_change()    → bool
              │
         TradingBot._execute_portfolio_rebalance()
              │
         ExecutionHandler.(open/close/reduce)_*_position()
```

For backtesting, `BacktestEngine` replaces `TradingBot` and `HistoricalDataManager` replaces `DataManager`. The strategy and manager objects are shared between live and backtest modes.

### Strategy hierarchy (`strategies/`)

```
MainStrategy (ABC)                     ← strategy_base.py
  └─ AdvancedStrategy                  ← main_strategy.py
       ├─ WeightedComponentRegimeDetector (CompositeStrategyForRegime)
       │    └─ [SubStrategyComponent, ...]   regime-scoring components
       └─ RegimeToStrategyMapping
            └─ {MarketRegime → CompositeStrategy}
                  └─ [SubStrategyComponent, ...]   trading components
```

- `SubStrategyComponent` — base for individual signal components. Each computes a `basic_forecast`, optionally standardizes it (mean or quantile scaling), and returns `ComponentOutput(forecast, confidence, ...)`.
- `CompositeStrategy` — weight-normalizes and combines component outputs into a single forecast via weighted sum.
- `CompositeStrategyForRegime` — extends `CompositeStrategy` with regime state tracking and change logging.
- `AdvancedStrategy.generate_forecast()` detects the current `MarketRegime`, looks up the mapped `CompositeStrategy`, and returns its forecast.
- Forecast standardization: raw forecast is normalized by `stddev_24 * close` to produce a scale-invariant signal, then scaled so the mean (or target quantile) maps to ±10.

### Key data structures

- `ComponentOutput` / `StrategyOutput` — typed dataclasses carrying forecast, confidence, regime, and `debug_info` dict.
- `RollingBuffer` — fixed-size deque of bar dicts with lazy indicator recomputation; accessed via `buffer['indicator_name']` for the latest value.
- `ForecastManager` tracks `current_allocations` and `target_allocations` per symbol. Rebalance triggers when `|new_target - actual_market_allocation| >= rebalance_threshold` (default 5%).

### Execution & portfolio

- `ExecutionHandler` / `MockExecutionHandler` (`execution/execution_handler.py`) — wraps Binance API calls or simulates them.
- `PortfolioInfo` / `MockPortfolioInfo` (`execution/portfolio_info.py`) — reads/tracks balances; `MockPortfolioInfo.update_local_balance()` simulates fills during backtesting.
- `PortfolioStateTracker` — records per-bar state snapshots to `backtest_results/` for later visualization.

### Performance tracking

- `EnhancedPerformanceTracker` (`performance/metrics.py`) — records `CompletedTrade` objects, computes Sharpe ratio, drawdown, and other metrics; has `classify_full_history()` and `plot_regime_chart()` for regime analysis.
- `ForecastAnalyzer` (`performance/forecast_analyzer.py`) — post-run analysis of forecast quality.

## Module map

| Path | Purpose |
|---|---|
| `trading-bot/main.py` | CLI entry point; wires all components together |
| `trading-bot/core/trading_bot.py` | Live trading loop and rebalance execution |
| `trading-bot/core/backtester.py` | Backtest engine extending TradingBot logic |
| `trading-bot/data/data_manager.py` | Live price fetching, candle building, historical data |
| `trading-bot/strategies/strategy_base.py` | Abstract base classes and shared primitives |
| `trading-bot/strategies/simple_strategy.py` | Concrete strategy components and regime detector |
| `trading-bot/strategies/main_strategy.py` | `AdvancedStrategy` wiring regime detector to strategies |
| `trading-bot/execution/execution_handler.py` | Order execution (live + mock) |
| `trading-bot/execution/forecast_manager.py` | Forecast→allocation conversion and rebalance gating |
| `trading-bot/execution/portfolio_info.py` | Balance reading and local simulation |
| `trading-bot/risk/risk_manager.py` | Allocation change approval |
| `trading-bot/performance/metrics.py` | Trade recording and performance metrics |
| `trading-bot/config/settings.py` | Env var loading and `ConfigManager` |
| `trading-bot/utils/logger.py` | Logger factory with custom `strategy_refinement` flag |
