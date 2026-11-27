import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            if len(b) < 5: continue
            c = b["close"]; r = c.pct_change()
            s30 = r.rolling(30, min_periods=15).std()
            mid = (b["high"] + b["low"]) / 2
            hl = (b["high"] - b["low"]).replace(0, np.nan)
            clv = 2 * (c - mid) / hl
            width = (hl / c) / s30
            tr60 = c / c.shift(60) - 1
            d = pd.DataFrame({
                "coin": coin, "win": w, "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "r0": r, "clv": clv, "width": width,
                "nxt": c.shift(-1) / c - 1, "nxt2": c.shift(-2) / c.shift(-1) - 1,
                "nxt3": c.shift(-3) / c - 1,
                "s30": s30, "tr60": tr60, "tr10": c / c.shift(10) - 1,
                "inprof": (b["regime"] == "unknown"),
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for col in ["nxt", "nxt2", "nxt3"]:
        D["ex_" + col] = D[col] - D["coin"].map(D.groupby("coin")[col].mean())
    D = D.dropna(subset=["ex_nxt", "clv", "width", "s30"])
    D["fade"] = -D["clv"] * D["width"]
    D["sq"] = D.groupby("coin")["s30"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    D["trb"] = pd.cut(D["tr60"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    D["side"] = np.where(D["fade"] > 0, "long", "short")
    D["big"] = D["fade"].abs() > D["fade"].abs().quantile(0.5)

    def ct(sub, col="sx"):
        g = sub.groupby("day")[col].sum()
        return pd.Series({"n": len(sub), "days": len(g), "mean": sub[col].mean(),
                          "t": g.mean() / (g.std() / np.sqrt(len(g))) if len(g) > 4 else np.nan})
    out = {}
    B = D[D["big"]].copy()
    B["sx"] = np.sign(B["fade"]) * B["ex_nxt"]
    B["sx2"] = np.sign(B["fade"]) * B["ex_nxt2"]
    out["signedfade_big_by_vol_side"] = B.groupby(["sq", "side"]).apply(ct).round(4)
    out["signedfade_big_by_vol_trend_short"] = B[B.side == "short"].dropna(subset=["trb"]).groupby(["trb", "sq"]).apply(ct).round(4)
    out["signedfade_big_by_vol_trend_long"] = B[B.side == "long"].dropna(subset=["trb"]).groupby(["trb", "sq"]).apply(ct).round(4)
    out["day2_signedfade_by_vol"] = B.groupby("sq").apply(lambda s: ct(s, "sx2")).round(4)
    # graded: within high-vol tercile, quintile of |fade|, short side
    H = D[D.sq == 2].copy()
    H["sx"] = np.sign(H["fade"]) * H["ex_nxt"]
    H["aq"] = H.groupby("side")["fade"].transform(lambda x: pd.qcut(x.abs(), 4, labels=False, duplicates="drop"))
    out["highvol_by_side_absfadeQ"] = H.groupby(["side", "aq"]).apply(ct).round(4)
    out["highvol_signedfade_by_year"] = B[B.sq == 2].groupby("yr").apply(ct).round(4)
    out["highvol_signedfade_by_coin"] = B[B.sq == 2].groupby("coin").apply(ct).round(4)
    # strength in usual moves
    B["sxz"] = B["sx"] / B["s30"]
    out["strength_big_by_vol"] = B.groupby("sq")["sxz"].agg(["count", "mean"]).round(4)
    return out
