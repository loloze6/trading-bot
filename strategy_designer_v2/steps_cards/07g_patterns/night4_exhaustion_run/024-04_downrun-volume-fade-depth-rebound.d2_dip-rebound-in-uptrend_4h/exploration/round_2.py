def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    for H in (18, 6):
        rows = []
        for coin, wins in data["bars"].items():
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"].astype(float); v = b["volume"].astype(float)
                r = c.pct_change()
                absm = r.abs().rolling(180, min_periods=90).mean()
                r6 = (c / c.shift(6) - 1) / absm
                r36 = (c / c.shift(36) - 1) / absm
                vr6 = np.log(v.rolling(6).mean() / v.rolling(180, min_periods=60).mean().shift(6))
                r180 = c / c.shift(180) - 1
                ts = pd.to_datetime(b["timestamp"])
                fwd = c.shift(-H) / c - 1
                for i in range(0, len(b), H):
                    if i + H >= len(b): continue
                    rows.append(dict(coin=coin, w=w, fwd=fwd[i], r6=r6[i], r36=r36[i], vr6=vr6[i],
                                     r180=r180[i], wd=ts[i].weekday(), yr=ts[i].year))
        d = pd.DataFrame(rows)
        d["un"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
        d = d.dropna(subset=["un"])
        def grp(x, key, q):
            x = x.dropna(subset=[key])
            o = x.groupby(pd.qcut(x[key], q, duplicates="drop"))["un"].agg(["mean", "count", "std"])
            o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
            return o[["mean", "count", "t"]].round(4)
        def sp(x, key):
            x = x.dropna(subset=[key, "un"])
            rho, p = stats.spearmanr(x[key], x["un"])
            return f"rho={rho:.4f} p={p:.4f} n={len(x)}"
        if H == 18:
            dn = d[d.r6 < 0]; up = d[d.r6 > 0]
            big_dn = d[d.r6 < d.r6.quantile(0.2)]
            big_up = d[d.r6 > d.r6.quantile(0.8)]
            out["H18 big 1d fall: un by vol ratio q"] = grp(big_dn, "vr6", 3)
            out["H18 big 1d fall: spearman vr6"] = sp(big_dn, "vr6")
            out["H18 big 1d rise: un by vol ratio q"] = grp(big_up, "vr6", 3)
            out["H18 big 1d rise: spearman vr6"] = sp(big_up, "vr6")
            out["H18 r36>0: un by r36 q"] = grp(d[d.r36 > 0], "r36", 5)
            out["H18 r36>0 spearman"] = sp(d[d.r36 > 0], "r36")
            out["H18 r36 top quintile by year"] = d[d.r36 > d.r36.quantile(0.8)].groupby("yr")["un"].agg(["mean", "count"]).round(4)
            out["H18 r36 top quintile by coin"] = d[d.r36 > d.r36.quantile(0.8)].groupby("coin")["un"].agg(["mean", "count"]).round(4)
            s = d[d.wd == 6]
            out["H18 sunday-start by year"] = s.groupby("yr")["un"].agg(["mean", "count"]).round(4)
            out["H18 sunday-start by coin"] = s.groupby("coin")["un"].agg(["mean", "count"]).round(4)
        else:
            out["H6 r6 q"] = grp(d, "r6", 10)
            out["H6 r6<0 spearman"] = sp(d[d.r6 < 0], "r6")
            out["H6 r6>0 spearman"] = sp(d[d.r6 > 0], "r6")
            out["H6 weekday"] = d.groupby("wd")["un"].agg(["mean", "count"]).round(4)
    # book around biggest days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["w"] = w; dd.append(x)
    D = pd.concat(dd)
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index().dropna()
    bk["gain_mkt"] = bk["book_return"]
    q = bk["book_return"].quantile([0.02, 0.98]).values
    out["book worst 2% days: mean book, coin"] = bk[bk.book_return <= q[0]][["book_return", "coin_return"]].mean().round(4)
    out["book best 2% days: mean book, coin"] = bk[bk.book_return >= q[1]][["book_return", "coin_return"]].mean().round(4)
    bk["wd"] = pd.to_datetime(bk["day"]).dt.weekday
    out["coin daily ret weekday t"] = bk.groupby("wd")["coin_return"].agg(lambda s: s.mean() / (s.std() / np.sqrt(len(s)))).round(3)
    return out
