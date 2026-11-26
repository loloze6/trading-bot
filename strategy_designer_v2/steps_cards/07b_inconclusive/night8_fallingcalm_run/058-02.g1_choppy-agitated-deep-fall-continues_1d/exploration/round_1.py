def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    hold = {}
    for coin, wins in bars.items():
        for H in [1,3,5,10,20]:
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c)-H, H)
                rr += list(c[idx+H]/c[idx]-1)
            hold[(coin,H)] = np.mean(rr) if rr else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; v = df["volume"].values
            col = "debug_info.components.scaled_fall.last_history_value"
            raw = df[col] if col in df.columns else pd.Series(np.nan, index=df.index)
            f = df["forecast"].values
            n = len(df)
            for i in range(0, n-5, 5):
                if not (f[i] < 0): continue
                rec = {"coin":coin,"w":w,"year":pd.Timestamp(df["timestamp"].iloc[i]).year,
                       "f":f[i],"raw":raw.iloc[i]}
                for H in [1,3,5,10,20]:
                    if i+H < n:
                        rec[f"x{H}"] = c[i+H]/c[i]-1-hold[(coin,H)]
                if i >= 30:
                    rec["vol10_30"] = v[i-9:i+1].mean()/v[i-29:i+1].mean()
                    rec["ret30"] = c[i]/c[i-30]-1
                rows.append(rec)
    d = pd.DataFrame(rows)
    out = {}
    def reg(s, ycol="x5"):
        s = s.dropna(subset=[ycol])
        if len(s) < 5: return (len(s), np.nan, np.nan, np.nan)
        r = stats.linregress(s["f"], s[ycol])
        return (len(s), s[ycol].mean(), r.slope, r.slope/r.stderr)
    out["all_by_H"] = pd.DataFrame({H: reg(d, f"x{H}") for H in [1,3,5,10,20]}, index=["n","mean_excess","slope","t"]).T
    out["by_coin"] = pd.DataFrame({k: reg(g) for k,g in d.groupby("coin")}, index=["n","mean","slope","t"]).T
    out["by_year"] = pd.DataFrame({k: reg(g) for k,g in d.groupby("year")}, index=["n","mean","slope","t"]).T
    d["fq"] = pd.qcut(d["f"].rank(method="first"), 3, labels=["deep","mid","shallow"])
    out["by_f_tercile"] = d.groupby("fq")[["x1","x3","x5","x10","f"]].agg(["mean","count"])
    dv = d.dropna(subset=["vol10_30"])
    dv["vq"] = pd.qcut(dv["vol10_30"].rank(method="first"), 2, labels=["quiet","heavy"])
    out["by_volume_half"] = pd.DataFrame({k: reg(g) for k,g in dv.groupby("vq")}, index=["n","mean","slope","t"]).T
    out["raw_vs_f_corr"] = float(d[["raw","f"]].corr().iloc[0,1]) if d["raw"].notna().any() else "na"
    return out
