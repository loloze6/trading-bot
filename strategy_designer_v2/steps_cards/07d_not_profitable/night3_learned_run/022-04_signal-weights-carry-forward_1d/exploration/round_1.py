import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    comps = ["mom","rev","high","vol"]
    rows = []
    # drift per coin
    drift = {}
    for c, ws in data["bars"].items():
        r = []
        for w, b in ws.items():
            cl = b["close"].values
            idx = np.arange(0, len(cl)-5, 5)
            r += list(cl[idx+5]/cl[idx]-1)
        drift[c] = np.mean(r)
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl = b["close"].values
            n = len(cl)
            idx = np.arange(0, n-5, 5)
            fr = cl[idx+5]/cl[idx]-1 - drift[c]
            ret28 = pd.Series(cl).pct_change(28).values[idx]
            ret1 = pd.Series(cl).pct_change(1).values[idx]
            d = {"coin": c, "win": w, "year": pd.to_datetime(b["timestamp"].values[idx]).year,
                 "ex": fr, "fc": b["forecast"].values[idx],
                 "alloc": b["postRebalance_current_allocation"].values[idx],
                 "r28": ret28, "r1": ret1}
            for k in comps:
                d[k+"_raw"] = b[f"debug_info.components.{k}.last_history_value"].values[idx]
                d[k+"_pp"] = b[f"debug_info.components.{k}.post_pipeline_value"].values[idx]
            rows.append(pd.DataFrame(d))
    df = pd.concat(rows, ignore_index=True)
    out = {}
    res = []
    for k in comps + ["fc"]:
        col = k if k=="fc" else k+"_pp"
        s = df[[col,"ex"]].dropna()
        x = np.sign(s[col])*s["ex"]
        prod = s[col]*s["ex"]
        res.append({"sig": k, "n": len(s), "signed_mean_ex": x.mean(), "t_signed": x.mean()/x.std()*np.sqrt(len(x)),
                    "corr": s[col].corr(s["ex"]), "share_pos": (s[col]>0).mean(),
                    "t_prod": prod.mean()/prod.std()*np.sqrt(len(prod))})
    out["per_component"] = pd.DataFrame(res)
    # sign of component vs raw signals (does w_k flip direction?)
    agree = []
    for k, raw in [("mom","r28"),("rev","r1")]:
        s = df[[k+"_raw", raw]].dropna()
        agree.append({"comp": k, "n": len(s), "share_same_sign": (np.sign(s[k+"_raw"])==np.sign(s[raw])).mean()})
    out["comp_vs_raw_sign"] = pd.DataFrame(agree)
    # raw signals' own predictive power
    res2 = []
    for raw in ["r28","r1"]:
        s = df[[raw,"ex"]].dropna()
        x = np.sign(s[raw])*s["ex"]
        res2.append({"raw": raw, "n": len(s), "signed_mean": x.mean(), "t": x.mean()/x.std()*np.sqrt(len(x)), "corr": s[raw].corr(s["ex"])})
    out["raw_signals"] = pd.DataFrame(res2)
    # forecast by year
    g = df.dropna(subset=["fc"]).assign(sx=lambda d: np.sign(d.fc)*d.ex)
    out["fc_by_year"] = g.groupby("year").agg(n=("sx","size"), mean=("sx","mean"), share_long=("fc", lambda v:(v>0).mean()))
    out["fc_by_coin"] = g.groupby("coin").agg(n=("sx","size"), mean=("sx","mean"), share_long=("fc", lambda v:(v>0).mean()))
    # book: market part vs timing
    bk = []
    for c, ws in data["days"].items():
        mu = pd.concat([d["coin_return"] for d in ws.values()]).mean()
        for w, d in ws.items():
            b = data["bars"][c][w]
            al = b.groupby(pd.to_datetime(b["timestamp"]).dt.floor("D"))["postRebalance_current_allocation"].last().shift(1)
            dd = d.copy(); dd["day"] = pd.to_datetime(dd["day"])
            dd = dd.merge(al.rename("al").reset_index().rename(columns={"timestamp":"day"}), on="day", how="left")
            dd["mkt"] = dd["al"]*mu; dd["coin"]=c
            bk.append(dd)
    bk = pd.concat(bk)
    out["book"] = pd.Series({"mean_book": bk.book_return.mean(), "market_part": bk.mkt.mean(),
                             "timing": bk.book_return.mean()-bk.mkt.mean(), "mean_abs_alloc": bk.al.abs().mean(),
                             "share_long_days": (bk.al>0).mean(), "share_short_days": (bk.al<0).mean()})
    return out
