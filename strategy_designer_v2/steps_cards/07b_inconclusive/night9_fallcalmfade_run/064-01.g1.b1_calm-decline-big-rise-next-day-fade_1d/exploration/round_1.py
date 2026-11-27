def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    allret = {}
    for coin, wins in bars.items():
        dr = []
        for w, df in wins.items():
            c = df["close"].values
            dr.append(pd.Series(c).pct_change().dropna())
        allret[coin] = pd.concat(dr)
    drift = {k: v.mean() for k, v in allret.items()}
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            reg = df["regime"].values
            col = "debug_info.components.scaled_rise.last_history_value"
            vsr = df[col].values if col in df else np.full(len(df), np.nan)
            r1 = pd.Series(c).pct_change().values
            sd20 = pd.Series(r1).rolling(20).std().values
            raw = r1 / sd20
            shallow = 0.0
            for t in range(len(df)):
                if f[t] >= 0:
                    shallow = 0.0
                    continue
                if f[t] > shallow:
                    shallow = f[t]
                if f[t] <= shallow - 2 and reg[t] == "mean_reversion":
                    rec = {"coin": coin, "w": w, "day": t, "dayts": str(df["timestamp"].iloc[t])[:10],
                           "vsr": vsr[t] if not np.isnan(vsr[t]) else raw[t], "fc": f[t],
                           "year": pd.Timestamp(df["timestamp"].iloc[t]).year,
                           "rawret": r1[t]}
                    for h in (1, 2, 3, 5, 10):
                        if t + h < len(df):
                            rec[f"u{h}"] = -(c[t+h]/c[t]-1 - h*drift[coin])
                            rec[f"tot{h}"] = -(c[t+h]/c[t]-1)
                        else:
                            rec[f"u{h}"] = np.nan; rec[f"tot{h}"] = np.nan
                    rows.append(rec)
                    shallow = f[t]
    d = pd.DataFrame(rows)
    def tday(s, g):
        x = pd.DataFrame({"v": s, "g": g}).dropna().groupby("g")["v"].sum()
        # per-day summed deviations: t of mean
        return x.mean()/(x.std(ddof=1)/np.sqrt(len(x))) if len(x) > 2 else np.nan
    hz = []
    for h in (1, 2, 3, 5, 10):
        s = d[f"u{h}"]
        hz.append({"h": h, "n": s.notna().sum(), "mean_unusual": s.mean(), "t_day": tday(s, d["dayts"]),
                   "mean_total": d[f"tot{h}"].mean(), "share_pos": (s > 0).mean()})
    out = {"horizons": pd.DataFrame(hz)}
    d["q"] = pd.qcut(d["vsr"], 4, labels=["q1", "q2", "q3", "q4"])
    g = d.groupby("q").agg(n=("u1", "size"), vsr=("vsr", "mean"), u1=("u1", "mean"), u2=("u2", "mean"),
                            u3=("u3", "mean"), u5=("u5", "mean"))
    out["by_quartile"] = g
    out["by_coin"] = d.groupby("coin").agg(n=("u1", "size"), u1=("u1", "mean"), u3=("u3", "mean"), u5=("u5", "mean"))
    out["by_window"] = d.groupby("w").agg(n=("u1", "size"), u1=("u1", "mean"), u3=("u3", "mean"), u5=("u5", "mean"))
    out["by_year"] = d.groupby("year").agg(n=("u1", "size"), u1=("u1", "mean"), u3=("u3", "mean"), u5=("u5", "mean"))
    out["corr_vsr_u"] = pd.Series({f"u{h}": stats.spearmanr(d["vsr"], d[f"u{h}"], nan_policy="omit")[0] for h in (1,2,3,5,10)})
    out["counts"] = pd.Series({"cases": len(d), "days": d["dayts"].nunique(), "vsr_median": d["vsr"].median()})
    return out
