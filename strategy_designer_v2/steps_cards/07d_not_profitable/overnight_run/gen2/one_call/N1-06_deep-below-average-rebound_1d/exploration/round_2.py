def explore(data):
    import numpy as np, pandas as pd
    out = {}
    def st(x):
        x = pd.Series(x).dropna(); n = len(x)
        if n < 2: return pd.Series({"n": n, "mean": np.nan, "t": np.nan})
        m = x.mean(); s = x.std()
        return pd.Series({"n": n, "mean": m, "t": m / (s / np.sqrt(n)) if s > 0 else np.nan})
    # book days
    dl = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = c; d["win"] = w
            d["year"] = pd.to_datetime(d["day"]).dt.year
            dl.append(d)
    D = pd.concat(dl, ignore_index=True).dropna(subset=["book_return", "coin_return"])
    D["inpos"] = D["book_return"].abs() > 1e-9
    D["cdir"] = np.where(D["coin_return"] > 0, "coin_up", "coin_down")
    out["book_by_year"] = D.groupby("year").agg(book_sum=("book_return", "sum"), coin_sum=("coin_return", "sum"), inpos=("inpos", "mean"))
    out["book_by_coindir_inpos"] = D[D["inpos"]].groupby("cdir")["book_return"].agg(["size", "mean", "sum"])
    # worst windows per coin by book return
    W = D.groupby(["coin", "win"]).agg(book=("book_return", "sum"), coin=("coin_return", "sum")).reset_index()
    out["window_book_dist"] = W["book"].describe()
    out["corr_window_book_coin"] = float(W["book"].corr(W["coin"]))
    out["windows_book_lt_m10pct_share_coin_neg"] = float((W[W["book"] < -0.10]["coin"] < 0).mean())
    # bar-level conditions
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True); cl = pd.Series(b["close"].values.astype(float))
            fwd = cl.shift(-10) / cl - 1
            r1 = cl.pct_change()
            ret5 = cl / cl.shift(5) - 1
            ret10 = cl / cl.shift(10) - 1
            hi20 = cl.rolling(20).max(); lo20 = cl.rolling(20).min()
            pos20 = (cl - lo20) / (hi20 - lo20)
            vol = r1.rolling(20).std(); volm = vol.rolling(200, min_periods=50).median()
            below = (b["forecast"].values > 0).astype(int)
            run = pd.Series(below).groupby((pd.Series(below) != pd.Series(below).shift()).cumsum()).cumcount() + 1
            run = np.where(below == 1, run, 0)
            ma200 = cl.rolling(200, min_periods=200).mean()
            slope200 = ma200 / ma200.shift(20) - 1
            rows.append(pd.DataFrame({"coin": c, "i": np.arange(len(b)), "fc": b["forecast"].values, "fwd": fwd,
                "ret5": ret5, "ret10": ret10, "pos20": pos20, "hivol": vol > volm, "run": run, "slope200": slope200}))
    B = pd.concat(rows, ignore_index=True)
    G = B[(B["i"] % 10 == 0) & B["fwd"].notna()].copy()
    G["ex"] = G["fwd"] - G.groupby("coin")["fwd"].transform("mean")
    A = G[G["fc"] > 0].copy()
    A["ret10s"] = np.where(A["ret10"] > 0, "up", "down")
    out["active_by_ret10"] = A.groupby("ret10s")["ex"].apply(st).unstack()
    A["p20"] = pd.cut(A["pos20"], [-0.01, 0.2, 0.5, 0.8, 1.01])
    out["active_by_pos20"] = A.groupby("p20", observed=True)["ex"].apply(st).unstack()
    A["runb"] = pd.cut(A["run"], [0, 20, 60, 150, 2000])
    out["active_by_run_days"] = A.groupby("runb", observed=True)["ex"].apply(st).unstack()
    A["sl"] = pd.cut(A["slope200"], [-1, -0.10, -0.03, 0, 1])
    out["active_by_sma200_slope20"] = A.groupby("sl", observed=True)["ex"].apply(st).unstack()
    Dp = A[A["fc"] >= 5].copy()
    Dp["cell"] = np.where(Dp["hivol"], "hv", "lv") + "_" + np.where(Dp["ret10"] > 0, "up", "dn")
    out["deep_by_vol_ret10"] = Dp.groupby("cell")["ex"].apply(st).unstack()
    out["deep_by_run"] = Dp.groupby(pd.cut(Dp["run"], [0, 30, 90, 2000]), observed=True)["ex"].apply(st).unstack()
    return out
