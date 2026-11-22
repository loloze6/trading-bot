import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    wk_rows = []; ctrl_rows = []; hr_rows = []; mv_rows = []
    for coin in bars:
        # usual 48h and 24h std per coin, on grid
        r48 = []; r24 = []; r1 = []
        for w, df in bars[coin].items():
            c = df["close"].values
            r48 += list(c[48::48][:len(c[0::48])-1] / c[0::48][:len(c[48::48])] - 1) if len(c) > 48 else []
            g = c[0::24]; r24 += list(g[1:] / g[:-1] - 1)
            r1 += list(c[1:] / c[:-1] - 1)
        s48 = np.std(r48); m48 = np.mean(r48); s24 = np.std(r24); m24 = np.mean(r24); s1 = np.std(r1); m1 = np.mean(r1)
        for w, df in bars[coin].items():
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            c = df["close"].values.astype(float); n = len(c)
            lr = np.r_[np.nan, np.diff(np.log(c))]
            dow = ts.dt.dayofweek.values; hr = ts.dt.hour.values
            tsv = ts.values
            def ok(a, b, h):
                return 0 <= a < n and 0 <= b < n and (tsv[b] - tsv[a]) == np.timedelta64(h, 'h')
            for target, rows in ((6, wk_rows), (1, ctrl_rows), (2, ctrl_rows)):
                for i in np.where((dow == target) & (hr == 23))[0]:
                    if not (ok(i - 216, i, 216) and ok(i, i + 48, 48)): continue
                    past = c[i] / c[i - 48] - 1
                    sat = c[i - 24] / c[i - 48] - 1; sun = c[i] / c[i - 24] - 1
                    vr = np.nanstd(lr[i - 47:i + 1]) / np.nanstd(lr[i - 215:i - 47])
                    f24 = c[i + 24] / c[i] - 1; f48 = c[i + 48] / c[i] - 1
                    rows.append(dict(coin=coin, day=target, past=past / s48, sat=sat / s48, sun=sun / s48, vr=vr,
                                     f24=(f24 - m48 / 2) / s48, f48=(f48 - m48) / s48))
            # hourly
            hr_rows.append(pd.DataFrame({"hr": hr[1:], "dow": dow[1:], "z": ((c[1:] / c[:-1] - 1) - m1) / s1,
                                         "gap": (np.diff(tsv) == np.timedelta64(1, 'h'))}))
            # 24h grid moves
            g = np.arange(0, n, 24)
            gc = c[g]; rr = gc[1:] / gc[:-1] - 1
            vol = pd.Series(lr).rolling(168).std().values[g]
            for k in range(1, len(rr)):
                mv_rows.append(dict(coin=coin, past=(rr[k - 1] - m24) / s24, nxt=(rr[k] - m24) / s24, vol=vol[k] / s1 if np.isfinite(vol[k]) else np.nan))
    W = pd.DataFrame(wk_rows); C = pd.DataFrame(ctrl_rows)
    def reg(D, x, y):
        D = D.dropna(subset=[x, y]); s = stats.linregress(D[x], D[y]); return pd.Series(dict(n=len(D), slope=s.slope, t=s.slope / s.stderr))
    out["weekend_reg"] = pd.DataFrame({"wk past->f48": reg(W, "past", "f48"), "wk past->f24": reg(W, "past", "f24"),
        "wk sat->f48": reg(W, "sat", "f48"), "wk sun->f48": reg(W, "sun", "f48"),
        "ctrl past->f48": reg(C, "past", "f48"), "ctrl past->f24": reg(C, "past", "f24")}).T
    W["vrq"] = pd.qcut(W["vr"], 3, labels=["lo", "mid", "hi"])
    W["sg"] = np.sign(W["past"]) * W["f48"]
    out["weekend_by_vr"] = W.groupby("vrq").agg(n=("sg", "size"), mean_signed=("sg", "mean"), sd=("sg", "std"))
    out["weekend_by_vr"]["t"] = out["weekend_by_vr"].mean_signed / (out["weekend_by_vr"].sd / np.sqrt(out["weekend_by_vr"].n))
    W["pq"] = pd.qcut(W["past"], 5, labels=False)
    out["weekend_by_pastq"] = W.groupby("pq").agg(n=("f48", "size"), past=("past", "mean"), f48=("f48", "mean"), sd=("f48", "std"))
    out["weekend_by_coin"] = W.groupby("coin").apply(lambda d: reg(d, "past", "f48"))
    H = pd.concat(hr_rows); H = H[H.gap]
    g = H.groupby("hr")["z"].agg(["size", "mean", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["size"]))
    out["hour_z"] = g[["size", "mean", "t"]]
    g = H.groupby("dow")["z"].agg(["size", "mean", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["size"]))
    out["dow_z"] = g[["size", "mean", "t"]]
    M = pd.DataFrame(mv_rows).dropna()
    M["pq"] = pd.qcut(M["past"], 5, labels=False); M["vq"] = pd.qcut(M["vol"], 3, labels=False)
    g = M.groupby("pq")["nxt"].agg(["size", "mean", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["size"]))
    out["24h_next_by_pastq"] = g
    out["24h_reg_by_volq"] = M.groupby("vq").apply(lambda d: reg(d, "past", "nxt"))
    g = M.groupby("vq")["nxt"].agg(["size", "mean", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["size"])); out["24h_next_by_volq"] = g
    # book
    D = []
    for coin in days:
        for w, d in days[coin].items():
            dd = d.dropna(subset=["book_return", "coin_return"]).copy(); dd["dow"] = pd.to_datetime(dd["day"]).dt.dayofweek; dd["coin"] = coin; D.append(dd)
    D = pd.concat(D)
    g = D.groupby("dow").agg(n=("book_return", "size"), book=("book_return", "mean"), coin=("coin_return", "mean"))
    out["book_by_dow"] = g
    q_hi = D.book_return.quantile(0.99); q_lo = D.book_return.quantile(0.01)
    out["book_extremes"] = pd.DataFrame({"top1pct": D[D.book_return >= q_hi].groupby("dow").size(), "bot1pct": D[D.book_return <= q_lo].groupby("dow").size()}).fillna(0)
    out["book_extremes_sums"] = pd.Series(dict(sum_top=D[D.book_return >= q_hi].book_return.sum(), sum_bot=D[D.book_return <= q_lo].book_return.sum(), sum_all=D.book_return.sum()))
    return out
