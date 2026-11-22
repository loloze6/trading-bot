import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    H = [1, 2, 3, 5, 10]
    # coin drift per horizon (non-overlapping grids)
    drift = {}
    for c in bars:
        for h in H:
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs) if rs else np.nan
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            r1 = pd.Series(cl).pct_change()
            vol = r1.rolling(20).std()
            z = (r1 / vol).values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            f = b["forecast"].values
            reg = b["regime"].values
            f90 = b.get("debug_info.components.fall90.last_history_value", pd.Series(np.nan, index=b.index)).values
            n = len(b)
            for start in range(0, n, 5):
                cell = range(start, min(start + 5, n))
                # first bar in cell with strong short forecast
                sel = [i for i in cell if f[i] <= -2]
                kind = "short"
                if not sel:
                    # comparison: big rise in rising regime
                    sel = [i for i in cell if reg[i] != "mean_reversion" and z[i] > 2]
                    kind = "uptrend_bounce"
                    if not sel:
                        continue
                i = sel[0]
                d = {"coin": c, "win": w, "year": yr[i], "kind": kind, "z": z[i], "f": f[i], "f90": f90[i]}
                for h in H:
                    if i + h < n:
                        d[f"tot{h}"] = -(cl[i + h] / cl[i] - 1)
                        d[f"unu{h}"] = -(cl[i + h] / cl[i] - 1 - drift[(c, h)])
                rows.append(d)
    df = pd.DataFrame(rows)
    def summ(g):
        out = {"n": len(g)}
        for h in H:
            x = g[f"tot{h}"].dropna()
            out[f"tot{h}"] = x.mean()
        x = g["tot5"].dropna(); out["t_tot5"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        x = g["unu5"].dropna(); out["unu5"] = x.mean(); out["t_unu5"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        return pd.Series(out)
    res = {}
    res["by_kind"] = df.groupby("kind").apply(summ)
    s = df[df.kind == "short"].copy()
    s["zq"] = pd.qcut(s["z"], 4, labels=False, duplicates="drop")
    res["short_by_z_quartile"] = s.groupby("zq").apply(summ)
    s["f90q"] = pd.qcut(s["f90"], 5, labels=False, duplicates="drop")
    res["short_by_fall90_quintile"] = s.groupby("f90q").apply(summ)
    res["short_f90_range"] = s.groupby("f90q")["f90"].agg(["min", "max"])
    res["short_by_year"] = s.groupby("year").apply(summ)
    # book
    allb = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            r = b["close"].pct_change().shift(-1)
            g = b["postRebalance_current_allocation"] * r
            allb.append(pd.DataFrame({"pos": b["postRebalance_current_allocation"], "g": g, "fee": (b["total_portfolio_value"].shift(-1) - b["postRebalance_total_value"]) }))
    bb = pd.concat(allb)
    res["bar_gain_short_vs_flat"] = bb.assign(side=np.sign(bb.pos)).groupby("side")["g"].agg(["count", "mean", "sum"])
    tr = pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values()])
    tr["year"] = pd.to_datetime(tr["entry_time"]).dt.year
    res["trades_by_year"] = tr.groupby("year")[["profit_loss_percent", "net_profit_loss_percent"]].agg(["count", "mean"])
    res["trades_all"] = tr[["profit_loss_percent", "net_profit_loss_percent", "duration_minutes"]].describe()
    dd = pd.concat([d.assign(coin=c, win=w) for c in days for w, d in days[c].items()])
    dd["year"] = pd.to_datetime(dd["day"]).dt.year
    res["book_vs_coin_by_year"] = dd.groupby("year")[["book_return", "coin_return"]].mean()
    return res
