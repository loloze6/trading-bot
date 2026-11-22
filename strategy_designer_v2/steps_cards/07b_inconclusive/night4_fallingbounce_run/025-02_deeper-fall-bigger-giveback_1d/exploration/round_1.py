def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        r5 = []
        for w, df in ws.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 5, 5)
            r5 += list(c[idx + 5] / c[idx] - 1)
        drift[coin] = (np.mean(r5), np.std(r5))
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r1 = c.pct_change()
            jump = r1 / r1.rolling(20, min_periods=10).std()
            raw = df.get("debug_info.components.fall_depth.last_history_value")
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for i in np.where(df["regime"].values == "mean_reversion")[0]:
                d = {"coin": coin, "w": w, "year": yr[i], "pos": i,
                     "fc": df["forecast"].iloc[i],
                     "ret90": raw.iloc[i] if raw is not None else np.nan,
                     "jump": jump.iloc[i], "r1": r1.iloc[i]}
                for h in [1, 2, 3, 5, 10, 20]:
                    d[f"f{h}"] = c.iloc[i + h] / c.iloc[i] - 1 if i + h < len(c) else np.nan
                rows.append(d)
    ev = pd.DataFrame(rows)
    for coin in drift:
        m = ev.coin == coin
        ev.loc[m, "u5"] = ev.loc[m, "f5"] - drift[coin][0]
        ev.loc[m, "s5"] = (ev.loc[m, "f5"] - drift[coin][0]) / drift[coin][1]
    out = {}
    def summ(g):
        s = g.dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    out["horizons"] = pd.DataFrame({f"f{h}": summ(ev[f"f{h}"]) for h in [1, 2, 3, 5, 10, 20]}).T
    out["u5_by_coin"] = ev.groupby("coin")["u5"].apply(summ).unstack()
    out["u5_by_year"] = ev.groupby("year")["u5"].apply(summ).unstack()
    ev["fc_q"] = pd.qcut(ev["fc"].rank(method="first"), 3, labels=["deep", "mid", "shallow"])
    out["u5_by_fc_tercile"] = ev.groupby("fc_q")["u5"].apply(summ).unstack()
    e2 = ev.dropna(subset=["ret90"])
    if len(e2) > 10:
        e2 = e2.copy()
        e2["r90_q"] = pd.qcut(e2["ret90"].rank(method="first"), 3, labels=["deep", "mid", "shallow"])
        out["u5_by_ret90_tercile"] = e2.groupby("r90_q")["u5"].apply(summ).unstack()
        out["ret90_range"] = e2.groupby("r90_q")["ret90"].agg(["min", "max", "mean"])
        sl = stats.linregress(e2["ret90"], e2["u5"].fillna(0))
        out["slope_u5_on_ret90"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(e2)})
    ev["j_q"] = pd.qcut(ev["jump"].rank(method="first"), 3, labels=["small", "mid", "big"])
    out["u5_by_jump_tercile"] = ev.groupby("j_q")["u5"].apply(summ).unstack()
    out["f1to10_by_fc_tercile"] = ev.groupby("fc_q")[["f1", "f3", "f5", "f10"]].mean()
    out["fc_nonzero_share"] = float((ev.fc < 0).mean())
    out["n_events"] = len(ev)
    return out
