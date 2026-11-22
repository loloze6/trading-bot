import numpy as np, pandas as pd

def explore(data):
    H = [2, 3, 6]
    rows = []
    drift = {}
    for coin, ws in data["bars"].items():
        for h in H:
            rs = []
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.concatenate(rs).mean()
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            f = b["forecast"].values
            fl = b["debug_info.components.fall.last_history_value"].values
            fv = b["debug_info.components.fall_x_volume.last_history_value"].values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            n = len(b)
            for s in range(0, n, 3):
                cell = np.where(f[s:s+3] >= 2)[0]
                if len(cell) == 0:
                    continue
                t = s + cell[0]
                v = fv[t] / fl[t] if (np.isfinite(fl[t]) and fl[t] != 0) else np.nan
                d = {"coin": coin, "year": yr[t], "fall": fl[t], "v": v}
                for h in H:
                    d[f"u{h}"] = (c[t+h] / c[t] - 1 - drift[(coin, h)]) if t + h < n else np.nan
                rows.append(d)
    df = pd.DataFrame(rows)
    df["v"] = df["v"].replace([np.inf, -np.inf], np.nan)

    def summ(g):
        out = {}
        for h in H:
            x = g[f"u{h}"].dropna()
            out[f"m{h}_bp"] = x.mean() * 1e4
            out[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        out["n"] = len(g)
        return pd.Series(out)

    res = {}
    df["fq"] = pd.qcut(df["fall"], 5, labels=False, duplicates="drop")
    df["vh"] = pd.qcut(df["v"], 2, labels=["thin", "heavy"])
    res["3h_grid_by_fall_q"] = df.groupby("fq").apply(summ)
    res["fall_q_x_vol_half"] = df.groupby(["fq", "vh"]).apply(summ)[["m3_bp", "t3", "n"]]
    deep = df[df["fq"] <= 1]
    res["deep2q_by_coin"] = deep.groupby("coin").apply(summ)
    res["deep2q_by_year"] = deep.groupby("year").apply(summ)[["m3_bp", "t3", "n"]]
    # graded: correlation of fall depth with 3h unusual move
    x = df[["fall", "u3"]].dropna()
    r = np.corrcoef(-x["fall"], x["u3"])[0, 1]
    res["corr_depth_u3"] = pd.Series({"r": r, "t": r * np.sqrt((len(x) - 2) / (1 - r**2)), "n": len(x)})
    xv = df[["v", "u3"]].dropna()
    rv = np.corrcoef(xv["v"], xv["u3"])[0, 1]
    res["corr_v_u3"] = pd.Series({"r": rv, "t": rv * np.sqrt((len(xv) - 2) / (1 - rv**2)), "n": len(xv)})
    return res
