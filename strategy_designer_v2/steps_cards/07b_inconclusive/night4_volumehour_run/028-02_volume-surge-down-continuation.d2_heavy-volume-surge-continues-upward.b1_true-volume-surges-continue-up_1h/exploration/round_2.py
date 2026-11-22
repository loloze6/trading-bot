import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            r1 = pd.Series(c).pct_change()
            sd = r1.rolling(720, min_periods=240).std()
            vr = (b["volume"] / b["volume"].rolling(720, min_periods=240).mean()).values
            zr = (r1 / sd).values
            year = pd.to_datetime(b["timestamp"]).dt.year.values
            n = len(b)
            for h in (2, 4, 6, 12, 24):
                idx = np.arange(0, n - h, h)
                fr = c[idx + h] / c[idx] - 1
                for i, f in zip(idx, fr):
                    rows.append((coin, w, year[i], h, zr[i], vr[i], f))
    df = pd.DataFrame(rows, columns=["coin", "w", "year", "h", "zr", "vr", "fr"])
    df["drift"] = df.groupby(["coin", "h"])["fr"].transform("mean")
    df["ex"] = df["fr"] - df["drift"]
    df["usual"] = df.groupby(["coin", "h"])["fr"].transform("std")
    d = df.dropna(subset=["zr", "vr"]).copy()
    d["score_dn"] = np.clip(-d.zr, 0, None) * d.vr
    d["score_up"] = np.clip(d.zr, 0, None) * d.vr
    def agg(g):
        m = g["ex"].mean(); s = g["ex"].std(); n = len(g)
        return pd.Series({"n": n, "mean_ex_bp": m * 1e4, "t": m / (s / np.sqrt(n)) if n > 2 else np.nan,
                          "strength": (g["ex"] / g["usual"]).mean(),
                          "w_mean_bp": 1e4 * (g["ex"] * g["w"]).sum() / g["w"].sum()})
    out = {}
    for side in ("dn", "up"):
        tab = []
        for h in (2, 4, 6, 12, 24):
            g = d[(d.h == h) & (d[f"score_{side}"] > 0)].copy()
            thr = g[f"score_{side}"].quantile([0.9, 0.97, 0.99]).values
            for q, th in zip(("top10", "top3", "top1"), thr):
                gg = g[g[f"score_{side}"] >= th].assign(w=lambda x: x[f"score_{side}"])
                r = agg(gg); r["h"] = h; r["q"] = q; tab.append(r)
        out[f"{side}_score_tops_by_h"] = pd.DataFrame(tab).set_index(["h", "q"]).round(3)
    g = d[(d.h == 12) & (d.score_dn > 0)].copy()
    th = g.score_dn.quantile(0.97)
    gg = g[g.score_dn >= th].assign(w=lambda x: x.score_dn)
    out["dn_top3_h12_by_coin"] = gg.groupby("coin").apply(agg).round(3)
    out["dn_top3_h12_by_year"] = gg.groupby("year").apply(agg).round(3)
    g6 = d[(d.h == 6) & (d.score_dn > 0)].copy()
    th6 = g6.score_dn.quantile(0.97)
    gg6 = g6[g6.score_dn >= th6].assign(w=lambda x: x.score_dn)
    out["dn_top3_h6_by_coin"] = gg6.groupby("coin").apply(agg).round(3)
    out["dn_top3_h6_by_year"] = gg6.groupby("year").apply(agg).round(3)
    # graded: spearman of score_dn vs ex among top 10%
    res = {}
    for h in (4, 6, 12, 24):
        g = d[(d.h == h) & (d.score_dn > 0)]
        g = g[g.score_dn >= g.score_dn.quantile(0.9)]
        rho, p = stats.spearmanr(g.score_dn, g.ex)
        res[h] = (round(rho, 3), round(p, 3), len(g))
    out["dn_top10_spearman"] = pd.DataFrame(res, index=["rho", "p", "n"]).T
    return out
