import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    raw_col = "debug_info.components.break_touches.last_history_value"
    def feats(H):
        rows = []
        for coin, wins in bars.items():
            allr = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - H, H)
                allr.extend(list(c[idx + H] / c[idx] - 1))
            dr = np.mean(allr); sd = np.std(allr)
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"].values; n = len(c)
                r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
                vol = pd.Series(r1).rolling(20).std().values
                s = pd.Series(c)
                ret20 = (s / s.shift(20) - 1).values
                hi60 = s.rolling(60, min_periods=30).max().values
                raw = b[raw_col].values if raw_col in b else np.full(n, np.nan)
                ts = pd.to_datetime(b["timestamp"])
                for i in range(0, n - H, H):
                    u = c[i + H] / c[i] - 1 - dr
                    rows.append(dict(coin=coin, brk=bool(raw[i] > 0) if not np.isnan(raw[i]) else False,
                                     raw=raw[i] if not np.isnan(raw[i]) else 0.0,
                                     u=u, s=u / sd, z1=r1[i] / vol[i] if vol[i] > 0 else np.nan,
                                     ret20=ret20[i], near=c[i] / hi60[i] - 1, vol=vol[i],
                                     wd=ts.iloc[i].weekday()))
        return pd.DataFrame(rows)
    def summ(g, col="u"):
        x = g[col].dropna()
        lo, hi = x.quantile(0.01), x.quantile(0.99)
        xw = x.clip(lo, hi)
        return pd.Series({"n": len(x), "mean": x.mean(), "median": x.median(), "wmean": xw.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "strength": g["s"].mean()})
    for H in (5, 10, 20):
        d = feats(H)
        out["H%d_all_mean_u" % H] = float(d["u"].mean())
        out["H%d_break_vs_not" % H] = d.groupby("brk").apply(summ)
        bk = d[d.brk]
        if H == 20:
            out["H20_break_by_raw_tercile"] = bk.assign(q=pd.qcut(bk["raw"].rank(method="first"), 3, labels=False)).groupby("q").apply(summ)
            pc = d.groupby(["coin", "brk"])["u"].mean().unstack()
            out["H20_coins_break_minus_not_pos"] = f"{int(((pc[True]-pc[False])>0).sum())} of {int(pc.notna().all(axis=1).sum())}"
        out["H%d_by_ret20_quintile" % H] = d.assign(q=pd.qcut(d["ret20"].rank(method="first"), 5, labels=False)).groupby("q").apply(summ)
        out["H%d_by_near_high_quintile" % H] = d.assign(q=pd.qcut(d["near"].rank(method="first"), 5, labels=False)).groupby("q").apply(summ)
        if H == 5:
            out["H5_by_z1_quintile"] = d.assign(q=pd.qcut(d["z1"].rank(method="first"), 5, labels=False)).groupby("q").apply(summ)
            out["H5_by_vol_quintile"] = d.assign(q=pd.qcut(d["vol"].rank(method="first"), 5, labels=False)).groupby("q").apply(summ)
            out["H5_by_weekday"] = d.groupby("wd").apply(summ)
        if H == 20:
            pc = d.dropna(subset=["ret20"]).groupby("coin").apply(lambda g: g["ret20"].corr(g["u"], method="spearman"))
            out["H20_coins_ret20_rankcorr_pos"] = f"{int((pc>0).sum())} of {int(pc.notna().sum())}, median {pc.median():.3f}"
            pn = d.dropna(subset=["near"]).groupby("coin").apply(lambda g: g["near"].corr(g["u"], method="spearman"))
            out["H20_coins_near_rankcorr_pos"] = f"{int((pn>0).sum())} of {int(pn.notna().sum())}, median {pn.median():.3f}"
    return out
