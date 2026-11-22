import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = [6, 18, 42]
    rows = []
    col = "debug_info.components.streak_vol_rise.last_history_value"
    for coin, wins in bars.items():
        drift = {}; usual = {}
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            drift[h] = np.mean(rs); usual[h] = np.std(rs)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; f = df["forecast"].fillna(0).values
            raw = df[col].values if col in df.columns else np.full(len(df), np.nan)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(df)
            ref = 0.0; used = set()
            for i in range(n):
                if f[i] <= 0:
                    ref = 0.0; continue
                ref = min(ref, f[i])
                if f[i] - ref >= 2:
                    ref = f[i]; cell = i // 42
                    if cell in used: continue
                    used.add(cell)
                    r = {"coin": coin, "year": yr[i], "f": f[i], "raw": raw[i]}
                    for h in H:
                        if i + h < n:
                            r[f"u{h}"] = c[i+h]/c[i]-1-drift[h]
                    rows.append(r)
    d = pd.DataFrame(rows)
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["raw_describe"] = d["raw"].describe()
    d["rawabs"] = d["raw"].abs()
    d["rq"] = pd.qcut(d["rawabs"].rank(method="first"), 4, labels=False)
    for h in H:
        out[f"by_raw_q_{h}"] = d.groupby("rq").apply(lambda g: pd.concat([tt(g[f"u{h}"]), pd.Series({"raw": g["raw"].mean()})]))
        med = d["rawabs"].median()
        out[f"raw_median_split_{h}"] = d.loc[d.rawabs > med, f"u{h}"].mean() - d.loc[d.rawabs <= med, f"u{h}"].mean()
    out["by_year_18"] = d.groupby("year")["u18"].apply(tt).unstack()
    out["by_coin_18"] = d.groupby("coin")["u18"].apply(tt).unstack()
    out["share_f_at_cap"] = (d.f >= 20).mean()
    return out
