def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    hold = {}
    for coin, wins in bars.items():
        rr = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c)-5, 5)
            rr += list(c[idx+5]/c[idx]-1)
        hold[coin] = np.mean(rr)
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; v = df["volume"].values; f = df["forecast"].values
            n = len(df)
            col = "debug_info.components.scaled_fall.last_history_value"
            raw = df[col] if col in df.columns else pd.Series(np.nan, index=df.index)
            for i in range(0, n-5, 5):
                if not (f[i] < 0): continue
                rec = {"coin":coin,"w":w,"day":str(pd.Timestamp(df["timestamp"].iloc[i]).date()),
                       "year":pd.Timestamp(df["timestamp"].iloc[i]).year,"f":f[i],"raw":raw.iloc[i],
                       "x5":c[i+5]/c[i]-1-hold[coin]}
                if i >= 30:
                    rec["r30"] = c[i]/c[i-30]-1
                    rec["vr"] = v[i-29:i+1].mean()/v[max(0,i-89):i+1].mean() if i>=60 else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    out = {}
    g = d.groupby("day")["x5"].sum()
    nd = d.groupby("day").size()
    tm = d["x5"].mean()/ (g.std(ddof=1)*np.sqrt(len(g))/len(d))
    out["mean_excess"] = pd.Series({"n":len(d),"days":len(g),"mean":d["x5"].mean(),
        "t_dayclustered":tm,"t_plain":stats.ttest_1samp(d["x5"],0).statistic,
        "share_neg":(d["x5"]<0).mean()})
    out["mean_by_coin_sign"] = d.groupby("coin")["x5"].agg(["mean","count"])
    out["mean_by_window"] = d.groupby("w")["x5"].agg(["mean","count"])
    def reg(s, x):
        s = s.dropna(subset=[x,"x5"])
        if len(s)<5: return (len(s),np.nan,np.nan)
        r = stats.linregress(s[x], s["x5"]); return (len(s), r.slope, r.slope/r.stderr)
    out["slope_alt"] = pd.DataFrame({"f":reg(d,"f"),"raw":reg(d,"raw"),"r30":reg(d,"r30"),
        "f_no2021":reg(d[d.year!=2021],"f")}, index=["n","slope","t"]).T
    dv = d.dropna(subset=["vr"]).copy()
    dv["vq"] = np.where(dv["vr"] <= dv["vr"].median(), "quiet", "heavy")
    out["vol_split"] = dv.groupby("vq")["x5"].agg(["mean","count"])
    return out
