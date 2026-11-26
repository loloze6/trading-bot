def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    out = {}
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            n = len(b)
            fc = b["forecast"].fillna(0).values
            inprof = (b["regime"] == "unknown").values
            r7 = pd.Series(cl).pct_change(7)
            sc = r7 / r7.abs().rolling(30).mean()
            r60 = pd.Series(cl).pct_change(60)
            for h in (7, 14, 28):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=c, w=w, h=h, i=i, ts=b["timestamp"].iloc[i],
                                     ret=cl[i + h] / cl[i] - 1, fc=fc[i], prof=inprof[i],
                                     sc=sc.iloc[i], r60=r60.iloc[i]))
    df = pd.DataFrame(rows)
    df["day"] = pd.to_datetime(df["ts"]).dt.floor("D")
    df["drift"] = df.groupby(["coin", "h"])["ret"].transform("mean")
    df["um"] = df["ret"] - df["drift"]
    df["year"] = pd.to_datetime(df["ts"]).dt.year

    def summ(g):
        d = g.groupby("day")["um"].sum()
        nd = len(d)
        t = d.mean() / (d.std(ddof=1) / np.sqrt(nd)) * 1 if nd > 2 else np.nan
        return pd.Series(dict(n=len(g), days=nd, um=g["um"].mean(), tot=g["ret"].mean(), t_day=t))

    res = []
    for h in (7, 14, 28):
        d = df[df.h == h]
        sig = d[(d.fc > 0) & d.prof]
        noprofsig = d[d.prof & (d.fc <= 0)]
        allp = d[d.prof]
        for name, g in [("sig", sig), ("prof_nosig", noprofsig), ("prof_all", allp), ("all", d)]:
            s = summ(g); s["h"] = h; s["grp"] = name; res.append(s)
        if len(sig) > 20:
            q = pd.qcut(sig["fc"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
            for k, g in sig.groupby(q):
                s = summ(g); s["h"] = h; s["grp"] = "sig_" + str(k); s["fc_mean"] = g.fc.mean(); res.append(s)
        # scaled rise in profile, recomputed, terciles of positive sc
        ps = d[d.prof & (d.sc > 0)]
        if len(ps) > 20:
            q = pd.qcut(ps["sc"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
            for k, g in ps.groupby(q):
                s = summ(g); s["h"] = h; s["grp"] = "rawsc_" + str(k); s["sc_mean"] = g.sc.mean(); res.append(s)
        # scaled rise everywhere (not profile)
        ns = d[(~d.prof) & (d.sc > 0)]
        if len(ns) > 20:
            q = pd.qcut(ns["sc"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
            for k, g in ns.groupby(q):
                s = summ(g); s["h"] = h; s["grp"] = "outprof_sc_" + str(k); res.append(s)
    out["cases"] = pd.DataFrame(res).set_index(["h", "grp"])

    s14 = df[(df.h == 14) & (df.fc > 0) & df.prof]
    out["sig14_by_year"] = s14.groupby("year").agg(n=("um", "size"), um=("um", "mean"), tot=("ret", "mean"))
    out["sig14_by_coin"] = s14.groupby("coin").agg(n=("um", "size"), um=("um", "mean"), tot=("ret", "mean"))
    # r60 inside profile
    s14 = s14.copy()
    s14["r60b"] = pd.cut(s14.r60, [-1, -0.03, 0.03, 1])
    out["sig14_by_r60"] = s14.groupby("r60b").agg(n=("um", "size"), um=("um", "mean"), tot=("ret", "mean"))

    # book daily
    br = []
    for c in days:
        for w, d in days[c].items():
            x = d[["day", "book_return", "coin_return"]].copy(); x["coin"] = c; x["w"] = w; br.append(x)
    br = pd.concat(br)
    bk = br.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    bw = bk.groupby("w").agg(days=("day", "size"), book=("book_return", "mean"), coin=("coin_return", "mean"),
                             bsd=("book_return", "std"))
    bw["book_sh"] = bw.book / bw.bsd * np.sqrt(365)
    out["book_by_window"] = bw
    # deepest fall
    v = (1 + bk.sort_values(["w", "day"])["book_return"].fillna(0)).cumprod()
    dd = v / v.cummax() - 1
    out["maxdd"] = float(dd.min())
    bk2 = bk.sort_values(["w", "day"]).reset_index(drop=True); bk2["dd"] = dd.values
    out["dd_by_window"] = bk2.groupby("w")["dd"].min()
    # trades
    tr = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()])
    tr["win"] = tr.net_profit_loss_percent > 0
    tr["fcb"] = pd.qcut(tr.entry_forecast.rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["trades_by_fc"] = tr.groupby("fcb").agg(n=("win", "size"), win=("win", "mean"),
                                                net=("net_profit_loss_percent", "mean"),
                                                dur_d=("duration_minutes", lambda x: x.mean() / 1440))
    return out
