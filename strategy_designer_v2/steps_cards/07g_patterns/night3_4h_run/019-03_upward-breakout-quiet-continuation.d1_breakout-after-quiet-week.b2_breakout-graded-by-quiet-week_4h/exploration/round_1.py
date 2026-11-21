import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 18
    rows = []
    hourrows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(b)
            if n < 60: continue
            ph = hi.shift(1).rolling(12).max(); pl = lo.shift(1).rolling(12).min()
            rng = (hi - lo) / c
            atr = rng.rolling(42, min_periods=20).mean()
            quiet = rng.rolling(360, min_periods=180).mean() / rng.rolling(42).mean()
            fwd = c.shift(-H) / c - 1
            df = pd.DataFrame({
                "coin": coin, "w": w,
                "up": (c > ph).astype(float), "dn": (c < pl).astype(float),
                "brk_up_mag": (c / ph - 1) / atr, "brk_dn_mag": (pl / c - 1) / atr,
                "r1": c.pct_change(1), "r6": c.pct_change(6), "r42": c.pct_change(42),
                "quiet": quiet, "volz": atr, "fwd": fwd,
                "fcast": b["forecast"], "pos": b["postRebalance_current_allocation"],
            })
            df.loc[ph.isna(), ["up", "dn"]] = np.nan
            df = df.iloc[::H].copy()
            rows.append(df)
            ts = pd.to_datetime(b["timestamp"])
            nx = c.shift(-1) / c - 1
            hourrows.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour, "wd": ts.dt.weekday, "nx": nx}))
    g = pd.concat(rows, ignore_index=True).dropna(subset=["fwd"])
    drift = g.groupby("coin")["fwd"].mean()
    sd = g.groupby("coin")["fwd"].std()
    g["u"] = g["fwd"] - g["coin"].map(drift)
    g["s"] = g["u"] / g["coin"].map(sd)
    out = {}
    def summ(sub, col="u"):
        x = sub[col].dropna()
        return pd.Series({"n": len(x), "mean_u": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "mean_abs_fwd": sub["fwd"].abs().mean()})
    out["drift_sd"] = pd.DataFrame({"drift": drift, "sd": sd})
    out["up_vs_dn_vs_none"] = pd.DataFrame({
        "up": summ(g[g.up == 1]), "dn": summ(g[g.dn == 1]), "none": summ(g[(g.up == 0) & (g.dn == 0)])}).T
    for col in ["r1", "r6", "r42", "quiet", "volz"]:
        sub = g.dropna(subset=[col]).copy()
        sub["q"] = sub.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
        out["quint_" + col] = sub.groupby("q").apply(summ)
    for col in ["brk_up_mag"]:
        sub = g[g.up == 1].dropna(subset=[col]).copy()
        sub["q"] = pd.qcut(sub[col].rank(method="first"), 4, labels=False)
        out["up_by_mag"] = sub.groupby("q").apply(summ)
    sub = g[g.dn == 1].dropna(subset=["brk_dn_mag"]).copy()
    sub["q"] = pd.qcut(sub["brk_dn_mag"].rank(method="first"), 4, labels=False)
    out["dn_by_mag"] = sub.groupby("q").apply(summ)
    # quiet x up breakout
    sub = g[g.up == 1].dropna(subset=["quiet"]).copy()
    sub["q"] = pd.qcut(sub["quiet"].rank(method="first"), 4, labels=False)
    out["up_by_quiet"] = sub.groupby("q").apply(summ)
    sub = g[g.dn == 1].dropna(subset=["quiet"]).copy()
    sub["q"] = pd.qcut(sub["quiet"].rank(method="first"), 4, labels=False)
    out["dn_by_quiet"] = sub.groupby("q").apply(summ)
    hr = pd.concat(hourrows, ignore_index=True).dropna()
    hr["nx_u"] = hr["nx"] - hr["coin"].map(hr.groupby("coin")["nx"].mean())
    f = lambda x: pd.Series({"n": len(x), "mean_bps": x.mean() * 1e4, "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out["by_hour"] = hr.groupby("hour")["nx_u"].apply(f).unstack()
    out["by_weekday"] = hr.groupby("wd")["nx_u"].apply(f).unstack()
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w
            d["next_coin"] = d["coin_return"].shift(-1); d["next_book"] = d["book_return"].shift(-1)
            dd.append(d)
    D = pd.concat(dd).dropna(subset=["book_return", "coin_return"])
    D["bq"] = pd.qcut(D["book_return"].rank(method="first"), 10, labels=False)
    out["book_deciles"] = D.groupby("bq")[["book_return", "coin_return", "next_coin", "next_book"]].mean()
    out["book_by_window"] = D.groupby("w")[["book_return", "coin_return"]].mean().assign(n=D.groupby("w").size())
    return out
