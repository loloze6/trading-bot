def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        dr = {}
        for H in (5, 10, 20):
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - H, H):
                    rs.append(c[i + H] / c[i] - 1)
            dr[H] = (np.mean(rs), np.std(rs, ddof=1))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; h = df["high"]; l = df["low"]
            hi60 = h.shift(1).rolling(60).max(); lo60 = l.shift(1).rolling(60).min()
            hi20 = h.shift(1).rolling(20).max(); lo20 = l.shift(1).rolling(20).min()
            pos20 = (c - lo20) / (hi20 - lo20)
            pos60 = (c - lo60) / (hi60 - lo60)
            er60 = (c - c.shift(60)).abs() / c.diff().abs().rolling(60).sum()
            brk = c / hi60 - 1
            day = pd.to_datetime(df["timestamp"]).dt.floor("D")
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for H in (5, 10, 20):
                d, sd = dr[H]
                for i in range(0, len(c) - H, H):
                    fr = c.iloc[i + H] / c.iloc[i] - 1
                    rows.append(dict(coin=coin, win=w, H=H, un=fr - d, st=(fr - d) / sd,
                        pos20=pos20.iloc[i], pos60=pos60.iloc[i], brk=brk.iloc[i], er60=er60.iloc[i],
                        day=day.iloc[i], yr=yr.iloc[i],
                        fold="B" if int(w[1:]) <= 12 else "C",
                        reg=df["regime"].iloc[i]))
    S = pd.DataFrame(rows)
    def ct(x):
        g = x.groupby("day")["un"].sum()
        m = x["un"].mean(); n = len(x)
        dev = x.assign(d=x["un"] - m).groupby("day")["d"].sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / n
        return pd.Series(dict(n=n, days=G, un=m, st=x["st"].mean(), tcl=m / se))
    out = {}
    for col in ["pos20", "pos60"]:
        for H in (5, 10, 20):
            s = S[S.H == H].dropna(subset=[col]).copy()
            s["q"] = pd.qcut(s[col].rank(method="first"), 5, labels=False)
            out[f"{col}_H{H}"] = s.groupby("q").apply(ct).round(4)
            out[f"{col}_H{H}_byfold"] = s.groupby(["fold", "q"]).apply(ct)[["n", "un", "tcl"]].unstack(0).round(3)
            out[f"{col}_H{H}_corr_by_coin"] = s.groupby("coin").apply(lambda x: x[col].corr(x["st"])).round(3)
    s = S[S.H == 20].dropna(subset=["pos60", "er60"]).copy()
    s["erq"] = pd.qcut(s["er60"], 3, labels=False)
    s["pq"] = pd.qcut(s["pos60"].rank(method="first"), 3, labels=False)
    out["H20_er_x_pos60"] = s.groupby(["erq", "pq"]).apply(ct)[["n", "un", "tcl"]].unstack(1).round(3)
    s = S[(S.H == 10)].dropna(subset=["pos60", "er60"]).copy()
    s["erq"] = pd.qcut(s["er60"], 3, labels=False)
    s["pq"] = pd.qcut(s["pos60"].rank(method="first"), 3, labels=False)
    out["H10_er_x_pos60"] = s.groupby(["erq", "pq"]).apply(ct)[["n", "un", "tcl"]].unstack(1).round(3)
    # book concentration
    D = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df.copy(); x["win"] = w; D.append(x)
    D = pd.concat(D)
    bk = D.groupby(["win", "day"])["book_return"].mean().dropna().sort_values()
    tot = bk.sum()
    out["book_conc"] = pd.Series(dict(n=len(bk), total=tot, top10=bk.tail(10).sum(), top30=bk.tail(30).sum(),
                                      bot10=bk.head(10).sum(), pos_share=(bk > 0).mean())).round(4)
    return out
