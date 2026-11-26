def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 2, 3, 5]
    # coin drift per horizon, non-overlapping grid per window
    drift = {}
    usual = {}
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs, ddof=1)
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values; hi = df["high"].values; lo = df["low"].values
            ret = pd.Series(cl).pct_change()
            sd30 = ret.rolling(30).std().values
            n = len(df)
            sig = (df["regime"] == "mean_reversion") & (df["forecast"] > 2)
            seen = set()
            for i in np.where(sig.values)[0]:
                cell = i // 3
                if cell in seen: continue
                seen.add(cell)
                r = {"coin": c, "win": w, "day": str(df["timestamp"].iloc[i])[:10],
                     "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                     "fc": df["forecast"].iloc[i],
                     "loc": (hi[i] - cl[i]) / (hi[i] - lo[i]) if hi[i] > lo[i] else np.nan,
                     "width": ((hi[i] - lo[i]) / cl[i]) / sd30[i] if sd30[i] > 0 else np.nan,
                     "prevret": ret.iloc[i]}
                for h in H:
                    if i + h < n:
                        r[f"u{h}"] = cl[i + h] / cl[i] - 1 - drift[(c, h)]
                    else:
                        r[f"u{h}"] = np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    def tday(col, sub):
        s = sub.dropna(subset=[col])
        g = s.groupby("day")[col].sum()
        m = s[col].mean()
        se = g.std(ddof=1) * np.sqrt(len(g)) / len(s) if len(g) > 1 else np.nan
        return pd.Series({"n": len(s), "days": len(g), "mean": m, "t": m / se if se else np.nan})
    out = {}
    out["by_horizon"] = pd.DataFrame({f"u{h}": tday(f"u{h}", d) for h in H}).T
    out["by_coin_u3"] = d.groupby("coin").apply(lambda s: tday("u3", s))
    out["by_coin_u1"] = d.groupby("coin").apply(lambda s: tday("u1", s))
    out["by_year_u3"] = d.groupby("year").apply(lambda s: tday("u3", s))
    out["by_win_u3"] = d.groupby("win").apply(lambda s: tday("u3", s))
    d["wq"] = pd.qcut(d["width"], 3, labels=["w_lo", "w_mid", "w_hi"])
    d["lq"] = pd.qcut(d["loc"], 3, labels=["l_lo", "l_mid", "l_hi"])
    out["by_width_terc"] = pd.concat({h: d.groupby("wq").apply(lambda s: tday(h, s)) for h in ["u1", "u3", "u5"]})
    out["by_loc_terc"] = pd.concat({h: d.groupby("lq").apply(lambda s: tday(h, s)) for h in ["u1", "u3", "u5"]})
    out["width_quantiles"] = d["width"].describe()
    out["corr_spearman"] = pd.Series({f"{a}_{h}": stats.spearmanr(d[a], d[h], nan_policy="omit")[0]
                                      for a in ["width", "loc", "fc", "prevret"] for h in ["u1", "u3", "u5"]})
    d["up"] = d["prevret"] > 0
    out["by_prevret_sign"] = d.groupby("up").apply(lambda s: tday("u3", s))
    out["median_u3_shpos"] = pd.Series({"median": d["u3"].median(), "share_pos": (d["u3"] > 0).mean()})
    return out
