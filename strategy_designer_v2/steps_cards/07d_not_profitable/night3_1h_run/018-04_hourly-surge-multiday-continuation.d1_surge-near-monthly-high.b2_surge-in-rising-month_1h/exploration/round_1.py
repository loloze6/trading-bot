import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    coins = list(bars.keys())
    wins = sorted({w for c in coins for w in bars[c]}, key=lambda s: int(s[1:]))
    # book daily
    seg = []
    per_win = []
    for w in wins:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day", "book_return", "coin_return"]].copy()
                d["coin"] = c
                frames.append(d)
        df = pd.concat(frames)
        g = df.groupby("day")[["book_return", "coin_return"]].mean().sort_index().dropna()
        g["win"] = w
        seg.append(g)
        eq = (1 + g.book_return).cumprod()
        dd = (eq / eq.cummax() - 1).min()
        per_win.append({"win": w, "days": len(g), "book_sum": g.book_return.sum(),
                        "hold_sum": g.coin_return.sum(), "book_maxdd": dd})
    allb = pd.concat(seg).reset_index(drop=True)
    eq = (1 + allb.book_return).cumprod()
    ddser = eq / eq.cummax() - 1
    out["per_window"] = pd.DataFrame(per_win).round(4)
    trough = ddser.idxmin()
    peak = eq[:trough + 1].idxmax()
    out["deepest_fall"] = pd.Series({"dd": ddser.min(), "peak_win": allb.win[peak], "trough_win": allb.win[trough],
                                     "days_long": trough - peak,
                                     "coin_ret_sum_in_fall": allb.coin_return[peak:trough + 1].sum()})
    # second-level: falls by episode (top 5)
    eps = []
    inside = False
    for i, v in ddser.items():
        if v < 0 and not inside:
            inside = True; start = i
        if v == 0 and inside:
            inside = False
            seg_ = ddser[start:i]
            eps.append({"start_win": allb.win[start], "end_win": allb.win[seg_.idxmin()], "dd": seg_.min(), "days": i - start})
    out["top_falls"] = pd.DataFrame(eps).sort_values("dd").head(6).round(4) if eps else "none"
    # trade features
    rows = []
    for c in coins:
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            cl = b.close.values
            ts = pd.to_datetime(b.timestamp).values
            s = pd.Series(cl)
            r720 = s / s.shift(720) - 1
            r24 = s / s.shift(24) - 1
            r168 = s / s.shift(168) - 1
            hi720 = s.rolling(720, min_periods=200).max()
            dist_hi = s / hi720 - 1
            lr = np.log(s).diff()
            vol24 = lr.rolling(24).std(); vol720 = lr.rolling(720, min_periods=200).std()
            vr = vol24 / vol720
            t = trades[c].get(w) if isinstance(trades[c], dict) else None
            if t is None or len(t) == 0:
                continue
            for _, tr in t.iterrows():
                et = np.datetime64(pd.to_datetime(tr.entry_time).tz_localize(None) if pd.to_datetime(tr.entry_time).tzinfo else pd.to_datetime(tr.entry_time))
                tsn = pd.to_datetime(b.timestamp)
                if tsn.dt.tz is not None:
                    tsn = tsn.dt.tz_localize(None)
                i = int(np.searchsorted(tsn.values, et, side="right") - 1)
                if i < 0: continue
                # path within next 240 bars
                j = min(i + 240, len(cl) - 1)
                path = cl[i:j + 1] / cl[i] - 1
                rows.append({"coin": c, "win": w, "pnl": tr.net_profit_loss_percent,
                             "r720": r720[i], "r24": r24[i], "r168": r168[i], "dist_hi": dist_hi[i], "vr": vr[i],
                             "mae": path.min(), "ret240": path[-1],
                             "alloc": b.postRebalance_current_allocation[i] if i < len(b) else np.nan})
    T = pd.DataFrame(rows)
    out["n_trades"] = len(T)
    out["pnl_summary"] = T.pnl.describe().round(3)
    for f in ["r720", "r24", "r168", "dist_hi", "vr"]:
        x = T.dropna(subset=[f, "ret240"])
        q = pd.qcut(x[f], 5, labels=False, duplicates="drop")
        out["by_" + f] = x.groupby(q).agg(lo=(f, "min"), hi=(f, "max"), n=("ret240", "size"),
                                         ret240=("ret240", "mean"), pnl=("pnl", "mean"),
                                         mae=("mae", "mean"), loss_share=("ret240", lambda v: (v < -0.05).mean())).round(4)
    out["by_coin"] = T.groupby("coin").agg(n=("pnl", "size"), pnl=("pnl", "mean"), ret240=("ret240", "mean"), mae=("mae", "mean")).round(3)
    return out
