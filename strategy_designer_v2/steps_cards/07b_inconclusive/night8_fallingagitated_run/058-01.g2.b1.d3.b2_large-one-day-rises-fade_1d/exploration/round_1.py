import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = [1, 2, 3, 5, 10]
    drift = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs) if rs else np.nan
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            r = pd.Series(cl).pct_change()
            sd = r.rolling(30, min_periods=20).std()
            sr = (r / sd).values
            r3 = pd.Series(cl).pct_change(3).values
            ts = pd.to_datetime(df["timestamp"])
            mr = (df["regime"] == "mean_reversion").values
            for i in np.where(mr)[0]:
                rec = {"coin": c, "win": w, "year": ts.dt.year.values[i], "i": i,
                       "day": ts.dt.floor("D").values[i], "sr": sr[i], "r1": r.values[i],
                       "prior2": (r3[i] + 1) / (r.values[i] + 1) - 1 if not np.isnan(r3[i]) else np.nan}
                for h in H:
                    if i + h < len(cl):
                        tot = cl[i + h] / cl[i] - 1
                        rec[f"u{h}"] = -(tot - drift[(c, h)])
                        rec[f"t{h}"] = -tot
                    else:
                        rec[f"u{h}"] = np.nan
                        rec[f"t{h}"] = np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)

    def tday(x, col):
        x = x.dropna(subset=[col])
        n = len(x)
        if n < 3:
            return np.nan
        m = x[col].mean()
        dev = (x[col] - m).groupby(x["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / n
        return m / se if se > 0 else np.nan

    out = {}
    hz = []
    for h in H:
        xx = d.assign(cell=d["i"] // h).drop_duplicates(["coin", "win", "cell"])
        hz.append({"h": h, "n": int(xx[f"u{h}"].notna().sum()),
                   "days": int(xx.dropna(subset=[f"u{h}"])["day"].nunique()),
                   "mean_unusual": xx[f"u{h}"].mean(), "t_day": tday(xx, f"u{h}"),
                   "mean_total": xx[f"t{h}"].mean()})
    out["by_horizon"] = pd.DataFrame(hz)

    c5 = d.assign(cell=d["i"] // 5).drop_duplicates(["coin", "win", "cell"]).copy()

    def grp(key):
        g = []
        for k, x in c5.groupby(key):
            g.append({"key": k, "n": int(x["u5"].notna().sum()), "mean_u5": x["u5"].mean(),
                      "t": tday(x, "u5"), "mean_u1": x["u1"].mean(), "mean_u3": x["u3"].mean(),
                      "mean_u10": x["u10"].mean()})
        return pd.DataFrame(g)

    out["by_coin"] = grp("coin")
    out["by_year"] = grp("year")
    out["by_window"] = grp("win")
    c5["srq"] = pd.qcut(c5["sr"], 4, labels=False, duplicates="drop")
    out["by_sr_quartile"] = grp("srq")
    out["sr_quartile_edges"] = c5.groupby("srq")["sr"].agg(["min", "max", "count"])
    c5["prior2_up"] = (c5["prior2"] > 0).astype(int)
    out["by_prior2days_up"] = grp("prior2_up")
    out["spearman_sr_u5"] = float(c5[["sr", "u5"]].dropna().corr(method="spearman").iloc[0, 1])
    out["n_cases_5grid"] = int(len(c5))
    return out
