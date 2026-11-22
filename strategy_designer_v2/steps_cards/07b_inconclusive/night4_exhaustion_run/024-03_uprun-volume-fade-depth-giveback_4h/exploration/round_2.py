import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = [6, 12, 18, 36]
    rows = []
    for coin, wins in bars.items():
        drift = {}
        usual = {}
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            rs = np.concatenate(rs)
            drift[h] = rs.mean(); usual[h] = rs.std()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; v = df["volume"].values
            n = len(c)
            r = np.r_[np.nan, c[1:] / c[:-1] - 1]
            absm = pd.Series(np.abs(r)).rolling(180, min_periods=45).mean().values
            up_len = np.zeros(n, int); dn_len = np.zeros(n, int)
            for i in range(1, n):
                if r[i] > 0: up_len[i] = up_len[i-1] + 1
                if r[i] < 0: dn_len[i] = dn_len[i-1] + 1
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for side, L_arr, sgn in (("dn", dn_len, 1), ("up", up_len, -1)):
                for cell in range(0, n, 18):
                    hit = None
                    for i in range(cell, min(cell + 18, n)):
                        L = L_arr[i]
                        if L >= 2 and not np.isnan(absm[i]):
                            hit = i; break
                    if hit is None: continue
                    i = hit; L = L_arr[i]
                    g = abs(np.sum(r[i-L+1:i+1])) / absm[i]
                    fade = np.log(max(v[i-L+1], 1e-12) / max(v[i], 1e-12))
                    rec = dict(coin=coin, w=w, side=side, L=L, g=g, vf=fade, yr=yr[i])
                    for h in H:
                        if i + h < n:
                            ret = c[i+h] / c[i] - 1
                            rec[f"u{h}"] = sgn * (ret - drift[h])
                            rec[f"tot{h}"] = sgn * ret
                            rec[f"s{h}"] = rec[f"u{h}"] / usual[h]
                        else:
                            rec[f"u{h}"] = np.nan; rec[f"tot{h}"] = np.nan; rec[f"s{h}"] = np.nan
                    rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g, col="u18"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "tot": g["tot18"].dropna().mean(), "str": g["s18"].dropna().mean()})
    out = {}
    for side in ("dn", "up"):
        s = d[d.side == side].copy()
        s["gq"] = pd.qcut(s["g"].rank(method="first"), 5, labels=False)
        s["vfq"] = pd.qcut(s["vf"].rank(method="first"), 3, labels=False)
        out[f"{side} horizons all"] = pd.DataFrame({h: summ(s, f"u{h}") for h in H}).T
        out[f"{side} by size quintile"] = s.groupby("gq").apply(summ)
        out[f"{side} top2 size q by fade tercile"] = s[s.gq >= 3].groupby("vfq").apply(summ)
        out[f"{side} top2 size q by year"] = s[s.gq >= 3].groupby("yr").apply(summ)
        out[f"{side} top2 size q by coin"] = s[s.gq >= 3].groupby("coin").apply(summ)
    return out
