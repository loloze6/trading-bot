"""Trading Bot entry point — CLI dispatcher only."""

import argparse
import sys

from core.launcher import Launcher

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Trading Bot Control - Execute various bot functions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py run_bot                    # Run live trading bot
  python main.py simulate                   # Run backtest simulation
  python main.py visualize_data             # Visualize historical data
  python main.py get_value_portfolio        # Get current portfolio value
        """,
    )
    parser.add_argument(
        "function",
        choices=[
            "run_bot",
            "get_portfolio_converted",
            "get_value_portfolio",
            "visualize_data",
            "simulate",
            "analyze_past_data",
        ],
        help="Specify the function to run",
    )

    args = parser.parse_args()

    try:
        launcher = Launcher()
        getattr(launcher, args.function)()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        sys.exit(1)
