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
            hi90 = pd.Series(c).rolling(90, min_periods=20).max().values
            prev = np.r_[0, f[:-1]]
            sig = (f - prev >= 2) & (f > 0)
            seen = set()
            for t in np.where(sig)[0]:
                cell = t // 3
                if cell in seen: continue
                seen.add(cell)
                d = {"coin": coin, "win": w, "wnum": int(w[1:]), "f": f[t], "pv": pv[t], "raw": rv[t],
                     "r30": r30[t], "nearhi": c[t] / hi90[t] - 1 if not np.isnan(hi90[t]) else np.nan,
                     "year": pd.Timestamp(df["timestamp"].iloc[t]).year}
                for h in (1, 3, 5, 10):
                    d[f"x{h}"] = (c[t + h] / c[t] - 1 - drift[(coin, h)][0]) if t + h < n else np.nan
                d["x0"] = c[t] / c[t-1] - 1 if t > 0 else np.nan
                rows.append(d)
    D = pd.DataFrame(rows)
    def summ(g, col="x3"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["horizons"] = pd.DataFrame({h: summ(D, f"x{h}") for h in ("x0", "x1", "x3", "x5", "x10")}).T
    out["by_coin"] = D.groupby("coin").apply(summ)
    D["fold"] = pd.cut(D["wnum"], [0, 6, 12, 18, 24], labels=["w1-6", "w7-12", "w13-18", "w19-24"])
    out["by_wingroup"] = D.groupby("fold").apply(summ)
    out["by_year"] = D.groupby("year").apply(summ)
    D["fq"] = pd.qcut(D["pv"].rank(method="first"), 4, labels=False)
    out["by_forecast_q"] = D.groupby("fq").apply(lambda g: pd.concat([summ(g), pd.Series({"pv_mean": g.pv.mean(), "x10": g.x10.mean(), "x5": g.x5.mean()})]))
    D["rq"] = pd.qcut(D["raw"].rank(method="first"), 4, labels=False)
    out["by_raw_q"] = D.groupby("rq").apply(lambda g: pd.concat([summ(g), pd.Series({"raw_mean": g.raw.mean(), "x10": g.x10.mean()})]))
    D["r30q"] = pd.qcut(D["r30"].rank(method="first"), 4, labels=False)
    out["by_r30_q"] = D.groupby("r30q").apply(lambda g: pd.concat([summ(g), pd.Series({"r30": g.r30.mean(), "x10": g.x10.mean()})]))
    D["nhq"] = pd.qcut(D["nearhi"].rank(method="first"), 4, labels=False)
    out["by_nearhigh_q"] = D.groupby("nhq").apply(lambda g: pd.concat([summ(g), pd.Series({"nearhi": g.nearhi.mean(), "x10": g.x10.mean()})]))
    out["usual_move_3d_median"] = float(np.median([v[1] for k, v in drift.items() if k[1] == 3]))
    return out
