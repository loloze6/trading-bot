import numpy as np, pandas as pd

def _ct(vals, days):
    # mean, t clustered by day (deviations summed per day), n, ndays
    v = pd.Series(np.asarray(vals, float)); d = pd.Series(np.asarray(days))
    m = v.notna(); v = v[m]; d = d[m]
    n = len(v)
    if n < 5: return (np.nan, np.nan, n, 0)
    mu = v.mean(); s = (v - mu).groupby(d.values).sum()
    se = np.sqrt((s**2).sum()) / n
    return (mu, mu/se if se > 0 else np.nan, n, len(s))

def _slope_ct(x, y, days):
    x = np.asarray(x, float); y = np.asarray(y, float); d = np.asarray(days)
    m = ~np.isnan(x) & ~np.isnan(y); x, y, d = x[m], y[m], d[m]
    xc = x - x.mean(); b = (xc*(y-y.mean())).sum()/(xc**2).sum()
    e = (y - y.mean() - b*xc)
    s = pd.Series(xc*e).groupby(d).sum()
    se = np.sqrt((s**2).sum())/(xc**2).sum()
    return b, b/se, len(x)

def explore(data):
    H = 14
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "ret14": c/c.shift(14)-1, "ret60": c/c.shift(60)-1, "ret1": r1,
                "vr": v.rolling(14).mean()/v.rolling(30).mean()-1,
                "vol20": r1.rolling(20).std(),
                "fwd": c.shift(-H)/c-1,
                "fc": b["forecast"].astype(float), "regime": b["regime"],
                "pos": np.arange(len(b)),
            })
            df["vol_rel"] = df["vol20"]/r1.rolling(60, min_periods=40).std()
            rows.append(df[df["pos"] % H == 0])
    g = pd.concat(rows)
    g = g[g["fwd"].notna()]
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    out = {}

    def by_q(col, sub, name, q=5):
        s = sub[sub[col].notna()].copy()
        s["q"] = pd.qcut(s[col].rank(method="first"), q, labels=False)
        res = []
        for k, gg in s.groupby("q"):
            mu, t, n, nd = _ct(gg["ex"], gg["day"])
            res.append({"q": k, "x_mean": gg[col].mean(), "ex_mean": mu, "t": t, "n": n, "days": nd})
        bb, tt, nn = _slope_ct(s[col], s["ex"], s["day"])
        out[name] = pd.DataFrame(res)
        out[name + " slope,t,n"] = f"{bb:.4f}, {tt:.2f}, {nn}"

    up = g[g["ret14"] > 0]; dn = g[g["ret14"] <= 0]
    by_q("vr", up, "volswell | 14d up")
    by_q("vr", dn, "volswell | 14d down")
    by_q("ret60", g, "ret60 all")
    by_q("ret14", g, "ret14 all")
    by_q("vol_rel", g, "vol_rel all")
    by_q("ret60", up, "ret60 | 14d up")
    # interaction: 14d up and 60d return
    # daily: weekday of coin returns
    dd = pd.concat([d.assign(coin=c, win=w) for c, ws in data["days"].items() for w, d in ws.items()])
    dd["day"] = pd.to_datetime(dd["day"]); dd["wd"] = dd["day"].dt.weekday
    res = []
    for k, gg in dd.groupby("wd"):
        mu, t, n, nd = _ct(gg["coin_return"], gg["day"])
        mb, tb, _, _ = _ct(gg["book_return"], gg["day"])
        res.append({"wd": k, "coin_mean": mu, "t": t, "book_mean": mb, "book_t": tb, "days": nd})
    out["weekday"] = pd.DataFrame(res)
    # book daily: portfolio mean per day per window
    bk = dd.groupby(["win", "day"])["book_return"].mean().dropna()
    cr = dd.groupby(["win", "day"])["coin_return"].mean().dropna()
    j = pd.concat([bk, cr], axis=1).dropna()
    j["yr"] = j.index.get_level_values("day").year
    out["book by year"] = j.groupby("yr").agg(book=("book_return", "mean"), coins=("coin_return", "mean"),
                                              n=("book_return", "size"))
    srt = j["book_return"].sort_values()
    out["book top/bottom 5% share of total"] = pd.Series({
        "total": j["book_return"].sum(), "top5%": srt.iloc[-int(len(srt)*0.05):].sum(),
        "bottom5%": srt.iloc[:int(len(srt)*0.05)].sum(), "corr_with_coins": j.corr().iloc[0, 1]})
    # trades by entry forecast
    tr = pd.concat([t for ws in data["trades"].values() for t in ws.values() if len(t)])
    tr["fq"] = pd.qcut(tr["entry_forecast"].rank(method="first"), 4, labels=False)
    out["trades by entry fc q"] = tr.groupby("fq").agg(fc=("entry_forecast", "mean"),
        net=("net_profit_loss_percent", "mean"), med=("net_profit_loss_percent", "median"),
        n=("net_profit_loss_percent", "size"), days=("duration_minutes", lambda x: x.mean()/1440))
    return out
