def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    grid = []; daily = []; mk = []
    for c in bars:
        allr = pd.concat([days[c][w]["coin_return"] for w in days[c]]).dropna()
        mu = allr.mean()
        for w, b in bars[c].items():
            cl = b["close"].reset_index(drop=True)
            r720 = cl.pct_change(720)
            r1 = cl.pct_change()
            vr = r1.rolling(72).std() / r1.rolling(720).std()
            f = b["forecast"].reset_index(drop=True)
            for i in range(0, len(cl) - 72, 72):
                grid.append((c, w, f[i], cl[i + 72] / cl[i] - 1, r720[i], vr[i]))
            # daily book with state at day's start
            d = days[c][w].copy()
            b2 = b.assign(day=pd.to_datetime(b["timestamp"]).dt.floor("D").values, r720=r720.values, vr=vr.values)
            last = b2.groupby("day")[["r720", "vr", "postRebalance_current_allocation"]].last().shift(1)
            d["day"] = pd.to_datetime(d["day"])
            d = d.merge(last, left_on="day", right_index=True, how="left")
            d["coin"] = c
            daily.append(d)
            mk.append((d["postRebalance_current_allocation"].fillna(0) * mu).mean())
    g = pd.DataFrame(grid, columns=["coin", "win", "f", "fwd", "r720", "vr"])
    g["exc"] = g.fwd - g.groupby("coin").fwd.transform("mean")
    ga = g[g.f > 0].dropna().copy()
    def slope(x):
        if len(x) < 30: return pd.Series({"n": len(x)})
        r = stats.linregress(x.f, x.exc)
        return pd.Series({"n": len(x), "slope": r.slope, "t": r.slope / r.stderr, "mean_exc": x.exc.mean()})
    ga["tr"] = np.where(ga.r720 > 0, "up30", "down30")
    out["slope_by_30d_sign"] = ga.groupby("tr").apply(slope)
    ga["vrq"] = pd.qcut(ga.vr.rank(method="first"), 3, labels=["calm", "mid", "hot"])
    out["slope_by_volratio"] = ga.groupby("vrq").apply(slope)
    out["exc_tr_x_vr"] = ga.groupby(["tr", "vrq"]).exc.agg(["mean", "count"]).unstack()
    D = pd.concat(daily).dropna(subset=["book_return"])
    D["tr"] = np.where(D.r720 > 0, "up30", np.where(D.r720 <= 0, "down30", "na"))
    out["book_daily_by_30d_sign"] = D.groupby("tr")[["book_return", "coin_return", "postRebalance_current_allocation"]].agg(["mean", "count"]).round(5)
    out["market_part_mean"] = float(np.mean(mk))
    out["book_mean"] = float(D.book_return.mean())
    # worst windows: state shares
    ww = D.groupby("win").agg(book=("book_return", "mean"), up_share=("r720", lambda x: (x > 0).mean()), coin=("coin_return", "mean"))
    out["window_book_vs_upshare_corr"] = float(ww[["book", "up_share"]].corr().iloc[0, 1])
    out["worst6_windows"] = ww.sort_values("book").head(6).round(4)
    return out
