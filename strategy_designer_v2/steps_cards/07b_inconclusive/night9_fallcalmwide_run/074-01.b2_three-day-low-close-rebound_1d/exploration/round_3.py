def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    h = 3
    drift = {}
    for c, ws in bars.items():
        rs = []
        for w, df in ws.items():
            cl = df["close"].values
            idx = np.arange(0, len(cl) - h, h)
            rs += list(cl[idx + h] / cl[idx] - 1)
        drift[c] = np.mean(rs)
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values; hi = df["high"].values; lo = df["low"].values
            n = len(df)
            fc = df["forecast"].fillna(0).values
            prev = np.r_[0, fc[:-1]]
            sig = (fc - prev >= 2) & (fc > 0)
            reg = df["regime"].astype(str).values
            ret = pd.Series(cl).pct_change()
            sd30 = ret.rolling(30).std().values
            for cell in range(0, n // 3):
                i0 = cell * 3
                ii = [i for i in range(i0, min(i0 + 3, n))]
                cases = [i for i in ii if sig[i]]
                if cases:
                    i = cases[0]; kind = "case"
                else:
                    i = i0
                    if reg[i] == "chop":
                        kind = "outside"
                    else:
                        kind = "rc_other"
                if i + h >= n: continue
                loc = (hi[i] - cl[i]) / (hi[i] - lo[i]) if hi[i] > lo[i] else np.nan
                rows.append({"coin": c, "day": str(df["timestamp"].iloc[i])[:10],
                             "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                             "kind": kind, "loc": loc,
                             "dayret": ret.iloc[i],
                             "u3": cl[i + h] / cl[i] - 1 - drift[c]})
    d = pd.DataFrame(rows)
    def tday(sub):
        s = sub.dropna(subset=["u3"])
        g = s.groupby("day")["u3"].sum()
        m = s["u3"].mean()
        se = g.std(ddof=1) * np.sqrt(len(g)) / len(s) if len(g) > 1 else np.nan
        return pd.Series({"n": len(s), "days": len(g), "mean": m, "t": m / se if se else np.nan})
    out = {}
    out["by_kind"] = d.groupby("kind").apply(tday)
    out["by_kind_year"] = d.groupby(["kind", "year"]).apply(tday)
    rc = d[d["kind"] == "rc_other"]
    cs = d[d["kind"] == "case"]
    out["case_minus_rc_welch"] = pd.Series({"diff": cs["u3"].mean() - rc["u3"].mean(),
                                            "t": stats.ttest_ind(cs["u3"].dropna(), rc["u3"].dropna(), equal_var=False)[0]})
    # rising-calm other days that are down days closing low (not wide): baseline of low closes
    rc2 = rc.copy()
    rc2["lowclose"] = rc2["loc"] >= 0.75
    out["rc_other_by_lowclose"] = rc2.groupby("lowclose").apply(tday)
    out["case_share_by_year"] = d[d.kind != "outside"].groupby("year")["kind"].apply(lambda s: (s == "case").mean())
    return out
