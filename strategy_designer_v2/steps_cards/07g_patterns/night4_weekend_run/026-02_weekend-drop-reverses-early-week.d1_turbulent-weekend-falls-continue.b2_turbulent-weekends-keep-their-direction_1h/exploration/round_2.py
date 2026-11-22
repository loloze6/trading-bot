import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    W = []; M = []; H = []
    for coin in bars:
        r48 = []; r24 = []; r1 = []
        for w, df in bars[coin].items():
            c = df["close"].values.astype(float)
            g = c[0::48]; r48 += list(g[1:] / g[:-1] - 1)
            g = c[0::24]; r24 += list(g[1:] / g[:-1] - 1)
            r1 += list(c[1:] / c[:-1] - 1)
        s48, m48, s24, m24, s1, m1 = np.std(r48), np.mean(r48), np.std(r24), np.mean(r24), np.std(r1), np.mean(r1)
        for w, df in bars[coin].items():
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            c = df["close"].values.astype(float); n = len(c); tsv = ts.values
            lr = np.r_[np.nan, np.diff(np.log(c))]
            dow = ts.dt.dayofweek.values; hr = ts.dt.hour.values; yr = ts.dt.year.values
            def ok(a, b, h): return 0 <= a < n and 0 <= b < n and (tsv[b] - tsv[a]) == np.timedelta64(h, 'h')
            for i in np.where(hr == 23)[0]:
                if not (ok(i - 48, i, 48) and ok(i, i + 48, 48)): continue
                W.append(dict(coin=coin, win=w, yr=yr[i], day=dow[i],
                              d1=(c[i - 24] / c[i - 48] - 1) / s24, d0=(c[i] / c[i - 24] - 1) / s24,
                              f24=(c[i + 24] / c[i] - 1 - m24) / s24, f48=(c[i + 48] / c[i] - 1 - m48) / s48))
            g = np.arange(0, n, 24); gc = c[g]; rr = gc[1:] / gc[:-1] - 1
            vol = pd.Series(lr).rolling(168).std().values[g]
            for k in range(1, len(rr)):
                if np.isfinite(vol[k]):
                    M.append(dict(coin=coin, yr=yr[g[k]], past=(rr[k - 1] - m24) / s24, nxt=(rr[k] - m24) / s24, vol=vol[k] / s1))
            gap = np.r_[False, np.diff(tsv) == np.timedelta64(1, 'h')]
            z = np.r_[np.nan, (c[1:] / c[:-1] - 1 - m1) / s1]
            H.append(pd.DataFrame({"coin": coin, "yr": yr, "hr": hr, "dow": dow, "z": z})[gap])
    W = pd.DataFrame(W); M = pd.DataFrame(M); H = pd.concat(H)
    def reg(D, x, y):
        D = D.dropna(subset=[x, y])
        if len(D) < 20: return pd.Series(dict(n=len(D), slope=np.nan, t=np.nan))
        s = stats.linregress(D[x], D[y]); return pd.Series(dict(n=len(D), slope=s.slope, t=s.slope / s.stderr))
    # last-24h return reversal by day of week (day = day of the bar at 23:00)
    out["last24_to_f24_by_dow"] = W.groupby("day").apply(lambda d: reg(d, "d0", "f24"))
    out["last24_to_f48_by_dow"] = W.groupby("day").apply(lambda d: reg(d, "d0", "f48"))
    out["prev24_to_f48_by_dow"] = W.groupby("day").apply(lambda d: reg(d, "d1", "f48"))
    S = W[W.day == 6]
    out["sun_by_coin"] = S.groupby("coin").apply(lambda d: reg(d, "d0", "f48"))
    out["sun_by_year"] = S.groupby("yr").apply(lambda d: reg(d, "d0", "f48"))
    out["sat_by_coin"] = S.groupby("coin").apply(lambda d: reg(d, "d1", "f48"))
    out["sat_by_year"] = S.groupby("yr").apply(lambda d: reg(d, "d1", "f48"))
    S = S.copy(); S["sq"] = pd.qcut(S["d0"], 5, labels=False)
    out["sun_quintiles_f48"] = S.groupby("sq").agg(n=("f48", "size"), sun=("d0", "mean"), f48=("f48", "mean"), sd=("f48", "std"))
    # high-vol 24h reversal
    M["vq"] = pd.qcut(M["vol"], 5, labels=False)
    out["rev24_by_vol5"] = M.groupby("vq").apply(lambda d: reg(d, "past", "nxt"))
    Hv = M[M.vq == 4]
    out["rev24_topvol_by_coin"] = Hv.groupby("coin").apply(lambda d: reg(d, "past", "nxt"))
    out["rev24_topvol_by_year"] = Hv.groupby("yr").apply(lambda d: reg(d, "past", "nxt"))
    # hour 21-22 stability
    Q = H[H.hr.isin([21, 22])]
    g = Q.groupby("coin")["z"].agg(["size", "mean", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["size"])); out["h2122_by_coin"] = g
    g = Q.groupby("yr")["z"].agg(["size", "mean", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["size"])); out["h2122_by_year"] = g
    g = Q.groupby("dow")["z"].agg(["size", "mean", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["size"])); out["h2122_by_dow"] = g
    return out
