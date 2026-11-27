import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - 10, 10):
                rs.append(c[i + 10] / c[i] - 1)
        m10 = np.mean(rs)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.Series(df["close"].values)
            r = c.pct_change()
            ret60 = c.pct_change(60).values
            ret30 = c.pct_change(30).values
            vr = (r.rolling(10).std() / r.rolling(30).std()).values
            f = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            cv = c.values
            for i in range(0, len(cv) - 10, 10):
                if np.isnan(ret60[i]) or abs(ret60[i]) > 0.10 or np.isnan(vr[i]):
                    continue
                fwd = cv[i + 10] / cv[i] - 1 - m10
                rows.append({"coin": coin, "day": ts[i].normalize(), "ret30": ret30[i],
                             "ret60": ret60[i], "vr": vr[i], "fwd_ex": fwd, "f": f[i]})
    X = pd.DataFrame(rows)
    X["side"] = np.where(X["ret30"] < 0, "fall", "rise")
    X["quick"] = np.where(X["vr"] > 1, "vr>1", "vr<=1")
    X["cont"] = np.where(X["side"] == "fall", -X["fwd_ex"], X["fwd_ex"])
    def st(g):
        d = g.groupby("day")["cont"].sum()
        return pd.Series({"mean_cont": g["cont"].mean(), "n": len(g), "days": len(d),
                          "t_day": d.mean() / (d.std(ddof=1) / np.sqrt(len(d))) if len(d) > 2 else np.nan})
    out = {}
    out["side_x_vr"] = X.groupby(["side", "quick"]).apply(st)
    out["side_all"] = X.groupby("side").apply(st)
    X["q30"] = pd.qcut(X["ret30"], 5, labels=False)
    out["ret30_quintile_fwdex"] = X.groupby("q30").agg(ret30=("ret30", "mean"), fwd_ex=("fwd_ex", "mean"), n=("fwd_ex", "size"))
    F = X[X["side"] == "fall"].copy()
    F["q"] = pd.qcut(F["ret30"], 3, labels=["deep", "mid", "shallow"])
    out["fall_depth_x_vr"] = F.groupby(["q", "quick"]).apply(st)
    F["t60"] = np.where(F["ret60"] < 0, "60d<0", "60d>=0")
    out["fall_by_60d_sign"] = F.groupby(["t60", "quick"]).apply(st)
    out["corr_ret30_fwdex_fall"] = float(np.corrcoef(-F["ret30"], -F["fwd_ex"])[0, 1])
    out["corr_ret30_fwdex_all"] = float(np.corrcoef(X["ret30"], X["fwd_ex"])[0, 1])
    return out
