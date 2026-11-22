def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []; drows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20, min_periods=20).std().shift(1)
            z = r1 / sd20
            ret20 = c / c.shift(20) - 1
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "z": z, "ret20": ret20, "sd20": sd20,
                               "fwd": fwd, "fwd1": fwd1, "reg": b["regime"].values,
                               "fc": b["forecast"].astype(float), "wd": ts.dt.weekday,
                               "year": ts.dt.year, "pos": np.arange(len(b))})
            drows.append(df)
            rows.append(df[df["pos"] % H == 0])
    g = pd.concat(rows); a = pd.concat(drows)
    g = g.dropna(subset=["fwd"])
    drift = g.groupby("coin")["fwd"].mean(); usd = g.groupby("coin")["fwd"].std()
    g["un"] = g["fwd"] - g["coin"].map(drift)
    g["st"] = g["un"] / g["coin"].map(usd)
    g["tr"] = np.where(g["reg"] == "trending", "up90", "down90")
    def summ(x, col="un"):
        x = x.dropna()
        n = len(x); m = x.mean(); s = x.std()
        return pd.Series({"n": n, "mean": m, "t": m / (s / np.sqrt(n)) if n > 2 and s > 0 else np.nan})
    out = {}
    gz = g.dropna(subset=["z"]).copy()
    gz["zb"] = pd.cut(gz["z"], [-99, -2, -1, 0, 1, 2, 99])
    out["10d unusual by regime x z"] = gz.groupby(["tr", "zb"], observed=True)["un"].apply(summ).unstack()
    out["10d unusual by regime"] = g.groupby("tr")["un"].apply(summ).unstack()
    gr = g.dropna(subset=["ret20"]).copy()
    gr["q"] = gr.groupby("coin")["ret20"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["10d unusual by ret20 quintile"] = gr.groupby("q")["un"].apply(summ).unstack()
    out["10d unusual by ret20 quintile x regime"] = gr.groupby(["tr", "q"])["un"].apply(summ).unstack()
    gv = g.dropna(subset=["sd20"]).copy()
    gv["vq"] = gv.groupby("coin")["sd20"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["10d unusual by vol quintile"] = gv.groupby("vq")["un"].apply(summ).unstack()
    # daily
    a = a.dropna(subset=["fwd1"]).copy()
    a["u1"] = a["fwd1"] - a["coin"].map(a.groupby("coin")["fwd1"].mean())
    a["wd_next"] = (a["wd"] + 1) % 7
    out["next-day unusual by weekday of next day"] = a.groupby("wd_next")["u1"].apply(summ).unstack()
    az = a.dropna(subset=["z"]).copy()
    az["zb"] = pd.cut(az["z"], [-99, -2, -1, 0, 1, 2, 99])
    out["next-day unusual by z"] = az.groupby("zb", observed=True)["u1"].apply(summ).unstack()
    out["10d unusual by year"] = g.groupby("year")["un"].apply(summ).unstack()
    # forecast on grid
    gf = g[g["fc"] > 0].copy()
    gf["fb"] = pd.cut(gf["fc"], [0, 5, 10, 15, 20.1])
    out["10d unusual by forecast (grid, fc>0)"] = gf.groupby("fb", observed=True)["un"].apply(summ).unstack()
    # trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values() if len(t)])
    tr["fb"] = pd.cut(tr["entry_forecast"].astype(float), [-0.1, 5, 10, 15, 20.1])
    out["trades by entry forecast"] = tr.groupby("fb", observed=True)["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades by coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    # book days
    d = pd.concat([x.assign(coin=c, w=w) for c, ws in data["days"].items() for w, x in ws.items()])
    bk = d.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    q = bk["book_return"].quantile([0.02, 0.98])
    out["book extreme days"] = pd.DataFrame({
        "n": [(bk.book_return <= q.iloc[0]).sum(), (bk.book_return >= q.iloc[1]).sum()],
        "sum_book": [bk.book_return[bk.book_return <= q.iloc[0]].sum(), bk.book_return[bk.book_return >= q.iloc[1]].sum()],
        "total_book_sum": [bk.book_return.sum()] * 2}, index=["worst2%", "best2%"])
    return out
