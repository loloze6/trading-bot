def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]; al = b["postRebalance_current_allocation"]
            g = al * (c.shift(-1)/c - 1)
            r14 = c.pct_change(14)
            yr = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(pd.DataFrame(dict(wn=int(w[1:]), yr=yr, side=np.sign(al), g=g, r14s=np.sign(r14))))
    d = pd.concat(rows).dropna()
    out["window_years"] = d.groupby("wn")["yr"].agg(["min","max"])
    out["gain_by_side_window"] = d.groupby(["wn","side"])["g"].sum().unstack()
    out["gain_by_side_r14"] = d.groupby(["side","r14s"])["g"].agg(["count","mean","sum"])
    cr = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; f = b["forecast"].values
            r14 = pd.Series(c).pct_change(14).values
            n = len(c)
            for i in range(0, n - 28, 14):
                cr.append(dict(coin=coin, f=f[i], r14=r14[i], fr=c[i+14]/c[i]-1, fr28=c[i+28]/c[i]-1))
    g = pd.DataFrame(cr).dropna()
    g["ex"] = g["fr"] - g.groupby("coin")["fr"].transform("mean")
    g["ex28"] = g["fr28"] - g.groupby("coin")["fr28"].transform("mean")
    g["s"] = np.sign(g["f"]); g["r14s"] = np.sign(g["r14"])
    def sm(x, col):
        return pd.Series(dict(n=len(x), mean=x[col].mean(), t=x[col].mean()/(x[col].std()/np.sqrt(len(x)))))
    out["r14up_by_signal_side"] = g[g.r14s>0].groupby("s").apply(lambda x: sm(x,"ex"))
    out["r14dn_by_signal_side"] = g[g.r14s<0].groupby("s").apply(lambda x: sm(x,"ex"))
    g["dex28"] = g["s"]*g["ex28"]; g["dex"] = g["s"]*g["ex"]
    out["h14_vs_h28_dir"] = pd.DataFrame({"h14": sm(g,"dex"), "h28": sm(g,"dex28")})
    g["s2"] = np.where((g.s>0)&(g.r14s<=0), 0, g.s)
    a = g[g.s2!=0].copy(); a["dex2"] = a["s2"]*a["ex"]; a["dtot2"] = a["s2"]*a["fr"]
    out["agree_rule"] = pd.Series(dict(n_active=len(a), dex=a["dex2"].mean(), dtot=a["dtot2"].mean(),
                                       t=a["dex2"].mean()/(a["dex2"].std()/np.sqrt(len(a)))))
    return out
