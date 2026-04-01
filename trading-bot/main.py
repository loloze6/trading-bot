"""
Trading Bot Main Entry Point
Provides command-line interface for running live bot, backtesting, optimization, and utilities.
"""

from core.trading_bot import TradingBot
from core.backtester import BacktestEngine
from data.data_manager import DataManager, HistoricalDataFetcher, HistoricalDataManager, CandleBuilder
from execution.execution_handler import ExecutionHandler, MockExecutionHandler
from risk.risk_manager import RiskManager, MockRiskManager
from execution.portfolio_info import PortfolioInfo, MockPortfolioInfo, PortfolioStateTracker
from execution.forecast_manager import ForecastManager
from strategies.main_strategy import AdvancedStrategy
# from strategies.simple_strategy_copy import SimpleMovingAverageStrategy, BuyAndHoldXPeriodsStrategy
from performance.metrics import EnhancedPerformanceTracker
from utils.logger import setup_logger
from config.settings import ConfigManager
import argparse
import os
import sys
import datetime
import logging
from typing import Tuple, Optional


def initialize_config_and_logger() -> Tuple[Optional[ConfigManager], Optional[logging.Logger]]:
    """
    Load and validate configuration, setup logger.
    
    Returns:
        Tuple of (ConfigManager, Logger) or (None, None) if validation fails.
    """
    try:
        config = ConfigManager('config.json')
        
        if not config.validate():
            print("ERROR: Configuration validation failed. Please check config.json")
            return None, None

        # Use the new get_log_level method for cleaner code
        log_path = config.get('logging', 'file_path', 'logs/bot.log')
        log_level = config.get_log_level()  # ← UPDATED: Use new helper method
        
        logger = setup_logger('trading_bot', log_path, log_level)
        logger.info("="*80)
        logger.info("Trading Bot Initialized")
        logger.info(f"Config: {config}")
        logger.info("="*80)
        
        return config, logger
        
    except Exception as e:
        print(f"FATAL: Failed to initialize configuration: {e}")
        return None, None


def parse_date_safe(
    date_str: str, 
    logger: logging.Logger, 
    default_days_back: int = 30
) -> datetime.datetime:
    """
    Parse date string with fallback to default.
    
    Args:
        date_str: Date in YYYY-MM-DD format
        logger: Logger instance
        default_days_back: Number of days to go back if parsing fails
        
    Returns:
        Parsed datetime or default date
    """
    try:
        parsed_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        logger.debug(f"Parsed date: {date_str} -> {parsed_date}")
        return parsed_date
    except ValueError as e:
        logger.error(f"Invalid date format '{date_str}': {e}")
        default_date = datetime.datetime.now() - datetime.timedelta(days=default_days_back)
        logger.warning(f"Using default date: {default_date.strftime('%Y-%m-%d')}")
        return default_date


def create_strategy(
    config: ConfigManager, 
    logger: logging.Logger,
    strategy_class=AdvancedStrategy
):
    """
    Create strategy instance from config parameters.
    
    Args:
        config: ConfigManager instance
        logger: Logger instance
        strategy_class: Strategy class to instantiate
        
    Returns:
        Configured strategy instance
    """
    strategy_params = config.get('strategy', 'params', {})
    
    # if strategy_class == SimpleMovingAverageStrategy:
    #     short_window = strategy_params.get('short_window', 50)
    #     long_window = strategy_params.get('long_window', 200)
    #     logger.info(f"Creating SimpleMovingAverageStrategy (short={short_window}, long={long_window})")
    #     return SimpleMovingAverageStrategy(
    #         short_window=short_window,
    #         long_window=long_window
    #     )
    # elif strategy_class == AdvancedMovingAverageStrategy:
    #     logger.info("Creating AdvancedMovingAverageStrategy")
    #     return AdvancedMovingAverageStrategy()
    # elif strategy_class == BuyAndHoldXPeriodsStrategy:
    #     hold_period = strategy_params.get('hold_period', 30)
    #     logger.info(f"Creating BuyAndHoldXPeriodsStrategy (hold_period={hold_period})")
    #     return BuyAndHoldXPeriodsStrategy(hold_period=hold_period)
    # else:
    if True:    
        logger.info(f"Creating custom strategy: {strategy_class.__name__}")
        return strategy_class()


