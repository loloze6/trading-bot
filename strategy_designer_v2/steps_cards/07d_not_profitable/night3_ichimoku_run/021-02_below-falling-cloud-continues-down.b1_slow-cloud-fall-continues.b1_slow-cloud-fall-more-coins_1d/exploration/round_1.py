def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily returns per window (mean over coins per day within window)
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    daily = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    byw = daily.groupby("w").agg(n=("book_return", "size"), book_mean=("book_return", "mean"),
                                 book_sum=("book_return", "sum"), coin_mean=("coin_return", "mean"))
    byw["book_sharpe"] = daily.groupby("w")["book_return"].apply(lambda x: x.mean() / x.std() * np.sqrt(365))
    byw["year"] = daily.groupby("w")["day"].apply(lambda x: pd.to_datetime(x).dt.year.iloc[len(x)//2])
    byw["w_num"] = [int(i[1:]) for i in byw.index]
    out["by_window"] = byw.sort_values("w_num").drop(columns="w_num")
    # grid cases in regime: features and forward 26-bar returns
    H = 26
    cases = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            hi = b["high"]; lo = b["low"]
            ret26p = b["close"] / b["close"].shift(26) - 1
            ret90p = b["close"] / b["close"].shift(90) - 1
            vol = np.log(b["close"]).diff().rolling(30).std()
            ma100 = b["close"].rolling(100, min_periods=60).mean()
            for i in range(0, len(b) - H, H):
                if b.loc[i, "regime"] != "trending":
                    continue
                cases.append(dict(coin=c, w=w, fwd=cl[i + H] / cl[i] - 1, r26=ret26p[i], r90=ret90p[i],
                                  vol=vol[i], above_ma=(cl[i] / ma100[i] - 1) if not np.isnan(ma100[i]) else np.nan,
                                  sf=b.loc[i, "debug_info.components.slow_fall.last_history_value"],
                                  year=pd.to_datetime(b.loc[i, "timestamp"]).year))
    C = pd.DataFrame(cases)
    out["n_cases"] = len(C)
    out["fwd_mean_t"] = f"mean {C.fwd.mean():.4f} t {stats.ttest_1samp(C.fwd, 0).statistic:.2f}"
    out["fwd_by_year"] = C.groupby("year")["fwd"].agg(["size", "mean", "median"])
    for col in ["r26", "r90", "vol", "above_ma", "sf"]:
        x = C.dropna(subset=[col])
        q = pd.qcut(x[col], 4, labels=False, duplicates="drop")
        g = x.groupby(q)["fwd"].agg(["size", "mean", "median"])
        g["lo"] = x.groupby(q)[col].min(); g["hi"] = x.groupby(q)[col].max()
        out["fwd_by_" + col] = g
    # trades
    T = pd.concat([t.assign(coin=c, w=w) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)])
    out["trades"] = f"n {len(T)} mean net {T.net_profit_loss_percent.mean():.3f} win {(T.net_profit_loss_percent>0).mean():.2f} sides {T.side.value_counts().to_dict()}"
    return out
