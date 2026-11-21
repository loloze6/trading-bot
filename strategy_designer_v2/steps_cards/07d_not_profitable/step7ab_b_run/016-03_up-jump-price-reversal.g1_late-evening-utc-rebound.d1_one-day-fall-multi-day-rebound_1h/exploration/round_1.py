def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # book daily returns: mean over coins per (window, day)
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["window"] = w
            rows.append(dd)
    D = pd.concat(rows)
    B = D.groupby(["window", "day"])[["book_return", "coin_return"]].mean().reset_index()
    B["wn"] = B["window"].str[1:].astype(int)
    B = B.sort_values(["wn", "day"])
    r = B["book_return"].fillna(0).values
    eq = np.cumprod(1 + r); peak = np.maximum.accumulate(eq); dd = eq / peak - 1
    B["dd"] = dd
    out["deepest_fall"] = float(dd.min())
    # per window: book return, coin return, min dd within window chain
    pw = B.groupby("wn").agg(book=("book_return", lambda x: (1 + x.fillna(0)).prod() - 1),
                             hold=("coin_return", lambda x: (1 + x.fillna(0)).prod() - 1),
                             worst_day=("book_return", "min"), dd_min=("dd", "min"))
    out["per_window"] = pw.round(4)
    # grid cases: forecast>0, 72h forward, conditioned on features
    recs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl = b["close"].values; vol = b["volume"].values; n = len(cl)
            hr = np.r_[np.nan, cl[1:] / cl[:-1] - 1]
            for i in range(0, n - 72, 72):
                if i < 720: continue
                f = b["forecast"].values[i]
                r24 = cl[i] / cl[i - 24] - 1
                r30 = cl[i] / cl[i - 720] - 1
                r7 = cl[i] / cl[i - 168] - 1
                h = hr[i - 23:i + 1]
                jump = np.nanmax(np.abs(h)) / (np.nansum(np.abs(h)) + 1e-12)
                eff = abs(r24) / (np.nansum(np.abs(h)) + 1e-12)
                v = vol[i - 23:i + 1]; vs = np.nanmax(v) / (np.nansum(v) + 1e-12)
                vol30 = np.nanstd(hr[i - 719:i + 1])
                fwd = cl[i + 72] / cl[i] - 1
                recs.append((c, w, f, r24, r30, r7, jump, eff, vs, vol30, fwd))
    G = pd.DataFrame(recs, columns=["coin", "w", "f", "r24", "r30", "r7", "jump", "eff", "vshare", "vol30", "fwd"])
    G["ex"] = G["fwd"] - G.groupby("coin")["fwd"].transform("mean")
    A = G[G.f > 0].copy()
    out["n_active"] = len(A)
    def tab(col, q=4):
        A["q"] = pd.qcut(A[col], q, labels=False, duplicates="drop")
        t = A.groupby("q").agg(n=("ex", "size"), mean_fwd=("fwd", "mean"), mean_ex=("ex", "mean"),
                               t=("ex", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))),
                               p10=("fwd", lambda x: x.quantile(0.1)))
        return t.round(4)
    for col in ["f", "r30", "r7", "jump", "eff", "vshare", "vol30"]:
        out["by_" + col] = tab(col)
    # flat cases for comparison by r30
    F = G[G.f <= 0].copy()
    F["q"] = pd.qcut(F["r30"], 4, labels=False)
    out["flat_by_r30"] = F.groupby("q")["ex"].agg(["size", "mean"]).round(4)
    # worst 5% of book days: coin state
    thr = B["book_return"].quantile(0.03)
    out["worst_days_share_of_loss"] = float(B.loc[B.book_return <= thr, "book_return"].sum() / B["book_return"].sum())
    return out
