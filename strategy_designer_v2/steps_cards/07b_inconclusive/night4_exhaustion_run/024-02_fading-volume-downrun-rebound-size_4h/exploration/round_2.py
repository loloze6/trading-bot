def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [6, 12, 18]
    rows = []
    for coin in bars:
        d = {}
        for h in H:
            rs = []
            for w, df in bars[coin].items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            rs = np.array(rs); d[h] = (np.nanmean(rs), np.nanstd(rs))
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values; v = df["volume"].values
            f = df["forecast"].fillna(0).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(df)
            ret1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            absr = pd.Series(np.abs(ret1)).rolling(180, min_periods=45).mean().values
            slen = np.zeros(n, int); sloss = np.full(n, np.nan)
            L = 0
            for i in range(1, n):
                L = L + 1 if c[i] < c[i - 1] else 0
                slen[i] = L
                if L >= 2 and absr[i] > 0:
                    sloss[i] = (c[i - L] - c[i]) / c[i - L] / absr[i]
            lo = 0.0; used = set()
            for i in range(n):
                if f[i] <= 0:
                    lo = 0.0; continue
                if f[i] - lo >= 2:
                    cell = i // 18; lo = f[i]
                    if cell not in used and i + 18 < n:
                        used.add(cell)
                        rec = dict(coin=coin, yr=yr[i], f=f[i], sloss=sloss[i])
                        for h in H:
                            rec["u%d" % h] = c[i + h] / c[i] - 1 - d[h][0]
                            rec["s%d" % h] = rec["u%d" % h] / d[h][1]
                            rec["tot%d" % h] = c[i + h] / c[i] - 1
                        rows.append(rec)
                else:
                    lo = min(lo, f[i])
    C = pd.DataFrame(rows).dropna(subset=["sloss"])
    def summ(g, col="u18"):
        x = g[col].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    q80 = C.sloss.quantile(0.8); q90 = C.sloss.quantile(0.9)
    T = C[C.sloss >= q80]
    out = {}
    out["thresholds"] = pd.Series(dict(q80=q80, q90=q90))
    out["top20_by_h"] = pd.DataFrame({h: summ(T, "u%d" % h) for h in H}).T
    out["top20_strength_total"] = T[["s6", "s12", "s18", "tot18"]].mean()
    out["top10_by_h"] = pd.DataFrame({h: summ(C[C.sloss >= q90], "u%d" % h) for h in H}).T
    out["top20_by_coin"] = T.groupby("coin").apply(summ)
    out["top20_by_year"] = T.groupby("yr").apply(summ)
    out["corr_sloss_u18"] = pd.Series(dict(pearson=C.sloss.corr(C.u18), spearman=C.sloss.corr(C.u18, method="spearman"),
                                           spearman_f=C.f.corr(C.u18, method="spearman")))
    C["dq"] = pd.qcut(C.sloss.rank(method="first"), 10, labels=False)
    out["by_decile"] = C.groupby("dq").apply(lambda g: pd.concat([summ(g), pd.Series({"sloss": g.sloss.mean()})]))
    return out