def create_risk_manager(
    config: ConfigManager, 
    logger: logging.Logger,
    is_live: bool = True
):
    """
    Create risk manager (live or mock) from config.
    
    Args:
        config: ConfigManager instance
        logger: Logger instance
        is_live: If True, create live RiskManager; else MockRiskManager
        
    Returns:
        RiskManager or MockRiskManager instance
    """
    risk_params = config.get('risk_management')
    risk_class = RiskManager if is_live else MockRiskManager
    
    max_position_size = risk_params.get('max_position_size', 0.1)
    stop_loss_pct = risk_params.get('stop_loss_pct', 0.05)
    
    mode = "Live" if is_live else "Mock"
    logger.info(f"Creating {mode} RiskManager (max_position={max_position_size}, stop_loss={stop_loss_pct})")
    
    return risk_class(
        max_position_size=max_position_size,
        stop_loss_pct=stop_loss_pct
    )


def create_forecast_manager(logger: logging.Logger) -> ForecastManager:
    """
    Create standard forecast manager with default parameters.
    
    Args:
        logger: Logger instance
        
    Returns:
        ForecastManager instance
    """
    logger.info("Creating ForecastManager with standard parameters")
    return ForecastManager(
        max_forecast=20.0,
        min_forecast=-20.0,
        max_allocation=1.0,
        min_allocation=-1.0,
        rebalance_threshold=0.05
    )


def main():
    """Run live trading bot."""
    config, logger = initialize_config_and_logger()
    if not config or not logger:
        sys.exit(1)

    logger.info("Starting live trading bot...")
    logger.info("-" * 80)

    # Get trading parameters from config
    test_mode = config.get('trading', 'test_mode', True)
    symbols = config.get('trading', 'symbols', ['BTCUSDT'])
    interval = config.get('trading', 'interval', 120)
    check_interval = config.get('trading', 'check_interval_seconds', 10)
    commission_rate = 0.001

    logger.info(f"Mode: {'TEST' if test_mode else 'LIVE'}")
    logger.info(f"Symbols: {', '.join(symbols)}")
    logger.info(f"Candle interval: {interval}s, Check interval: {check_interval}s")

    # Configure strategy and managers
    strategy = create_strategy(config, logger)
    risk_manager = create_risk_manager(config, logger, is_live=True)
    forecast_manager = create_forecast_manager(logger)

    # Initialize candle builder (callback set after bot creation)
    candle_builder = CandleBuilder(
        interval_seconds=interval,
        candle_completion_callback=None
    )

    # Initialize data manager with candle builder
    data_manager = DataManager(
        symbols=symbols,
        price_fetch_interval=check_interval,
        candle_builder=candle_builder
    )

    # Initialize execution and tracking
    performance_tracker = EnhancedPerformanceTracker(commission_rate)
    execution_handler = ExecutionHandler(performance_tracker)
    portfolio_info = PortfolioInfo()

    # Create trading bot
    bot = TradingBot(
        data_manager=data_manager,
        strategy=strategy,
        execution_handler=execution_handler,
        logger=logger,
        portfolio_info=portfolio_info,
        forecast_manager=forecast_manager,
        risk_manager=risk_manager,
        price_fetch_interval=check_interval,
        candle_interval_seconds=interval,
        test_mode=test_mode,
        symbols=symbols
    )

    # Set callback now that bot is created
    candle_builder.candle_completion_callback = bot._process_symbol_candle_completion

    logger.info("Bot initialized successfully. Starting main loop...")
    logger.info("="*80)
    
    try:
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (Ctrl+C)")
    except Exception as e:
        logger.error(f"Bot crashed with error: {e}", exc_info=True)
        sys.exit(1)


