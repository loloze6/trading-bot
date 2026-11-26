import pandas as pd, numpy as np

def explore(data):
    bars = data["bars"]
    H = [1, 2, 3, 5]
    rows = []
    drift = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.extend(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs)
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values; hi = df["high"].values; lo = df["low"].values
            rng = hi - lo
            loc = np.where(rng > 0, (cl - lo) / np.where(rng > 0, rng, 1), np.nan)
            ts = pd.to_datetime(df["timestamp"])
            ret1 = np.r_[np.nan, cl[1:] / cl[:-1] - 1]
            cl_s = pd.Series(cl)
            tr = (cl_s / cl_s.shift(60) - 1).values  # 60d trend inside window
            vol30 = pd.Series(ret1).rolling(30).std().values
            reg = df["regime"].values
            for i in range(len(cl)):
                if np.isnan(loc[i]) or loc[i] < 0.8:
                    continue
                r = {"coin": c, "w": w, "year": ts[i].year, "loc": loc[i], "regime": reg[i],
                     "fc": df["forecast"].iloc[i], "tr60": tr[i], "pos": i, "day": ts[i].normalize(),
                     "ret_today": ret1[i]}
                for h in H:
                    if i + h < len(cl):
                        r[f"u{h}"] = -((cl[i + h] / cl[i] - 1) - drift[(c, h)])
                        r[f"cell{h}"] = i // h
                rows.append(r)
    d = pd.DataFrame(rows)
    d["grp"] = np.where(d["regime"] == "mean_reversion", "inprofile", np.where(d["regime"] == "chop", "outprofile", d["regime"]))

    def tstat(sub, h):
        col = f"u{h}"
        s = sub.dropna(subset=[col]).drop_duplicates(subset=["coin", "w", f"cell{h}"])
        g = s.groupby("day")[col].sum()
        n = len(s)
        if n < 3: return pd.Series({"n": n, "mean": np.nan, "t": np.nan})
        m = s[col].mean()
        se = np.sqrt(((s.groupby("day")[col].apply(lambda x: (x - m).sum())) ** 2).sum()) / n
        return pd.Series({"n": n, "days": g.size, "mean": m, "t": m / se if se > 0 else np.nan})

    out = {}
    out["by_group_h"] = pd.DataFrame({f"{g}_h{h}": tstat(d[d.grp == g], h) for g in d.grp.unique() for h in H}).T
    ip = d[d.grp == "inprofile"]
    out["inprof_by_coin_h2"] = pd.DataFrame({c: tstat(ip[ip.coin == c], 2) for c in ip.coin.unique()}).T
    out["inprof_by_year_h2"] = pd.DataFrame({y: tstat(ip[ip.year == y], 2) for y in sorted(ip.year.unique())}).T
    ip = ip.copy()
    ip["locb"] = pd.cut(ip["loc"], [0.8, 0.9, 0.95, 1.01], right=False).astype(str)
    out["inprof_by_loc_h2"] = pd.DataFrame({b: tstat(ip[ip.locb == b], 2) for b in ip.locb.unique()}).T
    ip["upday"] = np.where(ip["ret_today"] > 0, "up", "down")
    out["inprof_by_todayret_h2"] = pd.DataFrame({b: tstat(ip[ip.upday == b], 2) for b in ip.upday.unique()}).T
    q = ip["ret_today"].quantile([0.5]).iloc[0]
    ip["bigup"] = np.where(ip["ret_today"] > q, "above_median_ret", "below_median_ret")
    out["inprof_by_todaysize_h2"] = pd.DataFrame({b: tstat(ip[ip.bigup == b], 2) for b in ip.bigup.unique()}).T
    ip["trs"] = np.where(ip["tr60"] > 0, "tr_pos", np.where(ip["tr60"] <= 0, "tr_neg", "na"))
    out["inprof_by_trend_sign_h2"] = pd.DataFrame({b: tstat(ip[ip.trs == b], 2) for b in ip.trs.unique()}).T
    out["inprof_by_window_h2"] = pd.DataFrame({w: tstat(ip[ip.w == w], 2) for w in sorted(ip.w.unique())}).T
    return out
