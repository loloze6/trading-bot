import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    col = "debug_info.components.vol_surge_up.last_history_value"
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            raw = pd.to_numeric(b[col], errors="coerce").values if col in b else np.full(len(b), np.nan)
            r1 = pd.Series(c).pct_change()
            sd = r1.rolling(720, min_periods=240).std()
            vr = b["volume"] / b["volume"].rolling(720, min_periods=240).mean()
            zr = (r1 / sd).values
            year = pd.to_datetime(b["timestamp"]).dt.year.values
            n = len(b)
            for h in (1, 2, 4, 6, 12):
                idx = np.arange(0, n - h, h)
                fr = c[idx + h] / c[idx] - 1
                for i, f in zip(idx, fr):
                    rows.append((coin, w, year[i], h, raw[i], zr[i], vr.values[i], f))
    df = pd.DataFrame(rows, columns=["coin", "w", "year", "h", "raw", "zr", "vr", "fr"])
    df["drift"] = df.groupby(["coin", "h"])["fr"].transform("mean")
    df["ex"] = df["fr"] - df["drift"]
    out = {}
    d = df.dropna(subset=["zr", "vr"]).copy()
    # bins by signed move and volume
    d["zbin"] = pd.cut(d["zr"], [-np.inf, -4, -2.5, -1.5, 1.5, 2.5, 4, np.inf])
    d["vbin"] = pd.cut(d["vr"], [0, 1.5, 3, np.inf])
    def agg(g):
        m = g["ex"].mean(); s = g["ex"].std(); n = len(g)
        return pd.Series({"n": n, "mean_ex_bp": m * 1e4, "t": m / (s / np.sqrt(n)) if n > 2 else np.nan})
    for h in (1, 2, 4, 6, 12):
        out[f"h{h}_z_x_vol"] = d[d.h == h].groupby(["zbin", "vbin"], observed=True).apply(agg).round(2)
    big = d[(d.h == 4) & (d.zr.abs() > 2.5) & (d.vr > 3)].copy()
    big["dir_ex"] = np.sign(big["zr"]) * big["ex"]
    big["side"] = np.where(big.zr > 0, "up", "down")
    out["h4_extreme_by_coin_side"] = big.groupby(["coin", "side"]).apply(lambda g: agg(g.assign(ex=g.dir_ex))).round(2)
    out["h4_extreme_by_year"] = big.groupby(["year"]).apply(lambda g: agg(g.assign(ex=g.dir_ex))).round(2)
    # raw component deciles, h=4
    d4 = df[(df.h == 4)].dropna(subset=["raw"]).copy()
    pos = d4[d4.raw > 0].copy()
    pos["q"] = pd.qcut(pos.raw, 10, labels=False, duplicates="drop")
    out["h4_raw_pos_deciles"] = pos.groupby("q").apply(agg).round(2)
    out["raw_pos_quantiles"] = pos.raw.quantile([.5, .9, .99, .999]).round(3)
    out["share_bars_forecast_pos"] = float(np.mean([ (b["forecast"] > 0).mean() for ws in data["bars"].values() for b in ws.values()]))
    return out
