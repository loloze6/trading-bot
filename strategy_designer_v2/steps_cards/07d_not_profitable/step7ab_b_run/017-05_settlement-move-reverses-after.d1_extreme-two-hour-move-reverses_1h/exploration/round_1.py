def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []      # per-case rows on grids
    book = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(20).std()
            ts = pd.to_datetime(df["timestamp"], utc=True)
            hour = ts.dt.hour.values
            volpct = r1.rolling(24*30, min_periods=24*10).std()
            for L in [2, 24, 72]:
                past = c / c.shift(L) - 1
                z = past / (vol * np.sqrt(L))
                for h in [24, 72, 168]:
                    fwd = c.shift(-h) / c - 1
                    idx = np.arange(0, len(df), h)
                    sub = pd.DataFrame({"coin": coin, "w": w, "L": L, "h": h,
                                        "z": z.values[idx], "fwd": fwd.values[idx],
                                        "hour": hour[idx], "vol30": volpct.values[idx],
                                        "fc": df["forecast"].values[idx]})
                    rows.append(sub)
            alloc = df["postRebalance_current_allocation"].astype(float)
            gross = alloc * (c.shift(-1) / c - 1)
            fee = (df["total_portfolio_value"] - df["postRebalance_total_value"]) / df["total_portfolio_value"]
            book.append(pd.DataFrame({"coin": coin, "gross": [gross.sum()], "fee": [fee.sum()],
                                      "n": [len(df)], "absalloc": [alloc.abs().mean()],
                                      "turnover": [(alloc - df["previous_allocation"]).abs().sum()]}))
    R = pd.concat(rows, ignore_index=True).dropna(subset=["z", "fwd"])
    drift = R.groupby(["coin", "L", "h"])["fwd"].transform("mean")
    R["unus"] = -np.sign(R["z"]) * (R["fwd"] - drift)   # fade direction
    R["tot"] = -np.sign(R["z"]) * R["fwd"]
    R["az"] = R["z"].abs()
    out = {}
    def summ(g):
        n = len(g); m = g["unus"].mean(); s = g["unus"].std()
        return pd.Series({"n": n, "unus_bps": m*1e4, "tot_bps": g["tot"].mean()*1e4,
                          "t": m/(s/np.sqrt(n)) if n > 2 else np.nan})
    # fade by |z| quintile, for each lookback and horizon
    R["q"] = R.groupby(["L", "h"])["az"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["fade_by_L_h_zquint"] = R.groupby(["L", "h", "q"]).apply(summ).reset_index()
    # top quintile of 2h move: by settlement hour vs other, h=24
    t = R[(R.L == 2) & (R.h == 24)].copy()
    t["settle"] = t["hour"].isin([0, 8, 16])
    out["2h_top_by_settle"] = t[t.q == 4].groupby("settle").apply(summ)
    # top quintile, by vol tercile (bps scale with vol)
    t["vt"] = pd.qcut(t["vol30"], 3, labels=False)
    out["2h_top_by_voltercile"] = t[t.q == 4].groupby("vt").apply(summ)
    out["2h_top_by_coin"] = t[t.q == 4].groupby("coin").apply(summ)
    B = pd.concat(book).groupby("coin").sum()
    B["gross_per_day_bps"] = B["gross"] / B["n"] * 24 * 1e4
    B["fee_per_day_bps"] = B["fee"] / B["n"] * 24 * 1e4
    B["turnover_per_day"] = B["turnover"] / B["n"] * 24
    B["absalloc"] = B["absalloc"] / 24
    out["book_gross_vs_fee"] = B[["gross_per_day_bps", "fee_per_day_bps", "turnover_per_day", "absalloc"]]
    return out
