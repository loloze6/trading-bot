# Review of the backtests in this folder

Step 4 (now accepting several folds) on the 6 plans of the full-data run: 6 coins (BTC, ETH, LTC, XMR, XRP, ZEC), folds A to D, 24 windows each, daily bars. 141 of 144 coin-windows per plan: the engine refused 1 XMR and 2 XRP windows at its warm-up check (fewer daily bars before the window than the 200-day average needs: a gap in the coins' history). About 25 minutes, 37 MB. The run and its review: `../../../FULL_DATA_RUN.md`.
