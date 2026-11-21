import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    for H in [5, 10, 20]:
        rows = []
        for coin, wins in data["bars"].items():
            allr = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - H, H)
                allr.extend(list(c[idx + H] / c[idx] - 1))
            allr = np.array(allr); drift, sd = allr.mean(), allr.std(ddof=1)
            for w, b in wins.items():
                b = b.reset_index(drop=True); c = b["close"]
                f = pd.DataFrame({
                    "coin": coin, "win": w,
                    "fwd": c.shift(-H) / c - 1,
                    "d_sma20": c / c.rolling(20).mean() - 1,
                    "d_hi30": c / b["high"].rolling(30).max() - 1,
                    "past10": c / c.shift(10) - 1,
                    "vol20": c.pct_change().rolling(20).std(),
                    "below50": (b["regime"] == "trending").astype(float),
                    "fc": b["forecast"],
                    "yr": pd.to_datetime(b["timestamp"]).dt.year,
                })
                f = f.iloc[np.arange(0, len(f), H)].dropna(subset=["fwd", "d_sma20"])
                f["un"] = (f["fwd"] - drift) / sd
                f["unraw"] = f["fwd"] - drift
                f["z"] = f["d_sma20"] / f["vol20"]
                rows.append(f)
        g = pd.concat(rows)
        g["q"] = g.groupby("coin")["d_sma20"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        t = g.groupby("q").agg(un=("un", "mean"), unraw=("unraw", "mean"), n=("un", "count"))
        rho = stats.spearmanr(g["d_sma20"], g["un"])
        rhoz = stats.spearmanr(g["z"], g["un"], nan_policy="omit")
        t["spearman_rho"] = rho.correlation; t["spearman_p"] = rho.pvalue
        t["rho_z"] = rhoz.correlation; t["p_z"] = rhoz.pvalue
        out[f"H{H}_dsma20_q"] = t
        if H == 10:
            # by coin: top quintile minus rest, and spearman
            rc = []
            for coin, d in g.groupby("coin"):
                r = stats.spearmanr(d["d_sma20"], d["un"])
                top = d[d.q == 4]["un"]
                rc.append(pd.Series({"rho": r.correlation, "p": r.pvalue,
                                     "top_un": top.mean(), "top_t": top.mean() / (top.std() / np.sqrt(len(top))),
                                     "n": len(d)}, name=coin))
            out["H10_by_coin"] = pd.DataFrame(rc)
            ry = []
            for yr, d in g.groupby("yr"):
                if len(d) < 30: continue
                r = stats.spearmanr(d["d_sma20"], d["un"])
                ry.append(pd.Series({"rho": r.correlation, "p": r.pvalue,
                                     "top_un": d[d.q == 4]["un"].mean(), "n": len(d)}, name=yr))
            out["H10_by_year"] = pd.DataFrame(ry)
            rb = []
            for reg, d in g.groupby("below50"):
                r = stats.spearmanr(d["d_sma20"], d["un"])
                rb.append(pd.Series({"rho": r.correlation, "p": r.pvalue,
                                     "top_un": d[d.q == 4]["un"].mean(), "n_top": (d.q == 4).sum()}, name=reg))
            out["H10_by_below50"] = pd.DataFrame(rb)
            # short-signal cases: mean d_sma20 quintile and outcome by quintile
            s = g[g.fc <= -2]
            out["H10_short_cases_by_q"] = s.groupby("q")["un"].agg(["mean", "count"])
    # book around its largest gains and losses (daily)
    bk = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            dd = dd.reset_index(drop=True)
            bk.append(pd.DataFrame({"br": dd["book_return"], "cr": dd["coin_return"],
                                    "cr_prev5": dd["close"].pct_change(5).shift(1)}))
    bk = pd.concat(bk).dropna()
    bk["bq"] = pd.qcut(bk["br"].rank(method="first"), 10, labels=False)
    out["book_deciles_vs_prior_coin5d"] = bk.groupby("bq").agg(br=("br", "mean"), cr=("cr", "mean"),
                                                               prev5=("cr_prev5", "mean"), n=("br", "count"))
    return out
