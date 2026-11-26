The data the workflow can test an idea on (Kraken; folds by year; each fold has its windows). A coin is run only in
the windows where it has data; the others are skipped.

**Bar sizes** (2026-11-18): the files hold daily and hourly bars for the 19 coins (daily to 2026-11-17, hourly to
2025-12-31). Any other bar size is built from the largest of them that divides it evenly: 4h, 2h or 12h from the
hourly bars (`trading-bot/data/coverage.py`, `data_bar`). The daily files are the hourly bars added up by day (measured:
identical on 2,921 days for each default coin).

The coins with data in each fold (the same on daily and hourly bars):

- All four folds A, B, C and D: BTC, ETH, LTC, XMR, XRP, ZEC (the default data).
- Folds A and D, and part of B and C: ADA, DOGE, LINK, TRX, UNI, AAVE (in B and C: ADA 8 of 12 windows, DOGE 5,
  LINK 6, TRX 4, UNI 2, AAVE 1).
- Folds A and D only: AVAX, SOL, INJ, NEAR (NEAR in fold A: its last window only).
- Fold D only: SUI, TAO, ONDO.
