import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        allr = {h: [] for h in (1, 2, 3, 5)}
        for w, b in wins.items():
            c = b["close"].values
            for h in allr:
                idx = np.arange(0, len(c) - h, h)
                allr[h].extend(list(c[idx + h] / c[idx] - 1))
        drift[coin] = {h: (np.mean(v), np.std(v, ddof=1)) for h, v in allr.items()}
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            f = b["forecast"].fillna(0).values
            fprev = np.r_[0, f[:-1]]
            rng = (b["high"] - b["low"]).values
            cl = np.where(rng > 0, (b["close"] - b["low"]).values / np.where(rng > 0, rng, 1), np.nan)
            rm_col = "debug_info.components.range_mult.last_history_value"
            rm = b[rm_col].values if rm_col in b.columns else np.full(len(b), np.nan)
            ret1d = np.r_[np.nan, c[1:] / c[:-1] - 1]
            ret5 = pd.Series(c).pct_change(5).values
            ts = pd.to_datetime(b["timestamp"])
            for i in range(len(b)):
                if f[i] < 0 and (f[i] - fprev[i]) <= -2:
                    r = {"coin": coin, "win": w, "year": ts.iloc[i].year, "wd": ts.iloc[i].weekday(),
                         "day": ts.iloc[i].normalize(), "fc": f[i], "cl": cl[i], "rm": rm[i],
                         "ret0": ret1d[i], "ret5": ret5[i]}
                    for h in (1, 2, 3, 5):
                        if i + h < len(c):
                            r[f"u{h}"] = -((c[i + h] / c[i] - 1) - drift[coin][h][0])
                        else:
                            r[f"u{h}"] = np.nan
                    rows.append(r)
    df = pd.DataFrame(rows)
    out = {}
    def tday(d, col="u1"):
        d = d.dropna(subset=[col])
        if len(d) < 3:
            return pd.Series({"n": len(d), "mean": d[col].mean() if len(d) else np.nan, "t": np.nan, "days": d["day"].nunique()})
        s = d.groupby("day")[col].sum()
        t = d[col].mean() / (s.std(ddof=1) * np.sqrt(len(s)) / len(d))
        return pd.Series({"n": len(d), "mean": d[col].mean(), "t": t, "days": len(s)})
    out["overall_by_h"] = pd.DataFrame({h: tday(df, f"u{h}") for h in ("u1", "u2", "u3", "u5")}).T
    out["by_coin"] = df.groupby("coin").apply(tday)
    out["by_window"] = df.groupby("win").apply(tday)
    out["by_year"] = df.groupby("year").apply(tday)
    df["rmq"] = pd.qcut(df["rm"], 4, labels=False, duplicates="drop")
    out["by_rm_quartile"] = df.groupby("rmq").apply(tday)
    out["rm_q_means"] = df.groupby("rmq")["rm"].mean()
    df["clq"] = pd.cut(df["cl"], [0.5, 0.625, 0.75, 0.875, 1.0001])
    out["by_cl_bin"] = df.groupby("clq").apply(tday)
    df["r0sign"] = np.sign(df["ret0"])
    out["by_day_ret_sign"] = df.groupby("r0sign").apply(tday)
    df["r5sign"] = np.sign(df["ret5"])
    out["by_5d_ret_sign"] = df.groupby("r5sign").apply(tday)
    out["by_weekday"] = df.groupby("wd").apply(tday)
    out["corr_rm_u1"] = float(df[["rm", "u1"]].dropna().corr().iloc[0, 1])
    out["corr_cl_u1"] = float(df[["cl", "u1"]].dropna().corr().iloc[0, 1])
    out["skew_u1"] = float(df["u1"].skew())
    out["median_u1"] = float(df["u1"].median())
    out["share_pos_u1"] = float((df["u1"] > 0).mean())
    return out
