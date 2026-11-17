import pandas as pd, numpy as np

def explore(data):
    bars = data["bars"]
    rows = []
    gridrows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.iloc[0]
            pos = df["forecast"] > 0
            rows.append({"coin": coin, "window": w, "year": yr, "bars": n,
                         "pos_bars": int(pos.sum())})
            c = df["close"].values
            for i in range(0, n - 30, 30):
                r = c[i + 30] / c[i] - 1
                gridrows.append({"coin": coin, "window": w, "year": yr,
                                 "f": df["forecast"].iloc[i], "r": r})
    R = pd.DataFrame(rows); G = pd.DataFrame(gridrows)
    G["pos"] = G["f"] > 0
    mean_r = G.groupby("coin")["r"].transform("mean")
    G["ex"] = G["r"] - mean_r
    P = G[G.pos]
    by_coin = R.groupby("coin")[["bars", "pos_bars"]].sum()
    by_coin["pos_share"] = by_coin.pos_bars / by_coin.bars
    by_coin["grid"] = G.groupby("coin").size()
    by_coin["grid_pos"] = G.groupby("coin")["pos"].sum()
    by_year = R.groupby("year")[["bars", "pos_bars"]].sum()
    by_year["grid"] = G.groupby("year").size()
    by_year["grid_pos"] = G.groupby("year")["pos"].sum()
    win = R.groupby("window")[["bars", "pos_bars"]].sum()
    # break-bar runs: how many distinct episodes
    eps = 0
    for coin, ws in bars.items():
        for w, df in ws.items():
            p = (df["forecast"] > 0).astype(int).values
            eps += int(((p[1:] == 1) & (p[:-1] == 0)).sum() + p[0])
    # all-bar (overlapping) cases, for scale only
    allpos = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            c = df["close"].values; f = df["forecast"].values
            for i in range(len(df) - 30):
                if f[i] > 0:
                    allpos.append(c[i + 30] / c[i] - 1)
    allpos = np.array(allpos)
    summ = {"windows_mean_len": R.bars.mean(), "total_bars": R.bars.sum(),
            "pos_bars": R.pos_bars.sum(), "grid_total": len(G),
            "grid_pos": int(G.pos.sum()), "episodes": eps,
            "pos_ex_mean": P.ex.mean(), "pos_ex_std": P.ex.std(),
            "all_grid_r_std": G.r.std(), "pos_f_mean": P.f.mean(),
            "pos_f_std": P.f.std(), "pos_f_max": P.f.max(),
            "overlap_pos_n": len(allpos), "overlap_pos_mean": allpos.mean() if len(allpos) else np.nan}
    return {"by_coin": by_coin, "by_year": by_year, "by_window": win,
            "summary": pd.Series(summ)}
