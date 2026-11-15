def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    col = "debug_info.components.below_ma.last_history_value"
    mus = {}
    for c, ws in bars.items():
        r = [(df["close"].shift(-1)/df["close"]-1).dropna() for w, df in ws.items()]
        mus[c] = pd.concat(r).mean()
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            if col not in df: continue
            d = df[col].values
            sma = cl/(1+d/100.0)
            for h in [10, 20]:
                for i in range(0, len(df)-h, h):
                    if np.isnan(d[i]) or d[i] >= 0: continue
                    ret = cl[i+h]/cl[i]-1
                    sl = sma[i]/sma[i-30]-1 if i >= 30 and not np.isnan(sma[i-30]) else np.nan
                    p20 = cl[i]/cl[i-20]-1 if i >= 20 else np.nan
                    p60 = cl[i]/cl[i-60]-1 if i >= 60 else np.nan
                    rows.append(dict(coin=c, win=w, h=h, d=d[i], sg=-(ret-h*mus[c]), slope30=sl, p20=p20, p60=p60))
    R = pd.DataFrame(rows)
    def summ(g):
        n = len(g); m = g.mean(); s = g.std()
        return pd.Series(dict(n=n, mean=m, t=m/(s/np.sqrt(n)) if n > 1 else np.nan))
    out = {}
    for h in [10, 20]:
        b = R[R.h == h].copy()
        b["sl_q"] = pd.qcut(b["slope30"], 3, labels=False)
        out[f"h{h}_by_sma_slope30_tercile(0=falling most)"] = b.groupby("sl_q").agg(sl=("slope30", "mean")).join(b.groupby("sl_q")["sg"].apply(summ).unstack())
        b["p20_q"] = pd.qcut(b["p20"], 3, labels=False)
        out[f"h{h}_by_past20_tercile"] = b.groupby("p20_q").agg(p=("p20", "mean")).join(b.groupby("p20_q")["sg"].apply(summ).unstack())
        b["p60_q"] = pd.qcut(b["p60"], 3, labels=False)
        out[f"h{h}_by_past60_tercile"] = b.groupby("p60_q").agg(p=("p60", "mean")).join(b.groupby("p60_q")["sg"].apply(summ).unstack())
        b["fall"] = b["slope30"] < 0
        out[f"h{h}_sma_falling_x_p60pos"] = b.groupby(["fall", b["p60"] > 0])["sg"].apply(summ).unstack()
    b = R[R.h == 10].copy()
    b["p60_q"] = pd.qcut(b["p60"], 3, labels=False)
    out["h10_top_p60_by_coin"] = b[b.p60_q == 2].groupby("coin")["sg"].apply(summ).unstack()
    out["h10_corr_sg_p60"] = float(b[["sg", "p60"]].corr().iloc[0, 1])
    out["h10_corr_sg_d"] = float(b[["sg", "d"]].corr().iloc[0, 1])
    return out
