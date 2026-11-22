def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    out = {}
    rows = []
    book_rows = []
    trade_rows = []
    for coin, wins in data["bars"].items():
        # drift: non-overlapping 18-bar returns over all windows
        grid = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            grid.extend(list(c[idx + H] / c[idx] - 1))
        grid = np.array(grid)
        drift, usual = np.nanmean(grid), np.nanstd(grid)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; v = b["volume"]
            r1 = c.pct_change()
            up4 = (r1 > 0).rolling(4).sum() == 4
            dn4 = (r1 < 0).rolling(4).sum() == 4
            fade = v.rolling(2).mean() < v.rolling(4).mean()
            vol = r1.rolling(180).std()
            sg = (c / c.shift(4) - 1) / vol
            fwd = c.shift(-H) / c - 1
            n = len(b)
            cell = np.arange(n) // H
            df = pd.DataFrame({"up4": up4, "dn4": dn4, "fade": fade, "sg": sg,
                               "fwd": fwd, "cell": cell, "fc": b["forecast"],
                               "alloc": b["postRebalance_current_allocation"],
                               "r1next": c.shift(-1) / c - 1})
            df["coin"] = coin; df["win"] = w
            df["unus"] = df["fwd"] - drift
            df["strength"] = df["unus"] / usual
            df["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(df)
        tr = data["trades"][coin]
        for w, t in tr.items():
            if len(t):
                tt = t.copy(); tt["coin"] = coin; trade_rows.append(tt)
    A = pd.concat(rows, ignore_index=True)
    A = A.dropna(subset=["fwd", "sg"])

    def summ(sub, sign):
        # first per cell
        s = sub.groupby(["coin", "win", "cell"]).head(1)
        x = sign * s["unus"]; tot = sign * s["fwd"]
        return pd.Series({"n": len(x), "unusual_mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "total_mean": tot.mean(), "strength": (sign * s["strength"]).mean()})
    res = {}
    res["up4_fade_short"] = summ(A[A.up4 & A.fade], -1)
    res["up4_risevol_short"] = summ(A[A.up4 & ~A.fade], -1)
    res["dn4_fade_long"] = summ(A[A.dn4 & A.fade], 1)
    res["dn4_risevol_long"] = summ(A[A.dn4 & ~A.fade], 1)
    res["all_bars_short"] = summ(A, -1)
    out["situations"] = pd.DataFrame(res).T

    # grading by sg quartile within up4 & fade
    S = A[A.up4 & A.fade].groupby(["coin", "win", "cell"]).head(1).copy()
    S["q"] = pd.qcut(S["sg"], 4, labels=False)
    out["up4fade_by_sg_quartile"] = S.groupby("q").agg(n=("unus", "size"), sg=("sg", "mean"),
        short_unusual=("unus", lambda x: -x.mean()), short_total=("fwd", lambda x: -x.mean()))
    D = A[A.dn4 & A.fade].groupby(["coin", "win", "cell"]).head(1).copy()
    D["q"] = pd.qcut(D["sg"], 4, labels=False)
    out["dn4fade_by_sg_quartile"] = D.groupby("q").agg(n=("unus", "size"), sg=("sg", "mean"),
        long_unusual=("unus", "mean"), long_total=("fwd", "mean"))
    out["up4fade_by_coin_short_unusual"] = S.groupby("coin")["unus"].agg(lambda x: -x.mean())
    out["up4fade_by_year_short_unusual"] = S.groupby("year")["unus"].agg(["size", lambda x: -x.mean()])

    # book: active share, gain split
    full = pd.concat(rows, ignore_index=True)
    act = full[full["alloc"].abs() > 1e-9]
    out["active_share_bars"] = float(len(act) / len(full))
    out["active_in_situation_share"] = float((act.up4 & act.fade).mean())
    out["forecast_nonzero_share"] = float((full.fc != 0).mean())
    out["fc_nonzero_in_situation"] = float(((full.fc != 0) & full.up4 & full.fade).sum() / max((full.fc != 0).sum(), 1))
    out["mean_alloc_when_active"] = float(act["alloc"].mean())
    # bar gain
    full["gain"] = full["alloc"] * full["r1next"]
    out["mean_bar_gain_active"] = float(full.loc[full.alloc.abs() > 1e-9, "gain"].mean())

    T = pd.concat(trade_rows, ignore_index=True)
    out["trades"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
        dur_h=("duration_minutes", lambda x: x.mean() / 60))
    # days
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, win=w))
    Dd = pd.concat(dd)
    out["days_book_vs_coin"] = pd.Series({"book_mean": Dd.book_return.mean(), "coin_mean": Dd.coin_return.mean()})
    return out
