import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            sd24 = r1.rolling(24).std()
            volm = sd24.rolling(720, min_periods=120).mean()
            s = r1 / volm
            vr = sd24 / volm
            year = pd.to_datetime(df["timestamp"]).dt.year
            fc = df["forecast"].astype(float)
            n = len(df); h = 24
            idx = np.arange(0, n - h, h)
            fwd = c.values[idx + h] / c.values[idx] - 1
            rows.append(pd.DataFrame({"coin": coin, "win": w, "fwd": fwd, "s": s.values[idx],
                                      "vr": vr.values[idx], "r1": r1.values[idx],
                                      "year": year.values[idx], "fc": fc.values[idx]}))
    A = pd.concat(rows, ignore_index=True)
    A["drift"] = A.groupby("coin")["fwd"].transform("mean")
    A["ex"] = A["fwd"] - A["drift"]
    A = A.dropna(subset=["s", "vr", "ex"])
    def summ(g):
        m = g["ex"].mean(); sd = g["ex"].std(); n = len(g)
        return pd.Series({"n": n, "mean_ex_%": 100*m, "mean_tot_%": 100*g["fwd"].mean(),
                          "t": m/(sd/np.sqrt(n)) if n > 2 and sd > 0 else np.nan})
    out = {}
    fall = A[A["r1"] < 0].copy()
    fall["sq"] = pd.qcut(fall["s"], 5, labels=["s1_big","s2","s3","s4","s5_small"])
    fall["vq"] = pd.qcut(fall["vr"], 3, labels=["v_low","v_mid","v_high"])
    g = fall.groupby(["sq","vq"], observed=True).apply(summ)
    out["fall_s_x_vr_mean"] = g["mean_ex_%"].unstack("vq")
    out["fall_s_x_vr_t"] = g["t"].unstack("vq")
    # all bars (no fall filter) by vr tercile: is high vr itself the driver?
    A["vq"] = pd.qcut(A["vr"], 3, labels=["v_low","v_mid","v_high"])
    A["side"] = np.where(A["r1"] < 0, "fall", "rise")
    out["all_by_vr_side"] = A.groupby(["vq","side"], observed=True).apply(summ)
    # strongest cell: big falls in high vr, by year and coin, and without 2021
    e = fall[(fall["sq"] == "s1_big") & (fall["vq"] == "v_high")]
    out["bighigh_by_year"] = e.groupby("year").apply(summ)
    out["bighigh_by_coin"] = e.groupby("coin").apply(summ)
    out["bighigh_ex2021"] = summ(e[e["year"] != 2021]).to_frame().T
    # within high vr: graded in fall size? deciles of s
    hv = fall[fall["vq"] == "v_high"].copy()
    hv["sd"] = pd.qcut(hv["s"], 5, labels=["d1_big","d2","d3","d4","d5_small"])
    out["highvr_by_fall"] = hv.groupby("sd", observed=True).apply(summ)
    # forecast on grid bars: share of falls with forecast >0, and mean ex by forecast>0
    fall["fpos"] = np.where(fall["fc"] > 0, "fc_pos", "fc_zero")
    out["fall_by_fc"] = fall.groupby("fpos").apply(summ)
    return out