def simulate():
    """Run backtest simulation."""
    config, logger = initialize_config_and_logger()
    if not config or not logger:
        sys.exit(1)

    logger.info("Starting backtest simulation...")
    logger.info("-" * 80)

    # Get backtest parameters
    symbols = config.get('trading', 'symbols', ['BTCUSDT'])
    interval = config.get('trading', 'interval', 180)
    check_interval = config.get('trading', 'check_interval_seconds', 60)
    test_mode = config.get('trading', 'test_mode', True)
    initial_balance = 1000
    commission_rate = 0.001

    # Parse dates with fallback
    start_date_str = '2025-03-01'
    end_date_str = '2025-04-01'
    start_date = parse_date_safe(start_date_str, logger, default_days_back=60)
    end_date = parse_date_safe(end_date_str, logger, default_days_back=0)

    logger.info(f"Backtest period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    logger.info(f"Initial balance: {initial_balance} USDT")
    logger.info(f"Symbols: {', '.join(symbols)}")

    # Configure strategy and managers
    # strategy = AdvancedMovingAverageStrategy()
    strategy = AdvancedStrategy()
    logger.info(f"Using strategy: {strategy.__class__.__name__}")
    
    risk_manager = create_risk_manager(config, logger, is_live=False)
    forecast_manager = create_forecast_manager(logger)

    # Initialize backtest components
    data_manager = HistoricalDataManager(interval_seconds=interval)
    performance_tracker = EnhancedPerformanceTracker(commission_rate, initial_capital=initial_balance)
    portfolio_info = MockPortfolioInfo(
        initial_balance={'USDT': {'free': initial_balance, 'locked': 0}},
        commission_rate=commission_rate
    )

    portfolio_state_tracker = PortfolioStateTracker(output_dir="backtest_results")
    execution_handler = MockExecutionHandler(
        performance_tracker=performance_tracker,
        portfolio_info=portfolio_info
    )

    # Initialize backtester
    bot = BacktestEngine(
        data_manager=data_manager,
        strategy=strategy,
        execution_handler=execution_handler,
        logger=logger,
        portfolio_info=portfolio_info,
        portfolio_state_tracker=portfolio_state_tracker,
        forecast_manager=forecast_manager,
        risk_manager=risk_manager,
        performance_tracker=performance_tracker,
        price_fetch_interval=check_interval,
        candle_interval_seconds=interval,
        test_mode=test_mode,
        symbols=symbols,
        initial_capital=initial_balance
    )

    # Load data and run backtest
    try:
        logger.info("Loading historical data...")
        bot.load_data(start_date=start_date, end_date=end_date)

        logger.info("Running simulation...")
        logger.info("="*80)
        metrics = bot.simulate_on_loaded_data()

        # Log results
        logger.info("="*80)
        logger.info("BACKTEST COMPLETED")
        logger.info("="*80)
        
        report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backtest_report.html')
        logger.info(f"Performance report saved to: {report_path}")
        
    except Exception as e:
        logger.error(f"Backtest failed: {e}", exc_info=True)
        sys.exit(1)


def analyze_past_data():
    """Run backtest simulation."""
    config, logger = initialize_config_and_logger()
    if not config or not logger:
        sys.exit(1)

    logger.info("Starting backtest simulation...")
    logger.info("-" * 80)

    # Get backtest parameters
    symbols = config.get('trading', 'symbols', ['BTCUSDT'])
    interval = config.get('trading', 'interval', 180)
    check_interval = config.get('trading', 'check_interval_seconds', 60)
    test_mode = config.get('trading', 'test_mode', True)
    initial_balance = 1000
    commission_rate = 0.001

    # Parse dates with fallback
    start_date_str = '2024-06-01'
    end_date_str = '2024-12-01'
    start_date = parse_date_safe(start_date_str, logger, default_days_back=60)
    end_date = parse_date_safe(end_date_str, logger, default_days_back=0)

    logger.info(f"Backtest period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    logger.info(f"Initial balance: {initial_balance} USDT")
    logger.info(f"Symbols: {', '.join(symbols)}")

    # Configure strategy and managers
    # strategy = AdvancedMovingAverageStrategy()
    strategy = AdvancedStrategy()
    logger.info(f"Using strategy: {strategy.__class__.__name__}")
    
    risk_manager = create_risk_manager(config, logger, is_live=False)
    forecast_manager = create_forecast_manager(logger)

    # Initialize backtest components
    data_manager = HistoricalDataManager(interval_seconds=interval)
    performance_tracker = EnhancedPerformanceTracker(commission_rate, initial_capital=initial_balance)
    portfolio_info = MockPortfolioInfo(
        initial_balance={'USDT': {'free': initial_balance, 'locked': 0}},
        commission_rate=commission_rate
    )

    portfolio_state_tracker = PortfolioStateTracker(output_dir="backtest_results")
    execution_handler = MockExecutionHandler(
        performance_tracker=performance_tracker,
        portfolio_info=portfolio_info
    )

    # Initialize backtester
    bot = BacktestEngine(
        data_manager=data_manager,
        strategy=strategy,
        execution_handler=execution_handler,
        logger=logger,
        portfolio_info=portfolio_info,
        portfolio_state_tracker=portfolio_state_tracker,
        forecast_manager=forecast_manager,
        risk_manager=risk_manager,
        performance_tracker=performance_tracker,
        price_fetch_interval=check_interval,
        candle_interval_seconds=interval,
        test_mode=test_mode,
        symbols=symbols,
        initial_capital=initial_balance
    )

    # Load data and run backtest
    try:
        bot.load_data(start_date=start_date, end_date=end_date)
        price_data = bot.extract_historical_price_data()
        full_regimes, price_index = bot.performance_tracker.classify_full_history(price_data)
        bot.performance_tracker.plot_regime_chart(full_regimes, price_data)
    
    except Exception as e:
        logger.error(f"Backtest failed: {e}", exc_info=True)
        sys.exit(1)

def visualize_data():
    """Fetch and visualize historical data with continuity checks."""
    config, logger = initialize_config_and_logger()
    if not config or not logger:
        sys.exit(1)

    logger.info("Starting data visualization...")
    logger.info("-" * 80)

    # Data fetching parameters
    start_date = '2024-01-01'
    end_date = '2024-06-01'
    symbols = ['BTCUSDT', 'ETHUSDT']

    logger.info(f"Fetching data for: {', '.join(symbols)}")
    logger.info(f"Period: {start_date} to {end_date}")

    try:
        # Create data fetcher
        fetcher = HistoricalDataFetcher(
            start_date, end_date, symbols,
            interval='1m',
            exchange='binance',
            localStorage=True
        )

        # Get data
        data = fetcher.get_data()

        # Print statistics for each symbol
        for symbol in symbols:
            if symbol in data and not data[symbol].empty:
                # Check data continuity
                is_continuous, gaps = fetcher.validate_data_continuity(symbol)

                logger.info(f"\n{symbol} DATA SUMMARY")
                logger.info("-" * 40)
                logger.info(f"  Records: {len(data[symbol]):,}")
                logger.info(f"  Date range: {data[symbol]['timestamp'].min()} to {data[symbol]['timestamp'].max()}")
                logger.info(f"  Continuous: {'Yes' if is_continuous else 'No'}")

                if not is_continuous:
                    logger.warning(f"  Found {len(gaps)} gap(s) in data")
                    # Show first 5 gaps
                    for i, (gap_start, gap_end) in enumerate(gaps[:5]):
                        duration = (gap_end - gap_start).total_seconds() / 60
                        logger.warning(f"    Gap {i+1}: {gap_start} to {gap_end} ({duration:.0f} minutes)")
                    if len(gaps) > 5:
                        logger.warning(f"    ... and {len(gaps) - 5} more gap(s)")
            else:
                logger.error(f"No data available for {symbol}")
                
    except Exception as e:
        logger.error(f"Data visualization failed: {e}", exc_info=True)
        sys.exit(1)


def optimize_strategy():
    """Run strategy optimization using backtesting with parameter grid search."""
    config, logger = initialize_config_and_logger()
    if not config or not logger:
        sys.exit(1)

    logger.info("Starting strategy optimization...")
    logger.info("="*80)

    # Get optimization parameters
    symbols = config.get('trading', 'symbols', ['BTCUSDT'])
    interval = config.get('trading', 'interval', 180)
    check_interval = config.get('trading', 'check_interval_seconds', 60)
    test_mode = config.get('trading', 'test_mode', True)
    initial_balance = 1000
    commission_rate = 0.001

    # Parse dates
    start_date_str = '2025-01-01'
    end_date_str = '2025-03-01'
    start_date = parse_date_safe(start_date_str, logger, default_days_back=60)
    end_date = parse_date_safe(end_date_str, logger, default_days_back=0)

    logger.info(f"Optimization period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    logger.info(f"Symbols: {', '.join(symbols)}")

    # Configure managers (shared across all tests)
    risk_manager = create_risk_manager(config, logger, is_live=False)
    forecast_manager = create_forecast_manager(logger)
    data_manager = HistoricalDataManager(interval_seconds=interval)
    performance_tracker = EnhancedPerformanceTracker(commission_rate)
    portfolio_info = MockPortfolioInfo(
        initial_balance={'USDT': {'free': initial_balance, 'locked': 0}},
        commission_rate=commission_rate
    )
    execution_handler = MockExecutionHandler(
        performance_tracker=performance_tracker,
        portfolio_info=portfolio_info
    )

    # Define parameter grid for optimization
    short_window_range = [20, 50, 100]
    long_window_range = [100, 200, 300]
    
    total_combinations = sum(1 for s in short_window_range for l in long_window_range if s < l)
    logger.info(f"Testing {total_combinations} parameter combinations")
    logger.info("-" * 80)

    best_sharpe = -float('inf')
    best_params = {}
    test_count = 0

    # Grid search through parameter combinations
    try:
        for short_window in short_window_range:
            for long_window in long_window_range:
                # Skip invalid combinations
                if short_window >= long_window:
                    continue

                test_count += 1
                logger.info(f"Test {test_count}/{total_combinations}: short={short_window}, long={long_window}")

                # # Configure strategy with current parameters
                # strategy = SimpleMovingAverageStrategy(
                #     short_window=short_window,
                #     long_window=long_window
                # )
                strategy = AdvancedStrategy()

                # Initialize backtester
                bot = BacktestEngine(
                    data_manager=data_manager,
                    strategy=strategy,
                    execution_handler=execution_handler,
                    logger=logger,
                    portfolio_info=portfolio_info,
                    forecast_manager=forecast_manager,
                    risk_manager=risk_manager,
                    performance_tracker=performance_tracker,
                    price_fetch_interval=check_interval,
                    candle_interval_seconds=interval,
                    test_mode=test_mode,
                    symbols=symbols,
                    initial_capital=initial_balance
                )

                # Load data and run backtest
                bot.load_data(start_date=start_date, end_date=end_date)
                metrics = bot.simulate_on_loaded_data()

                # Track best strategy based on Sharpe ratio
                current_sharpe = metrics.get('sharpe_ratio', -float('inf'))
                logger.info(f"  Result: Sharpe={current_sharpe:.4f}")
                
                if current_sharpe > best_sharpe:
                    best_sharpe = current_sharpe
                    best_params = {
                        'short_window': short_window,
                        'long_window': long_window
                    }
                    logger.info(f"  ✓ NEW BEST: {best_params} with Sharpe={best_sharpe:.4f}")

        # Report optimization results
        logger.info("="*80)
        logger.info("OPTIMIZATION COMPLETED")
        logger.info("="*80)
        logger.info(f"Best parameters: {best_params}")
        logger.info(f"Best Sharpe ratio: {best_sharpe:.4f}")
        logger.info(f"Total tests run: {test_count}")
        
    except Exception as e:
        logger.error(f"Optimization failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Trading Bot Control - Execute various bot functions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py run_bot                    # Run live trading bot
  python main.py simulate                   # Run backtest simulation
  python main.py optimize_strategy          # Optimize strategy parameters
  python main.py visualize_data             # Visualize historical data
  python main.py get_value_portfolio        # Get current portfolio value
        """
    )
    
    parser.add_argument(
        "function",
        choices=[
            "run_bot",
            "sell_all_assets_to_target",
            "get_portfolio_converted",
            "get_value_portfolio",
            "visualize_data",
            "simulate",
            "optimize_strategy",
            "analyze_past_data"
        ],
        help="Specify the function to run"
    )
    
    args = parser.parse_args()

    # Route to appropriate function based on argument
    try:
        if args.function == "run_bot":
            main()

        elif args.function == "simulate":
            simulate()

        elif args.function == "optimize_strategy":
            optimize_strategy()

        elif args.function == "analyze_past_data":
            analyze_past_data()

        elif args.function == "sell_all_assets_to_target":
            ExecutionHandler().sell_all_assets_to_target('USDT')

        elif args.function == "get_portfolio_converted":
            coin_values = PortfolioInfo().get_portfolio_converted('USDT')
            print(coin_values)

        elif args.function == "get_value_portfolio":
            coin_values = PortfolioInfo().get_portfolio_converted('USDT')
            grand_usdt_total = sum(map(lambda coin_usdt_value: coin_usdt_value[1], coin_values))
            print(f"Total portfolio value: {grand_usdt_total:.2f} USDT")

        elif args.function == "visualize_data":
            visualize_data()
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        sys.exit(1)
