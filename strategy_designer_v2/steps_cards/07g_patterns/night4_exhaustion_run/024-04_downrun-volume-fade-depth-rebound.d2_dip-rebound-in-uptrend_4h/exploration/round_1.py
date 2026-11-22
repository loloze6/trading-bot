def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            absm = r.abs().rolling(180, min_periods=90).mean()
            sgn = np.sign(r).fillna(0)
            # streak length and loss
            run = np.zeros(len(b)); start = np.zeros(len(b), dtype=int)
            for i in range(len(b)):
                if i > 0 and sgn[i] != 0 and sgn[i] == sgn[i-1]:
                    run[i] = run[i-1] + 1; start[i] = start[i-1]
                else:
                    run[i] = 1 if sgn[i] != 0 else 0; start[i] = i - 1 if i > 0 else 0
            sc = c.values[start]
            streak_ret = c.values / sc - 1
            streak_usual = streak_ret / absm.values
            # volume during streak vs prior 30 bars
            vavg30 = v.rolling(30, min_periods=10).mean().shift(1)
            v3 = v.rolling(3).mean()
            vfade = np.log(v3 / vavg30)
            ret180 = c / c.shift(180) - 1
            ret6 = c / c.shift(6) - 1
            ret36 = c / c.shift(36) - 1
            ts = pd.to_datetime(b["timestamp"])
            fwd = c.shift(-H) / c - 1
            idx = np.arange(0, len(b), H)
            for i in idx:
                if i + H >= len(b): continue
                rows.append(dict(coin=coin, w=w, fwd=fwd[i], sgn=sgn[i], run=run[i],
                    su=streak_usual[i], vf=vfade[i], r180=ret180[i], r6=ret6[i]/ (absm[i] if absm[i]>0 else np.nan),
                    r36=ret36[i]/(absm[i] if absm[i]>0 else np.nan), vol=absm[i], hour=ts[i].hour, wd=ts[i].weekday(),
                    fc=b["forecast"].iloc[i], yr=ts[i].year))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby("coin")["fwd"].transform("mean")
    d["un"] = d["fwd"] - d["drift"]
    def grp(key, q=None, sub=None):
        x = d if sub is None else d[sub]
        x = x.dropna(subset=["un"] + ([key] if q is None else [key]))
        g = pd.qcut(x[key], q, duplicates="drop") if q else x[key]
        o = x.groupby(g)["un"].agg(["mean", "count", "std"])
        o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
        return o[["mean", "count", "t"]].round(4)
    out = {}
    out["streak_usual_q (all)"] = grp("su", 10)
    out["streak_usual_q r180>0"] = grp("su", 5, d.r180 > 0)
    out["streak_usual_q r180<0"] = grp("su", 5, d.r180 < 0)
    out["r6 usual q"] = grp("r6", 10)
    out["r36 usual q"] = grp("r36", 10)
    out["vol level q"] = grp("vol", 5)
    out["vfade q, down streak>=3"] = grp("vf", 4, (d.sgn < 0) & (d.run >= 3))
    out["vfade q, up streak>=3"] = grp("vf", 4, (d.sgn > 0) & (d.run >= 3))
    out["hour"] = grp("hour")
    out["weekday"] = grp("wd")
    out["r180 q"] = grp("r180", 5)
    out["year"] = grp("yr")
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    D = pd.concat(dd)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    bk["wd"] = pd.to_datetime(bk["day"]).dt.weekday
    bk["yr"] = pd.to_datetime(bk["day"]).dt.year
    out["book by weekday"] = bk.groupby("wd")[["book_return", "coin_return"]].mean().round(5)
    out["book by year"] = bk.groupby("yr")[["book_return", "coin_return"]].agg(["mean"]).round(5)
    out["book by coin"] = D.groupby("coin")[["book_return", "coin_return"]].mean().round(5)
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; tr.append(t)
    T = pd.concat(tr)
    T["dur_h"] = T["duration_minutes"] / 60
    out["trades by duration q"] = T.groupby(pd.qcut(T["dur_h"], 5, duplicates="drop"))["net_profit_loss_percent"].agg(["mean", "count"]).round(3)
    out["trades by entry fc q"] = T.groupby(pd.qcut(T["entry_forecast"], 5, duplicates="drop"))["net_profit_loss_percent"].agg(["mean", "count"]).round(3)
    out["n grid"] = len(d)
    return out
