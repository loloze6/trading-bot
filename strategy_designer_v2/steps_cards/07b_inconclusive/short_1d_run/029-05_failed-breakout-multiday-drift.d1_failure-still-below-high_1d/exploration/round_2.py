import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H_list = [2, 4, 8, 16]
    drift = {}; usual = {}
    for c in bars:
        for h in H_list:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                if len(idx):
                    rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs) if rs else np.nan
            usual[(c, h)] = np.std(rs) if rs else np.nan
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values.astype(float)
            f = df["forecast"].fillna(0).values.astype(float)
            n = len(cl)
            year = pd.to_datetime(df["timestamp"]).dt.year.values
            s = pd.Series(cl)
            r20 = s.pct_change(20).values
            r60 = s.pct_change(60).values
            vol20 = s.pct_change().rolling(20).std().values
            depth = df.get("debug_info.components.depth.last_history_value")
            depth = depth.values.astype(float) if depth is not None else np.full(n, np.nan)
            for start in range(0, n, 8):
                end = min(start + 8, n)
                sel = [i for i in range(start, end) if f[i] <= -2]
                if not sel:
                    continue
                i = sel[0]
                rec = {"coin": c, "win": w, "year": int(year[i]), "absf": -f[i],
                       "r20": r20[i], "r60": r60[i], "vol20": vol20[i], "depth": depth[i]}
                for h in H_list:
                    if i + h < n:
                        tot = -(cl[i + h] / cl[i] - 1)
                        rec[f"u{h}"] = tot + drift[(c, h)]
                        rec[f"t{h}"] = tot
                rows.append(rec)
    d = pd.DataFrame(rows)

    def summ(x):
        x = pd.Series(x).dropna()
        if len(x) < 3:
            return {"n": len(x), "mean": np.nan, "t": np.nan}
        return {"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))}

    def grp(key, col="u8"):
        return pd.DataFrame({k: summ(g[col]) for k, g in d.groupby(key)}).T

    def terc(col):
        r = d[col].rank(method="first")
        return pd.qcut(r, 3, labels=["low", "mid", "high"])

    out = {}
    out["overall_by_horizon_unusual"] = pd.DataFrame({h: summ(d[f"u{h}"]) for h in H_list}).T
    out["overall_by_horizon_total"] = pd.DataFrame({h: summ(d[f"t{h}"]) for h in H_list}).T
    out["by_coin_u8"] = grp("coin")
    out["by_coin_u16"] = grp("coin", "u16")
    out["by_year_u8"] = grp("year")
    d["fq"] = terc("absf")
    out["by_forecast_tercile_u8"] = grp("fq")
    d["dq"] = terc("depth")
    out["by_depth_tercile_u8"] = grp("dq")
    d["tr20"] = np.where(d["r20"] > 0, "r20_up", "r20_down")
    out["by_prior20d_u8"] = grp("tr20")
    d["tr60"] = np.where(d["r60"] > 0, "r60_up", "r60_down")
    out["by_prior60d_u8"] = grp("tr60")
    out["by_prior60d_u16"] = grp("tr60", "u16")
    d["vq"] = terc("vol20")
    out["by_vol_tercile_u8"] = grp("vq")
    sub = d.dropna(subset=["u8", "absf"])
    sl = stats.linregress(sub["absf"], sub["u8"])
    out["slope_u8_on_absf"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(sub)})
    out["usual8"] = pd.Series({c: usual[(c, 8)] for c in bars})
    return out
