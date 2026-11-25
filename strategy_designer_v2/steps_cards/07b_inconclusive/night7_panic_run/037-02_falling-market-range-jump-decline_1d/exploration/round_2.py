def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        dr = {}
        for h in (3, 5):
            vals = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                vals += list(c[idx + h] / c[idx] - 1)
            dr[h] = np.mean(vals)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            lr = pd.Series(np.log(c)).diff()
            vol30 = lr.rolling(30).std()
            volpct = vol30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            ret60 = pd.Series(c) / pd.Series(c).shift(60) - 1
            rm = df.get("debug_info.components.range_mult.last_history_value")
            sit = (df["regime"] == "trending").values
            seen = set()
            for i in np.where(sit)[0]:
                cell = i // 3
                if cell in seen:
                    continue
                seen.add(cell)
                r = {"coin": coin, "ts": df["timestamp"].iloc[i],
                     "rm": rm.iloc[i] if rm is not None else np.nan,
                     "volpct": volpct.iloc[i], "ret60": ret60.iloc[i]}
                for h in (3, 5):
                    r[f"ex{h}"] = -(c[i + h] / c[i] - 1 - dr[h]) if i + h < n else np.nan
                    r[f"tot{h}"] = -(c[i + h] / c[i] - 1) if i + h < n else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    def summ(g, col="ex3"):
        g = g.dropna(subset=[col])
        if len(g) < 3:
            return pd.Series({"n": len(g), "mean": g[col].mean(), "t": np.nan})
        gd = g.groupby("ts")[col].sum()
        t = gd.sum() / (np.sqrt(len(gd)) * gd.std()) if gd.std() > 0 else np.nan
        return pd.Series({"n": len(g), "mean": g[col].mean(), "t": t})
    out = {}
    d["agit"] = np.where(d["volpct"] > 0.5, "agitated", np.where(d["volpct"].notna(), "calm", "na"))
    out["by_agitation"] = d.groupby("agit").apply(summ)
    out["by_agitation_h5"] = d.groupby("agit").apply(lambda g: summ(g, "ex5"))
    d["r60q"] = pd.qcut(d["ret60"], 3, duplicates="drop")
    out["by_fall_depth"] = d.groupby("r60q").apply(summ)
    out["total_move_h3"] = summ(d, "tot3").to_frame().T
    x = d.dropna(subset=["rm", "ex3"])
    out["corr_rm_ex3"] = float(np.corrcoef(x["rm"], x["ex3"])[0, 1])
    d["rmq"] = pd.qcut(d["rm"], 4, duplicates="drop")
    out["agit_x_rm"] = d[d.agit != "na"].groupby(["agit", "rmq"]).apply(summ)
    return out
