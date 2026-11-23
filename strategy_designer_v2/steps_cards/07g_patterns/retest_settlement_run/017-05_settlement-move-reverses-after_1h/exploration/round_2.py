def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; out = {}
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            d = df[["timestamp","close"]].copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            c = d["close"].values.astype(float); n = len(c)
            def ret(k, fwd=False):
                r = np.full(n, np.nan)
                if fwd: r[:n-k] = c[k:]/c[:n-k]-1
                else: r[k:] = c[k:]/c[:-k]-1
                return r
            lr = np.r_[np.nan, np.log(c[1:]/c[:-1])]
            e = pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(n),
                "hour":((d["timestamp"]+pd.Timedelta(hours=1)).dt.hour).values,
                "year":d["timestamp"].dt.year.values,
                "p24":ret(24),"f24":ret(24,True),"p2":ret(2),"f2":ret(2,True),
                "vol24":pd.Series(lr).rolling(24).std().values,
                "vol720":pd.Series(lr).rolling(720,min_periods=200).std().values})
            rows.append(e)
    E = pd.concat(rows, ignore_index=True)
    for k in (2,24):
        g = E[E.pos % k == 0].groupby("coin")[f"f{k}"].mean()
        E[f"x{k}"] = E[f"f{k}"] - E["coin"].map(g)
    us = E[E.pos % 24 == 0].groupby("coin")["f24"].std()
    E["us24"] = E["coin"].map(us)
    s = E[E.pos % 24 == 0].dropna(subset=["p24","x24","vol720","vol24"]).copy()
    s["vr"] = s["vol24"]/s["vol720"]            # known at close: recent vs longer vol
    s["z"] = s["p24"]/(s["vol720"]*np.sqrt(24))
    s["cr"] = -np.sign(s["p24"])*s["x24"]
    s["crt"] = -np.sign(s["p24"])*(s["f24"])
    def tab(g, col="cr"):
        a = g[col].agg(["count","mean","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"])); a["mean"]*=100; return a.round(3)
    # graded: |p24| raw quintile (absolute size, scale-free of vol720 normalisation)
    s["aq"] = pd.qcut(s["p24"].abs(), 5, labels=False)
    out["24h rev by |24h return| quintile"] = tab(s.groupby("aq"))
    s["zq"] = pd.qcut(s["z"].abs(), 5, labels=False)
    out["24h rev by |z| quintile"] = tab(s.groupby("zq"))
    # vol ratio quintile, within big moves
    big = s[s.zq >= 3].copy()
    big["vq"] = pd.qcut(big["vr"], 4, labels=False)
    out["24h rev big |z| by vol24/vol720 quartile"] = tab(big.groupby("vq"))
    # graded measure: cr weighted by |p24|/vol720 i.e. regression of x24 on -p24
    out["regress x24 on p24 by coin"] = s.groupby("coin").apply(lambda g: pd.Series(stats.linregress(g["p24"], g["x24"])._asdict())[["slope","rvalue","pvalue"]]).round(4)
    out["24h rev top2 |24h| quintiles by year"] = tab(s[s.aq>=3].groupby("year"))
    out["24h rev top2 |24h| quintiles by coin"] = tab(s[s.aq>=3].groupby("coin"))
    out["24h rev top2 quintiles by direction (1=after rise)"] = tab(s[s.aq>=3].assign(up=(s.p24>0).astype(int)).groupby("up"))
    out["total move top quintile |24h| (incl drift)"] = tab(s[s.aq==4], "crt")
    # windows: share of windows positive in top quintile
    ww = s[s.aq>=3].groupby("w")["cr"].mean()
    out["windows positive share (top2 q)"] = pd.DataFrame({"n_w":[len(ww)],"share_pos":[(ww>0).mean()],"mean_%":[ww.mean()*100]}).round(3)
    # 2h reversal: hours 12-14 vs others, graded by |z2|
    t2 = E[E.pos % 2 == 0].dropna(subset=["p2","x2","vol720"]).copy()
    t2["z"] = t2["p2"]/(t2["vol720"]*np.sqrt(2)); t2["cr"] = -np.sign(t2["p2"])*t2["x2"]
    t2["us"] = t2["hour"].isin([12,13,14]).astype(int)
    t2["zq"] = pd.qcut(t2["z"].abs(),5,labels=False)
    out["2h rev by US-open hours x |z| quintile"] = tab(t2.groupby(["us","zq"]))
    return out
