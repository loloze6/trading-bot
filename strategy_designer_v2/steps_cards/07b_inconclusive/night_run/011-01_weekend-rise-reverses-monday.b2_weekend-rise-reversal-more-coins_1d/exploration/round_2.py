import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        g = {}
        for h in (1, 2, 3, 5):
            acc = []
            for w, b in wins.items():
                c = b["close"].values.astype(float)
                idx = np.arange(0, len(c) - h, h)
                acc.extend(c[idx + h] / c[idx] - 1)
            g[h] = np.nanmean(acc)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            ts = pd.to_datetime(b["timestamp"])
            wd = ts.dt.weekday.values
            yr = ts.dt.year.values
            s = pd.Series(np.r_[np.nan, c[1:] / c[:-1] - 1])
            sd = s.rolling(60, min_periods=20).std()
            r2b = pd.Series(np.r_[np.nan, np.nan, c[2:] / c[:-2] - 1])
            n = len(c)
            for t in range(n - 5):
                if wd[t] != 6:
                    continue
                rows.append((coin, w, yr[t], s.iloc[t], s.iloc[t] / sd.iloc[t], r2b.iloc[t],
                             c[t+1]/c[t]-1-g[1], c[t+2]/c[t]-1-g[2], c[t+3]/c[t]-1-g[3], c[t+5]/c[t]-1-g[5]))
    d = pd.DataFrame(rows, columns=["coin","w","yr","r0","zs","wk2","e1","e2","e3","e5"]).dropna()
    def tf(v):
        return v.mean() / (v.std() / np.sqrt(len(v)))
    out = {}
    d["dec_r0"] = pd.qcut(d.r0.rank(method="first"), 10, labels=False)
    out["sun_all_by_r0_decile"] = d.groupby("dec_r0").agg(n=("e2","size"), r0=("r0","mean"), e1=("e1","mean"), e2=("e2","mean"), t2=("e2", tf), e5=("e5","mean"))
    d["dec_wk2"] = pd.qcut(d.wk2.rank(method="first"), 10, labels=False)
    out["sun_all_by_weekend2day_decile"] = d.groupby("dec_wk2").agg(n=("e2","size"), wk2=("wk2","mean"), e2=("e2","mean"), t2=("e2", tf))
    d["dec_zs"] = pd.qcut(d.zs.rank(method="first"), 10, labels=False)
    out["sun_all_by_volscaled_decile"] = d.groupby("dec_zs").agg(n=("e2","size"), zs=("zs","mean"), e2=("e2","mean"), t2=("e2", tf))
    up = d[d.r0 > 0]; dn = d[d.r0 <= 0]
    out["sign_split"] = pd.DataFrame({
        "up_n": [len(up)]*4, "up_mean": [up[k].mean() for k in ["e1","e2","e3","e5"]], "up_t": [tf(up[k]) for k in ["e1","e2","e3","e5"]],
        "dn_n": [len(dn)]*4, "dn_mean": [dn[k].mean() for k in ["e1","e2","e3","e5"]], "dn_t": [tf(dn[k]) for k in ["e1","e2","e3","e5"]],
        "updn_welch_t": [ (up[k].mean()-dn[k].mean())/np.sqrt(up[k].var()/len(up)+dn[k].var()/len(dn)) for k in ["e1","e2","e3","e5"]]},
        index=["h1","h2","h3","h5"])
    out["rank_corr_r0_e2_up"] = float(up[["r0","e2"]].corr(method="spearman").iloc[0,1])
    out["rank_corr_zs_e2_up"] = float(up[["zs","e2"]].corr(method="spearman").iloc[0,1])
    out["rank_corr_r0_e2_all"] = float(d[["r0","e2"]].corr(method="spearman").iloc[0,1])
    return out
