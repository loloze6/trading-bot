import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    allret = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            r = df["close"].pct_change()
            rs.append(r.dropna())
        allret[coin] = pd.concat(rs)
    for coin, wins in bars.items():
        mu1 = allret[coin].mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; h = df["high"]; l = df["low"]
            r = c.pct_change()
            sd30 = r.rolling(30).std()
            width = (h - l) / c / sd30
            loc = (c - l) / (h - l)
            ts = pd.to_datetime(df["timestamp"])
            for i in np.where(df["forecast"] < 0)[0]:
                rec = {"coin": coin, "win": w, "year": ts.iloc[i].year,
                       "width": width.iloc[i], "loc": loc.iloc[i],
                       "dayret": c.iloc[i]/c.iloc[i-1]-1 if i > 0 else np.nan,
                       "day": ts.iloc[i].normalize()}
                for hh in [1, 2, 3, 5]:
                    if i + hh < len(df):
                        rec[f"ex{hh}"] = -(c.iloc[i+hh]/c.iloc[i]-1) + hh*mu1
                        rec[f"tot{hh}"] = -(c.iloc[i+hh]/c.iloc[i]-1)
                    else:
                        rec[f"ex{hh}"] = np.nan; rec[f"tot{hh}"] = np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g, col="ex1"):
        x = g[col].dropna()
        dd = g.dropna(subset=[col]).groupby("day")[col].sum()
        n = len(x)
        t = dd.mean()/ (dd.std()/np.sqrt(len(dd))) * 1 if len(dd) > 2 else np.nan
        return pd.Series({"n": n, "days": len(dd), "mean": x.mean(), "median": x.median(), "hit": (x > 0).mean(), "t_day": t})
    out = {}
    out["overall_by_horizon"] = pd.DataFrame({hh: summ(d, f"ex{hh}") for hh in [1,2,3,5]}).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    out["by_win"] = d.groupby("win").apply(summ)
    d["wq"] = pd.qcut(d["width"], 3, labels=["w_lo","w_mid","w_hi"])
    d["lq"] = pd.qcut(d["loc"], 3, labels=["l_lo","l_mid","l_hi"])
    out["by_width_tercile"] = d.groupby("wq").apply(summ)
    out["by_loc_tercile"] = d.groupby("lq").apply(summ)
    d["dq"] = pd.qcut(d["dayret"], 3, labels=["d_lo","d_mid","d_hi"])
    out["by_dayret_tercile"] = d.groupby("dq").apply(summ)
    out["width_tercile_h3"] = d.groupby("wq").apply(lambda g: summ(g, "ex3"))
    out["corr_spearman"] = pd.Series({
        "width_ex1": stats.spearmanr(d["width"], d["ex1"], nan_policy="omit")[0],
        "loc_ex1": stats.spearmanr(d["loc"], d["ex1"], nan_policy="omit")[0],
        "dayret_ex1": stats.spearmanr(d["dayret"], d["ex1"], nan_policy="omit")[0]})
    out["width_desc"] = d["width"].describe()
    return out
