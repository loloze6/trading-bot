def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sma = c.rolling(20).mean()
            sd = r.rolling(20).std()
            st = (c - sma) / sma / sd
            r60 = c.pct_change(60)
            fc = b.get("debug_info.components.stretch.post_pipeline_value")
            for h in (5, 10):
                fw = c.shift(-h) / c - 1
                for i in range(0, len(b), h):
                    if np.isnan(fw.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, w=w, h=h, day=str(b["timestamp"].iloc[i])[:10],
                                     reg=b["regime"].iloc[i], st=st.iloc[i], r60=r60.iloc[i],
                                     fc=(fc.iloc[i] if fc is not None else np.nan), fw=fw.iloc[i]))
    df = pd.DataFrame(rows)
    df["un"] = df["fw"] - df.groupby(["coin", "h"])["fw"].transform("mean")

    def ct(d, col="un"):
        g = d.groupby("day")[col].sum()
        dev = d[col] - d[col].mean()
        gs = dev.groupby(d["day"]).sum()
        G = len(gs)
        if G < 3: return (np.nan, G)
        se = np.sqrt((gs ** 2).sum() * G / (G - 1)) / len(d)
        return (d[col].mean() / se, G)

    res = []
    for h in (5, 10):
        for reg in ("unknown", "chop"):
            for side, cond in (("below", lambda x: x.st < 0), ("above", lambda x: x.st >= 0)):
                d = df[(df.h == h) & (df.reg == reg) & df.st.notna()]
                d = d[cond(d)].copy()
                # graded: un weighted by |st| (slope proxy): mean of un*st / mean st^2
                d["x"] = d["un"] * d["st"]
                t1, G = ct(d, "x")
                q = d["st"].abs() > d["st"].abs().median()
                res.append(dict(h=h, reg=reg, side=side, n=len(d), days=G,
                                mean_un=d.un.mean(), t_un=ct(d)[0],
                                un_x_st=d.x.mean(), t_unxst=t1,
                                deep_minus_shallow=d.un[q].mean() - d.un[~q].mean()))
    out["graded raw stretch, clustered"] = pd.DataFrame(res).round(4)

    # by window: calm, h5, sign of mean(un*st) on all stretch
    d = df[(df.h == 5) & (df.reg == "unknown") & df.st.notna()].copy()
    d["x"] = d["un"] * d["st"]
    out["calm h5 un*st by window"] = d.groupby("w")["x"].agg(["mean", "count"]).round(4)

    # raw vs recorded forecast in calm below-average
    d = df[(df.h == 5) & (df.reg == "unknown") & (df.st < 0) & df.fc.notna()]
    out["calm below: corr un with raw st, with forecast"] = pd.Series(
        {"corr_raw": d[["un", "st"]].corr().iloc[0, 1], "corr_fc": d[["un", "fc"]].corr().iloc[0, 1],
         "corr_raw_fc": d[["st", "fc"]].corr().iloc[0, 1], "n": len(d)}).round(4)

    # trend x agitation x stretch half
    d = df[(df.h == 5) & df.st.notna() & df.r60.notna()].copy()
    d["tr"] = np.where(d.r60 > 0.10, "rising", np.where(d.r60 < -0.10, "falling", "choppy"))
    d["half"] = np.where(d.st < 0, "below", "above")
    res = []
    for (reg, tr, half), g in d.groupby(["reg", "tr", "half"]):
        g = g.copy(); g["x"] = g.un * g.st
        res.append(dict(reg=reg, tr=tr, half=half, n=len(g), mean_un=g.un.mean(), t=ct(g)[0],
                        un_x_st=g.x.mean(), t_x=ct(g, "x")[0]))
    out["h5 profile x half"] = pd.DataFrame(res).round(4)
    return out
