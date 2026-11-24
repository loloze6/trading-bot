import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = 3
    rows = []
    for coin, wins in data["bars"].items():
        grid_all = []
        per = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            o, h, l, c = b["open"], b["high"], b["low"], b["close"]
            rng = (h - l)
            rr = rng / rng.rolling(20, min_periods=20).mean()
            clv = (c - l) / rng.replace(0, np.nan)
            body = (c - o) / rng.replace(0, np.nan)
            r1 = c / c.shift(1) - 1
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            vol20 = r1.rolling(20).std()
            fwd = c.shift(-H) / c - 1
            idx = np.arange(0, len(b), H)
            idx = idx[idx + H < len(b)]
            g = pd.DataFrame({"coin": coin, "win": w, "day": b["timestamp"].iloc[idx].astype(str).str[:10].values,
                              "wd": pd.to_datetime(b["timestamp"].iloc[idx]).dt.weekday.values,
                              "year": pd.to_datetime(b["timestamp"].iloc[idx]).dt.year.values,
                              "rr": rr.iloc[idx].values, "clv": clv.iloc[idx].values, "body": body.iloc[idx].values,
                              "r1": r1.iloc[idx].values, "r5": r5.iloc[idx].values, "r20": r20.iloc[idx].values,
                              "vol20": vol20.iloc[idx].values, "fwd": fwd.iloc[idx].values,
                              "pos": b["postRebalance_current_allocation"].iloc[idx].values})
            per.append(g)
        g = pd.concat(per)
        drift = g["fwd"].mean(); sd = g["fwd"].std()
        g["un"] = g["fwd"] - drift
        g["str"] = g["un"] / sd
        rows.append(g)
    G = pd.concat(rows, ignore_index=True)

    def summ(df, key):
        out = []
        for k, s in df.groupby(key, observed=True):
            d = s.groupby("day")["un"].sum()
            n = len(s); nd = len(d)
            m = s["un"].mean()
            t = d.sum() / nd / (d.std(ddof=1) / np.sqrt(nd)) * (1) if nd > 2 else np.nan
            # t of mean with day pooling: mean = sum/n ; se via day sums
            t = (d.sum() / n) / (np.sqrt(nd) * d.std(ddof=1) / n) if nd > 2 else np.nan
            out.append({"grp": str(k), "n": n, "days": nd, "mean_un": round(m, 5), "strength": round(s["str"].mean(), 4), "t": round(t, 2)})
        return pd.DataFrame(out)

    G2 = G.dropna(subset=["rr", "r20", "clv"])
    G2["rr_q"] = pd.qcut(G2["rr"], 5)
    wide = G2[G2["rr"] >= 1.5].copy()
    wide["r20_q"] = pd.qcut(wide["r20"], 5)
    wide["clv_q"] = pd.qcut(wide["clv"], 4)
    wide["absbody_q"] = pd.qcut(wide["body"].abs(), 3)
    wide["r1_sign"] = np.sign(wide["r1"])
    G2["r20_q"] = pd.qcut(G2["r20"], 5)
    G2["r1_q"] = pd.qcut(G2["r1"], 7)
    G2["vol_q"] = pd.qcut(G2["vol20"], 5)
    narrow = G2[G2["rr"] < 1.5].copy()
    narrow["r20_q"] = pd.qcut(narrow["r20"], 5)
    return {
        "all_by_rangeratio_q": summ(G2, "rr_q"),
        "wide_by_r20_q": summ(wide, "r20_q"),
        "narrow_by_r20_q": summ(narrow, "r20_q"),
        "wide_by_close_location_q": summ(wide, "clv_q"),
        "wide_by_r1_sign": summ(wide, "r1_sign"),
        "wide_by_absbody": summ(wide, "absbody_q"),
        "all_by_r1_q": summ(G2, "r1_q"),
        "all_by_vol_q": summ(G2, "vol_q"),
        "all_by_weekday": summ(G2, "wd"),
        "wide_by_year": summ(wide, "year"),
    }
