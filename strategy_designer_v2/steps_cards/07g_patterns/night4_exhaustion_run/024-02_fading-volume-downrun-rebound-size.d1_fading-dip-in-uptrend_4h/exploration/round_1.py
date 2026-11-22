def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    hourly = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(180, min_periods=60).std()
            # signed streak
            sgn = np.sign(r1.fillna(0)).values
            st = np.zeros(len(b)); sl = np.zeros(len(b)); vs = np.full(len(b), np.nan)
            lv = np.log(v.replace(0, np.nan)).values
            for i in range(1, len(b)):
                if sgn[i] != 0 and sgn[i] == np.sign(st[i-1]):
                    st[i] = st[i-1] + sgn[i]
                else:
                    st[i] = sgn[i]
            n = len(b)
            ret6 = c / c.shift(6) - 1
            ret180 = c / c.shift(180) - 1
            # streak return
            stlen = np.abs(st).astype(int)
            srt = np.array([c.iloc[i] / c.iloc[i - stlen[i]] - 1 if stlen[i] > 0 and i - stlen[i] >= 0 else 0 for i in range(n)])
            for i in range(n):
                k = stlen[i]
                if k >= 3 and i - k + 1 >= 0:
                    y = lv[i-k+1:i+1]
                    if np.all(np.isfinite(y)):
                        vs[i] = np.polyfit(np.arange(k), y, 1)[0]
            fwd = c.shift(-H) / c - 1
            nxt = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "st": st, "srt_sd": srt / sd, "vs": vs,
                               "r6_sd": ret6 / (sd * np.sqrt(6)), "r180": ret180, "sd": sd,
                               "fwd": fwd, "nxt": nxt, "fc": b["forecast"].astype(float),
                               "hour": ts.dt.hour, "wd": ts.dt.weekday,
                               "grid": (np.arange(n) % H == 0)})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.grid].groupby("coin")["fwd"].mean()
    A["ex"] = A["fwd"] - A["coin"].map(drift)
    usual = A[A.grid].groupby("coin")["fwd"].std()
    A["exs"] = A["ex"] / A["coin"].map(usual)
    G = A[A.grid].dropna(subset=["ex"])
    def summ(g):
        x = g["exs"].dropna()
        return pd.Series({"n": len(x), "mean_strength": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "mean_ex_pct": 100 * g["ex"].mean()})
    out = {}
    G = G.copy()
    G["stb"] = pd.cut(G["st"], [-100, -5, -3, -1, 0, 2, 4, 100], labels=["<=-5", "-4..-3", "-2..-1", "0", "1..2", "3..4", ">=5"])
    out["streak_len"] = G.groupby("stb").apply(summ)
    G["r6q"] = pd.qcut(G["r6_sd"], 10, labels=False)
    out["r6_decile"] = G.groupby("r6q").apply(summ)
    G["trend"] = np.where(G["r180"] > 0, "up30", "down30")
    out["r6_ext_by_trend"] = G[G.r6q.isin([0, 9])].groupby(["r6q", "trend"]).apply(summ)
    G["volq"] = G.groupby("coin")["sd"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["vol_tercile"] = G.groupby("volq").apply(summ)
    out["r180_quint"] = G.groupby(pd.qcut(G["r180"], 5, labels=False)).apply(summ)
    S = G[(G.st.abs() >= 3) & G.vs.notna()].copy()
    S["dir"] = np.where(S.st > 0, "up", "down"); S["fade"] = np.where(S.vs < 0, "fade", "rise")
    out["streak3_dir_fade"] = S.groupby(["dir", "fade"]).apply(summ)
    # hour/weekday next-bar
    def s1(g):
        x = g["nxt"].dropna(); return pd.Series({"n": len(x), "mean_bp": 1e4 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out["hour_nextbar"] = A.groupby("hour").apply(s1)
    out["weekday_nextbar"] = A.groupby("wd").apply(s1)
    # forecast
    F = G[G.fc > 0]
    out["fc_pos_tercile"] = F.groupby(pd.qcut(F.fc, 3, labels=False, duplicates="drop")).apply(summ)
    out["fc_zero"] = summ(G[G.fc == 0])
    return out
