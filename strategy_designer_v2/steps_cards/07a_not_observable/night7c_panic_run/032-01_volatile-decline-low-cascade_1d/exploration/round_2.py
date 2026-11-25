def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]
    case_rows, sit_rows, jump_rows = [], [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            ts = pd.to_datetime(df["timestamp"])
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0)
            close = df["close"].astype(float)
            reg = df["regime"].astype(str)
            dfc = fc.diff()
            for i in range(n):
                if reg.iloc[i] == "trending":
                    sit_rows.append({"coin": coin, "window": w, "day": ts.iloc[i].normalize(),
                                     "pos": i, "fc": fc.iloc[i], "dfc": dfc.iloc[i],
                                     "prev_trending": (i > 0 and reg.iloc[i-1] == "trending")})
            for start in range(0, n, 5):
                sig = [i for i in range(start, min(start+5, n)) if dfc.iloc[i] <= -2]
                if sig:
                    i = sig[0]
                    r = close.iloc[i+5]/close.iloc[i]-1 if i+5 < n else np.nan
                    case_rows.append({"coin": coin, "window": w, "day": ts.iloc[i].normalize(),
                                      "pos": i, "ret5": r, "fc": fc.iloc[i]})
    s = pd.DataFrame(sit_rows); c = pd.DataFrame(case_rows)
    out = {}
    out["situation bars"] = len(s)
    out["situation distinct days"] = s["day"].nunique()
    out["situation bars by coins same day"] = s.groupby("day").size().value_counts().sort_index()
    out["situation bars: first of run vs continuing"] = s["prev_trending"].value_counts()
    s["is_case_jump"] = s["dfc"] <= -2
    out["situation bars with fc drop>=2"] = int(s["is_case_jump"].sum())
    out["situation |fc| quantiles"] = s["fc"].abs().quantile([.1,.25,.5,.75,.9])
    out["situation runs length"] = s.groupby(["coin","window"]).size().describe()
    out["situation pos in window"] = s["pos"].describe()
    out["cases incl. end-of-window"] = len(c)
    out["cases with no 5-bar outcome"] = int(c["ret5"].isna().sum())
    out["case distinct days"] = c["day"].nunique()
    out["cases per day count"] = c.groupby("day").size().value_counts().sort_index()
    cc = c.dropna(subset=["ret5"])
    d = (-cc["ret5"]).groupby(cc["day"]).sum()
    out["per-day summed short ret: mean,std,n,t"] = pd.Series({"mean": d.mean(), "std": d.std(), "n": len(d),
                                                              "t": d.mean()/(d.std()/np.sqrt(len(d)))})
    return out
