def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    comps = ["combined","s_momentum","s_reversal","s_high","s_volatility"]
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(b)
            for i in range(0, n - 5, 5):
                r = c[i+5]/c[i]-1
                d = {"coin": coin, "win": w, "year": pd.Timestamp(b["timestamp"].iloc[i]).year, "r": r}
                for k in comps:
                    d[k] = b.get(f"debug_info.components.{k}.last_history_value", pd.Series([np.nan]*n)).iloc[i]
                d["pp"] = b.get("debug_info.components.combined.post_pipeline_value", pd.Series([np.nan]*n)).iloc[i]
                rows.append(d)
    df = pd.DataFrame(rows)
    df["mu"] = df.groupby("coin")["r"].transform("mean")
    df["u"] = df["r"] - df["mu"]
    out = {}
    summ = []
    for k in comps:
        s = df.dropna(subset=[k])
        q = s[k].abs().quantile(0.9)
        t = s[s[k].abs() >= q]
        su = np.sign(t[k]) * t["u"]
        summ.append({"comp": k, "n": len(t), "mean": su.mean(), "t": su.mean()/(su.std()/np.sqrt(len(t))),
                     "long_share": (t[k] > 0).mean(),
                     "mean_long": su[t[k] > 0].mean(), "mean_short": su[t[k] < 0].mean(),
                     "all_cells_corr": np.corrcoef(s[k], s["u"])[0,1]})
        if k in ("combined","s_reversal","s_momentum"):
            g = pd.DataFrame({"su": su, "coin": t["coin"], "year": t["year"]})
            out[f"{k}_top_by_coin"] = g.groupby("coin")["su"].agg(["count","mean"])
            out[f"{k}_top_by_year"] = g.groupby("year")["su"].agg(["count","mean"])
    out["top10_summary"] = pd.DataFrame(summ)
    s = df.dropna(subset=["combined"]).copy()
    s["su"] = np.sign(s["combined"]) * s["u"]
    s["dec"] = pd.qcut(s["combined"].abs(), 10, labels=False)
    out["combined_abs_decile"] = s.groupby("dec")["su"].agg(["count","mean","std"])
    s["sdec"] = pd.qcut(s["combined"], 10, labels=False)
    out["combined_signed_decile_raw_u"] = s.groupby("sdec")["u"].agg(["count","mean"])
    for k in ["s_reversal","s_momentum","s_high","s_volatility"]:
        x = df.dropna(subset=[k]).copy()
        x["sdec"] = pd.qcut(x[k], 5, labels=False)
        out[f"{k}_signed_quintile_u"] = x.groupby("sdec")["u"].agg(["count","mean"])
    return out
