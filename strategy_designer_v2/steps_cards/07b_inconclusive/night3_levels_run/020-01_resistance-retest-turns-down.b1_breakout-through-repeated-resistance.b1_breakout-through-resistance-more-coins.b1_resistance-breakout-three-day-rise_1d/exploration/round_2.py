import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    fc = "debug_info.components.res_break.post_pipeline_value"
    raw = "debug_info.components.res_break.last_history_value"
    rows = []
    drift = {}
    for coin, ws in bars.items():
        for h in (1, 3, 5, 10):
            rs = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = (np.mean(rs), np.std(rs))
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            pv = df[fc].values if fc in df else np.full(len(df), np.nan)
            rv = df[raw].values if raw in df else np.full(len(df), np.nan)
            n = len(df)
            r30 = pd.Series(c).pct_change(30).values
            r90 = pd.Series(c).pct_change(min(89, max(n - 1, 1))).values if n > 90 else np.full(n, np.nan)
            hi90 = pd.Series(c).rolling(90, min_periods=20).max().values
            prev = np.r_[0, f[:-1]]
            sig = (f - prev >= 2) & (f > 0)
            seen = set()
            for t in np.where(sig)[0]:
                cell = t // 3
                if cell in seen: continue
                seen.add(cell)
                d = {"coin": coin, "wnum": int(w[1:]), "f": f[t], "pv": pv[t], "raw": rv[t],
                     "r30": r30[t], "nearhi": c[t] / hi90[t] - 1 if not np.isnan(hi90[t]) else np.nan,
                     "year": pd.Timestamp(df["timestamp"].iloc[t]).year,
                     "usual3": drift[(coin, 3)][1]}
                for h in (1, 3, 5, 10):
                    d[f"x{h}"] = (c[t + h] / c[t] - 1 - drift[(coin, h)][0]) if t + h < n else np.nan
                d["x0"] = c[t] / c[t-1] - 1 if t > 0 else np.nan
                rows.append(d)
    D = pd.DataFrame(rows)
    def summ(g, col="x3"):
        x = g[col].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "median": x.median(),
                          "pos_share": (x > 0).mean(),
                          "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    out["horizons"] = pd.DataFrame({h: summ(D, h) for h in ("x0", "x1", "x3", "x5", "x10")}).T
    # trimmed (winsorised 1%) x3
    x = D["x3"].dropna()
    lo, hi = x.quantile([0.01, 0.99])
    xw = x.clip(lo, hi)
    out["x3_winsor_mean_t"] = pd.Series({"mean": xw.mean(), "t": xw.mean() / (xw.std() / np.sqrt(len(xw)))})
    D["strength3"] = D["x3"] / D["usual3"]
    out["by_coin"] = D.groupby("coin").apply(lambda g: pd.concat([summ(g), pd.Series({"x10": g.x10.mean(), "str3": g.strength3.mean()})]))
    D["fold"] = pd.cut(D["wnum"], [0, 6, 12, 18, 24], labels=["w1-6", "w7-12", "w13-18", "w19-24"])
    out["by_wingroup"] = D.groupby("fold").apply(lambda g: pd.concat([summ(g), pd.Series({"x10": g.x10.mean()})]))
    out["by_year"] = D.groupby("year").apply(lambda g: pd.concat([summ(g), pd.Series({"x10": g.x10.mean()})]))
    D["fq"] = pd.qcut(D["pv"].rank(method="first"), 4, labels=False)
    out["by_forecast_q"] = D.groupby("fq").apply(lambda g: pd.concat([summ(g), pd.Series({"pv_mean": g.pv.mean(), "x5": g.x5.mean(), "x10": g.x10.mean()})]))
    D["rq"] = pd.qcut(D["raw"].rank(method="first"), 4, labels=False)
    out["by_raw_q"] = D.groupby("rq").apply(lambda g: pd.concat([summ(g), pd.Series({"raw_mean": g.raw.mean(), "x5": g.x5.mean(), "x10": g.x10.mean()})]))
    D["r30q"] = pd.qcut(D["r30"].rank(method="first"), 4, labels=False)
    out["by_r30_q"] = D.groupby("r30q").apply(lambda g: pd.concat([summ(g), pd.Series({"r30": g.r30.mean(), "x5": g.x5.mean(), "x10": g.x10.mean()})]))
    D["nhq"] = pd.qcut(D["nearhi"].rank(method="first"), 4, labels=False)
    out["by_nearhigh_q"] = D.groupby("nhq").apply(lambda g: pd.concat([summ(g), pd.Series({"nearhi": g.nearhi.mean(), "x5": g.x5.mean(), "x10": g.x10.mean()})]))
    D["x0q"] = pd.qcut(D["x0"].rank(method="first"), 4, labels=False)
    out["by_signal_bar_move_q"] = D.groupby("x0q").apply(lambda g: pd.concat([summ(g), pd.Series({"x0": g.x0.mean(), "x10": g.x10.mean()})]))
    core = D[D.coin.isin(["BTCUSD", "ETHUSD", "LTCUSD", "XMRUSD", "XRPUSD", "ZECUSD"])]
    out["default6_vs_rest"] = pd.DataFrame({"default6": summ(core), "other13": summ(D[~D.index.isin(core.index)])}).T
    sl = D[["pv", "x3"]].dropna()
    r = stats.spearmanr(sl.pv, sl.x3)
    out["spearman_pv_x3"] = pd.Series({"rho": r.correlation, "p": r.pvalue, "n": len(sl)})
    out["usual_move_3d_median"] = float(np.median([v[1] for k, v in drift.items() if k[1] == 3]))
    return out
