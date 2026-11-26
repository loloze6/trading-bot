def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]

    def cl_t_slope(x, y, g):
        # OLS slope of y on x with day-clustered se
        x = np.asarray(x, float); y = np.asarray(y, float)
        xc = x - x.mean(); b = (xc * y).sum() / (xc ** 2).sum()
        e = y - y.mean() - b * xc
        s = pd.Series(xc * e).groupby(np.asarray(g)).sum()
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / (xc ** 2).sum()
        return b, b / se, G

    def cl_t(y, g):
        y = pd.Series(np.asarray(y, float)); dev = y - y.mean()
        s = dev.groupby(np.asarray(g)).sum(); G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / len(y)
        return y.mean() / se, G

    for h in [14, 30]:
        recs = []
        for coin, ws in bars.items():
            per = []
            for w, b in ws.items():
                c = b["close"].values.astype(float); n = len(c)
                r1 = np.r_[np.nan, np.diff(np.log(c))]
                for p in range(0, n - h, h):
                    d = dict(coin=coin, w=w, ts=b["timestamp"].iloc[p],
                             yr=pd.Timestamp(b["timestamp"].iloc[p]).year,
                             fwd=c[p + h] / c[p] - 1)
                    d["vol30"] = np.nanstd(r1[p - 29:p + 1]) if p >= 30 else np.nan
                    d["vol10"] = np.nanstd(r1[p - 9:p + 1]) if p >= 10 else np.nan
                    d["vol60"] = np.nanstd(r1[p - 59:p + 1]) if p >= 60 else np.nan
                    d["ret1"] = r1[p] if p >= 1 else np.nan
                    d["dd60"] = c[p] / c[max(0, p - 59):p + 1].max() - 1 if p >= 30 else np.nan
                    d["p30"] = c[p] / c[p - 30] - 1 if p >= 30 else np.nan
                    per.append(d)
            if not per: continue
            d = pd.DataFrame(per)
            d["exz"] = (d["fwd"] - d["fwd"].mean()) / d["fwd"].std()
            recs.append(d)
        D = pd.concat(recs, ignore_index=True)
        D["volz"] = D.groupby("coin")["vol30"].transform(lambda s: s / s.mean())
        D["vratio"] = np.log(D["vol10"] / D["vol60"])
        D["ret1z"] = D.groupby("coin")["ret1"].transform(lambda s: s / s.std())
        D["p30z"] = D.groupby("coin")["p30"].transform(lambda s: s / s.abs().mean())
        res = []; coinres = []; yrres = []
        for sig in ["volz", "vratio", "ret1z", "dd60", "p30z"]:
            dd = D.dropna(subset=[sig, "exz"])
            xr = dd.groupby("coin")[sig].rank(pct=True)
            b, t, G = cl_t_slope(xr, dd["exz"], dd["ts"])
            res.append(dict(sig=sig, slope_rank=b, t_cl=t, n=len(dd), days=G))
            pos = 0; tot = 0
            for c_, s in dd.groupby("coin"):
                if len(s) < 15: continue
                r = stats.spearmanr(s[sig], s["exz"])[0]; tot += 1; pos += r > 0
            coinres.append(dict(sig=sig, coins_pos=pos, coins=tot))
            for y_, s in dd.groupby("yr"):
                if len(s) < 20: continue
                yrres.append(dict(sig=sig, yr=y_, rho=stats.spearmanr(s[sig], s["exz"])[0], n=len(s)))
        out[f"h{h}_slopes_clustered"] = pd.DataFrame(res)
        out[f"h{h}_coin_sign"] = pd.DataFrame(coinres)
        if h == 30:
            out["h30_rho_by_year"] = pd.DataFrame(yrres).pivot(index="yr", columns="sig", values="rho")
            dd = D.dropna(subset=["volz"]).copy()
            dd["q"] = dd.groupby("coin")["volz"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
            tab = []
            for q, s in dd.groupby("q"):
                t, G = cl_t(s["exz"], s["ts"])
                tab.append(dict(q=q, exz=s["exz"].mean(), fwd=s["fwd"].mean(), t=t, n=len(s), days=G))
            out["h30_volz_terciles_withincoin"] = pd.DataFrame(tab)

    # weekday with day clustering: mean across coins per day, then t across days
    allb = []
    for coin, ws in days.items():
        for w, dd in ws.items():
            x = dd[["day", "coin_return"]].dropna().copy(); x["coin"] = coin; allb.append(x)
    A = pd.concat(allb)
    A["rz"] = A.groupby("coin")["coin_return"].transform(lambda s: (s - s.mean()) / s.std())
    A["day"] = pd.to_datetime(A["day"])
    dm = A.groupby("day")["rz"].mean().to_frame()
    dm["wd"] = dm.index.weekday; dm["yr"] = dm.index.year
    out["weekday_daycluster"] = dm.groupby("wd")["rz"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    dm["half"] = np.where(dm["yr"] <= 2021, "early", "late")
    out["weekday_by_half"] = dm.groupby(["half", "wd"])["rz"].mean().unstack()
    return out
