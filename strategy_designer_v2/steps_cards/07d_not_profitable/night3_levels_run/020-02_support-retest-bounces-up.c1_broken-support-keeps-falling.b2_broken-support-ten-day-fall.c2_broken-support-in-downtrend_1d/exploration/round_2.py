def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    case_rows = []; drows = []
    for coin, wins in data["bars"].items():
        g = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - 10, 10):
                g.append(c[i + 10] / c[i] - 1)
        drift10 = np.mean(g)
        dr = pd.concat([data["days"][coin][w]["coin_return"] for w in wins]).dropna(); mu = dr.mean()
        for w, b in wins.items():
            c = b["close"].values; f = b["forecast"].fillna(0).values
            r60 = pd.Series(c).pct_change(60).values
            r10p = pd.Series(c).pct_change(10).values
            a = b["postRebalance_current_allocation"].fillna(0).values
            nxt = np.r_[c[1:] / c[:-1] - 1, np.nan]
            for i in range(len(c) - 1):
                drows.append((coin, -f[i], r60[i], r10p[i], a[i], a[i] * nxt[i], a[i] * mu))
            for i in range(0, len(c) - 10, 10):
                if f[i] < 0:
                    tot = -(c[i + 10] / c[i] - 1)
                    case_rows.append({"coin": coin, "absf": -f[i], "tot": tot, "exc": tot + drift10,
                                      "r60": r60[i], "r10": r10p[i]})
    C = pd.DataFrame(case_rows)
    C["fh"] = (C["absf"] >= C["absf"].median()).astype(int)
    C["r60b"] = pd.cut(C["r60"], [-9, -0.3, -0.15, 0], labels=["deep", "mid", "mild"])
    C["r10b"] = pd.cut(C["r10"], [-9, -0.1, 0.05, 9], labels=["fell", "flat", "rose"])
    agg = lambda x: pd.Series({"tot": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))), "n": len(x)})
    out["tot_by_r60_x_fhalf"] = C.groupby(["r60b", "fh"])["tot"].apply(agg).unstack()
    out["tot_by_r10_x_fhalf"] = C.groupby(["r10b", "fh"])["tot"].apply(agg).unstack()
    out["tot_by_r60_x_r10"] = C.groupby(["r60b", "r10b"])["tot"].apply(agg).unstack()
    out["corr_absf_r60_r10"] = C[["absf", "r60", "r10", "tot"]].corr()
    D = pd.DataFrame(drows, columns=["coin", "absf", "r60", "r10", "pos", "gain", "mkt"]).dropna()
    D = D[D["pos"] < 0]
    D["state"] = np.where(D["absf"] > 0, "forecast_on", "held_after_forecast_off")
    out["short_bars_by_state"] = D.groupby("state")[["gain", "mkt", "pos"]].agg(["mean"]).assign(n=D.groupby("state").size())
    D["fq"] = pd.cut(D["absf"], [-1, 0, 5, 10, 15, 21])
    out["short_bar_gain_by_absf"] = D.groupby("fq")[["gain", "mkt"]].mean().assign(n=D.groupby("fq").size())
    return out
