def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    allrows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float)
            b["fwd3"] = c.shift(-3) / c - 1
            b["ret1"] = c.pct_change()
            b["r20"] = c / c.shift(20) - 1
            b["r7"] = c / c.shift(7) - 1
            b["sma50"] = c / c.rolling(50, min_periods=30).mean() - 1
            b["vol20"] = b["ret1"].rolling(20, min_periods=10).std()
            b["vol60"] = b["ret1"].rolling(60, min_periods=20).std()
            b["vratio"] = b["vol20"] / b["vol60"]
            b["volu"] = b["volume"] / b["volume"].rolling(30, min_periods=10).mean()
            b["sun"] = ts.dt.dayofweek == 6
            b["coin"] = coin; b["win"] = w; b["year"] = ts.dt.year
            b["fc"] = b["forecast"].astype(float)
            # grid drift
            g = c.iloc[::3]
            b["grid3"] = np.nan
            allrows.append(b)
    A = pd.concat(allrows, ignore_index=True)
    # coin drift over 3 bars from non-overlapping grid
    drift = {}
    for coin, wins in data["bars"].items():
        rs = []
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            idx = np.arange(0, len(c) - 3, 3)
            rs.extend((c.values[idx + 3] / c.values[idx] - 1).tolist())
        drift[coin] = np.mean(rs)
    A["ex3"] = A["fwd3"] - A["coin"].map(drift)
    S = A[A["sun"]].dropna(subset=["fwd3"])
    cases = S[S["fc"] >= 2]
    nos = S[S["fc"] <= 0]
    def summ(df, col="ex3"):
        x = df[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan, "neg_share": (x < -0.1).mean()})
    out["cases_all"] = summ(cases)
    # by trend states
    tab = {}
    for name, col in [("r20", "r20"), ("sma50", "sma50"), ("vratio", "vratio"), ("volu", "volu"), ("r7", "r7"), ("vol20", "vol20")]:
        q = pd.qcut(S[col], 4, labels=False, duplicates="drop")
        for k in range(4):
            sub_c = cases[q.loc[cases.index] == k]
            sub_n = nos[q.loc[nos.index] == k]
            tab[(name, k)] = {"case_n": len(sub_c), "case_ex3": sub_c["ex3"].mean(), "case_t": summ(sub_c)["t"],
                              "nosig_n": len(sub_n), "nosig_ex3": sub_n["ex3"].mean()}
    out["by_state_quartile"] = pd.DataFrame(tab).T
    # by year
    out["cases_by_year"] = cases.groupby("year")["ex3"].agg(["count", "mean"])
    # by forecast bucket
    out["cases_by_fc"] = cases.groupby(pd.cut(cases["fc"], [2, 4, 6, 8, 12, 21]))["ex3"].agg(["count", "mean", "std"])
    # book daily
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            D.append(d)
    D = pd.concat(D, ignore_index=True)
    bk = D.groupby(["win", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index()
    bk["wn"] = bk["win"].str[1:].astype(int)
    bk = bk.sort_values(["wn", "day"]).dropna(subset=["br"])
    v = (1 + bk["br"]).cumprod().values
    peak = np.maximum.accumulate(v); dd = v / peak - 1
    bk["dd"] = dd
    i = dd.argmin(); pk = np.argmax(v[: i + 1] == peak[i])
    seg = bk.iloc[pk:i + 1]
    out["deepest_fall"] = pd.Series({"depth": dd[i], "days": i - pk, "windows": ",".join(seg["win"].unique()),
                                     "coins_mean_ret_chain": (1 + seg["cr"]).prod() - 1, "book_chain": (1 + seg["br"]).prod() - 1})
    # per window book stats
    out["book_by_window"] = bk.groupby("wn").agg(n=("br", "size"), book=("br", lambda x: (1 + x).prod() - 1),
                                                  hold=("cr", lambda x: (1 + x).prod() - 1),
                                                  mdd=("br", lambda x: ((1 + x).cumprod() / (1 + x).cumprod().cummax() - 1).min()))
    # cases inside deepest fall windows vs elsewhere
    fw = set(seg["win"].unique())
    out["cases_in_fall_windows"] = summ(cases[cases["win"].isin(fw)])
    out["cases_other"] = summ(cases[~cases["win"].isin(fw)])
    # prior state of cases in fall windows
    out["state_fall_vs_other"] = pd.DataFrame({"fall": cases[cases["win"].isin(fw)][["r20", "sma50", "vratio", "vol20", "volu"]].mean(),
                                               "other": cases[~cases["win"].isin(fw)][["r20", "sma50", "vratio", "vol20", "volu"]].mean()})
    return out
