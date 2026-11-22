import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [6, 12, 18, 36]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            rs = np.concatenate(rs)
            drift[(coin, h)] = rs.mean(); usual[(coin, h)] = rs.std()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; v = df["volume"].values
            n = len(c)
            r = np.r_[np.nan, c[1:] / c[:-1] - 1]
            absm = pd.Series(np.abs(r)).rolling(180, min_periods=45).mean().values
            # streak recompute both sides
            up_len = np.zeros(n, int); dn_len = np.zeros(n, int)
            for i in range(1, n):
                if r[i] > 0: up_len[i] = up_len[i-1] + 1
                if r[i] < 0: dn_len[i] = dn_len[i-1] + 1
            fc = df["forecast"].values
            rg = df["debug_info.components.run_gain.last_history_value"].values
            vf = df["debug_info.components.vol_fade.last_history_value"].values
            # short-bet cases approx: first bar per 18 grid cell with forecast <= -2
            for cell in range(0, n, 18):
                seg = np.where(fc[cell:cell+18] <= -2)[0]
                if len(seg):
                    i = cell + seg[0]
                    rec = dict(coin=coin, w=w, side="up_sig", i=i, L=up_len[i], rg=rg[i], vf=vf[i],
                               yr=pd.Timestamp(df["timestamp"].iloc[i]).year)
                    for h in H:
                        rec[f"u{h}"] = -(c[i+h]/c[i]-1 - drift[(coin,h)]) if i+h < n else np.nan
                        rec[f"s{h}"] = rec[f"u{h}"]/usual[(coin,h)] if i+h < n else np.nan
                    rows.append(rec)
            # down-streak analogue: per 18 grid cell, bar with largest down-run in usual moves (len>=3)
            for cell in range(0, n, 18):
                best = None
                for i in range(cell, min(cell+18, n)):
                    L = dn_len[i]
                    if L >= 3 and not np.isnan(absm[i]):
                        g = -np.sum(r[i-L+1:i+1]) / absm[i]
                        fade = np.log(max(v[i-L+1],1e-12)/max(v[i],1e-12))
                        if best is None or g > best[1]: best = (i, g, fade, L)
                if best:
                    i, g, fade, L = best
                    rec = dict(coin=coin, w=w, side="dn_run", i=i, L=L, rg=g, vf=fade,
                               yr=pd.Timestamp(df["timestamp"].iloc[i]).year)
                    for h in H:
                        rec[f"u{h}"] = (c[i+h]/c[i]-1 - drift[(coin,h)]) if i+h < n else np.nan
                        rec[f"s{h}"] = rec[f"u{h}"]/usual[(coin,h)] if i+h < n else np.nan
                    rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g, col="u18"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    up = d[d.side=="up_sig"]; dn = d[d.side=="dn_run"]
    out = {}
    out["up horizons"] = pd.DataFrame({h: summ(up, f"u{h}") for h in H}).T
    out["up by coin"] = up.groupby("coin").apply(summ)
    out["up by year"] = up.groupby("yr").apply(summ)
    up = up.copy(); up["rgq"] = pd.qcut(up["rg"].rank(method="first"), 5, labels=False)
    out["up by run_gain quintile"] = up.groupby("rgq").apply(summ)
    up["vfq"] = pd.qcut(up["vf"].rank(method="first"), 5, labels=False)
    out["up by vol_fade quintile"] = up.groupby("vfq").apply(summ)
    out["up by streak length"] = up.groupby(up["L"].clip(upper=6)).apply(summ)
    out["up rg x vf (top half each)"] = up.groupby([up.rgq>=3, up.vfq>=3]).apply(summ)
    dn = dn.copy(); dn["rgq"] = pd.qcut(dn["rg"].rank(method="first"), 5, labels=False)
    out["down-run long, by size quintile"] = dn.groupby("rgq").apply(summ)
    out["down-run horizons top quintile"] = pd.DataFrame({h: summ(dn[dn.rgq==4], f"u{h}") for h in H}).T
    dt = dn[dn.rgq>=3].copy(); dt["fade_pos"] = dt.vf > 0
    out["down-run top2q by fade>0"] = dt.groupby("fade_pos").apply(summ)
    return out
