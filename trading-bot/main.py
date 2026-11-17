"""Trading Bot entry point — CLI dispatcher only."""

import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Trading Bot Control - Execute various bot functions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py live_check --symbol BTCUSD                       # Kraken Futures reachable? account (read-only)
  python main.py run_live --run NAME --strategy PATH --symbol BTCUSD   # start a live run (new folder)
  python main.py run_live --run NAME                              # restart an existing live run
  python main.py simulate                                         # Run backtest simulation
  python main.py visualize_data                                   # Visualize historical data
        """,
    )
    parser.add_argument(
        "function",
        choices=[
            "run_live",
            "live_check",
            "visualize_data",
            "simulate",
            "analyze_past_data",
        ],
        help="Specify the function to run",
    )
    parser.add_argument("--run", help="run_live: the run's name (folder live_runs/<name>/)")
    parser.add_argument("--strategy", help="run_live: strategy config file (first start of a run)")
    parser.add_argument("--symbol", help="run_live / live_check: coin as in the research, e.g. BTCUSD")

    args = parser.parse_args()

    try:
        if args.function == "run_live":
            if not args.run:
                parser.error("run_live needs --run NAME")
            from live.runner import start
            start(args.run, args.strategy, args.symbol)
        elif args.function == "live_check":
            from live.runner import check
            check(args.symbol or "BTCUSD")
        else:
            from core.launcher import Launcher
            launcher = Launcher()
            getattr(launcher, args.function)()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        sys.exit(1)
