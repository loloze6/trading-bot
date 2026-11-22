def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        # coin drift over all windows, non-overlapping 10-day
        fw_all = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            fw_all += list(c[idx + H] / c[idx] - 1)
        drift = np.nanmean(fw_all) if fw_all else np.nan
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; hi = b["high"]; lo = b["low"]
            r30 = c / c.shift(30) - 1
            rhi = hi.rolling(31).max(); rlo = lo.rolling(31).min()
            rng = rhi - rlo
            nmr = (c - c.shift(30)) / rng
            pos = (c - (rhi + rlo) / 2) / rng
            r1 = c.pct_change()
            vol = r1.rolling(30).std()
            r5 = c / c.shift(5) - 1
            fwd = c.shift(-H) / c - 1
            n = len(b)
            for t in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, nmr=nmr[t], pos=pos[t], r30=r30[t], r5=r5[t],
                                 vol=vol[t], r1=r1[t], ex=fwd[t] - drift,
                                 fc=b["forecast"][t], wd=pd.Timestamp(b["timestamp"][t]).weekday()))
            # daily next-day after large move
            nx = c.shift(-1) / c - 1
            for t in range(31, n - 1):
                daily.append(dict(coin=coin, r1=r1[t], z=r1[t] / vol[t] if vol[t] > 0 else np.nan,
                                  nx=nx[t], nmr=nmr[t], wd=pd.Timestamp(b["timestamp"][t+1]).weekday()))
    g = pd.DataFrame(rows).dropna(subset=["nmr", "ex"])
    d = pd.DataFrame(daily).dropna()
    def summ(df, key):
        a = df.groupby(key, observed=True)["ex"].agg(["count", "mean", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a.round(4)
    out = {}
    g["nmr_q"] = pd.qcut(g["nmr"], 10, labels=False)
    out["10d excess by signed NMR decile"] = summ(g, "nmr_q")
    flat = g[g["nmr"].abs() < 0.5].copy()
    flat["pos_q"] = pd.qcut(flat["pos"], 5, labels=False)
    out["flat (|nmr|<.5): 10d excess by range position quintile"] = summ(flat, "pos_q")
    up = g[g["nmr"] >= 0.5].copy()
    up["vol_t"] = pd.qcut(up["vol"], 3, labels=False)
    out["clean up: by 30d vol tercile"] = summ(up, "vol_t")
    up["r5_t"] = pd.qcut(up["r5"], 3, labels=False)
    out["clean up: by 5d return tercile"] = summ(up, "r5_t")
    dn = g[g["nmr"] <= -0.5].copy()
    dn["r30_t"] = pd.qcut(dn["r30"], 3, labels=False)
    out["clean down: by 30d return tercile"] = summ(dn, "r30_t")
    d["zq"] = pd.qcut(d["z"], 10, labels=False)
    a = d.groupby("zq")["nx"].agg(["count", "mean", "std"]); a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["next-day return by today's vol-scaled move decile"] = a.round(5)
    a = d.groupby("wd")["nx"].agg(["count", "mean", "std"]); a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["daily return by weekday"] = a.round(5)
    # book
    bk = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd[["book_return", "coin_return"]].copy(); x["coin"] = coin
            bk.append(x)
    bk = pd.concat(bk).dropna()
    bk["inmkt"] = bk["book_return"].abs() > 1e-9
    out["book daily by in/out"] = bk.groupby("inmkt")[["book_return", "coin_return"]].agg(["count", "mean"]).round(5)
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    tr = pd.concat(tr)
    tr["fq"] = pd.qcut(tr["entry_forecast"], 4, labels=False, duplicates="drop")
    a = tr.groupby("fq")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades net pnl by entry forecast quartile"] = a.round(3)
    tr["dq"] = pd.qcut(tr["duration_minutes"], 4, labels=False, duplicates="drop")
    out["trades net pnl by duration quartile"] = tr.groupby("dq")["net_profit_loss_percent"].agg(["count", "mean", "median"]).round(3)
    return out
