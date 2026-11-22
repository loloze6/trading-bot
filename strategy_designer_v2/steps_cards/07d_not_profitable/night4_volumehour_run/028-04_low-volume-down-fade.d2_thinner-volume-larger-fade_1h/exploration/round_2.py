import numpy as np, pandas as pd

def explore(data):
    out = {}
    H = [6, 24, 48]
    drift, usual = {}, {}
    for coin, ws in data["bars"].items():
        for h in H:
            rs = []
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            x = np.concatenate(rs); drift[(coin, h)] = x.mean(); usual[(coin, h)] = x.std()
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; n = len(c)
            f = b["forecast"].fillna(0).values
            z = b["debug_info.components.fall.last_history_value"].values
            zv = b["debug_info.components.fall_x_volume.last_history_value"].values
            v = np.where(np.abs(z) > 1e-12, zv / z, np.nan)
            for cell in range(0, n, 6):
                seg = np.where(f[cell:cell + 6] >= 2)[0]
                if len(seg) == 0: continue
                t = cell + seg[0]
                if t < 168: continue
                r = {"coin": coin, "year": b["timestamp"].iloc[t].year, "z": z[t], "v": v[t],
                     "p168": c[t] / c[t - 168] - 1, "p24": c[t] / c[t - 24] - 1}
                for h in H:
                    r[f"u{h}"] = (c[t+h]/c[t]-1-drift[(coin,h)]) if t+h < n else np.nan
                    r[f"s{h}"] = r[f"u{h}"]/usual[(coin,h)]
                rows.append(r)
    d = pd.DataFrame(rows)
    def summ(g):
        s = {"n": len(g)}
        for h in H:
            x = g[f"u{h}"].dropna()
            s[f"u{h}"] = x.mean(); s[f"t{h}"] = x.mean()/(x.std()/np.sqrt(len(x))); s[f"str{h}"] = g[f"s{h}"].mean()
        return pd.Series(s)
    d["pq"] = pd.qcut(d["p168"].rank(method="first"), 5, labels=False)
    d["zq"] = pd.qcut(d["z"].rank(method="first"), 3, labels=False)
    out["p7d_q_x_fall_terc(0=deepest)"] = d.groupby(["pq", "zq"]).apply(summ)
    out["top_p7d_by_year"] = d[d.pq == 4].groupby("year").apply(summ)
    out["bottom_p7d_by_year"] = d[d.pq == 0].groupby("year").apply(summ)
    out["p7d_q_mean"] = d.groupby("pq")["p168"].mean()
    out["corr_p168_u48"] = d[["p168", "u48"]].corr().iloc[0, 1]
    # daily book by window
    bw = []
    for coin, ws in data["days"].items():
        for w, dd in ws.items():
            bw.append({"coin": coin, "w": int(w[1:]), "book": dd["book_return"].mean(), "coin_r": dd["coin_return"].mean()})
    bw = pd.DataFrame(bw).groupby("w")[["book", "coin_r"]].mean()
    out["book_by_window"] = bw
    return out
