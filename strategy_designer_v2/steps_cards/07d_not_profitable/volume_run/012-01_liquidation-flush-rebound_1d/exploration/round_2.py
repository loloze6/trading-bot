def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = c; d["w"] = w
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["wn"] = D["w"].str[1:].astype(int)
    port = D.groupby(["wn", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).dropna().sort_index().reset_index()
    eq = (1 + port["br"]).cumprod()
    dd = eq / eq.cummax() - 1
    port["dd"] = dd.values
    out["port_summary"] = pd.Series({"mean": port.br.mean(), "sd": port.br.std(), "n": len(port), "maxdd": dd.min(), "hold_mean": port.cr.mean(),
                                     "worst20_share_of_sum_neg": port.br.nsmallest(20).sum() / port.br[port.br < 0].sum()})
    out["port_by_window"] = port.groupby("wn").agg(book=("br", "sum"), hold=("cr", "sum"), mindd=("dd", "min"))
    try:
        recs = []
        for c, ws in data["bars"].items():
            for w, b in ws.items():
                b = b.reset_index(drop=True).copy()
                b["r1"] = b.close.shift(-1) / b.close - 1
                b["alloc"] = b.postRebalance_current_allocation.fillna(0)
                b["prev"] = b.previous_allocation.fillna(0)
                b["gain"] = b.alloc * b.r1
                b["ret20"] = b.close / b.close.shift(20) - 1
                b["ret60"] = b.close / b.close.shift(60) - 1
                b["ma50dist"] = b.close / b.close.rolling(50).mean() - 1
                b["rv20"] = b.close.pct_change().rolling(20).std()
                b["fee"] = (b.total_portfolio_value - b.postRebalance_total_value) / b.total_portfolio_value
                b["inpos"] = b.alloc.abs() > 1e-9
                b["entry"] = b.inpos & ~(b.prev.abs() > 1e-9)
                b["grp"] = b.entry.cumsum()
                b["k"] = np.where(b.inpos, b.groupby("grp").cumcount(), -1)
                b["coin"] = c; b["w"] = w
                recs.append(b)
        B = pd.concat(recs, ignore_index=True)
        out["basic"] = pd.Series({"share_in_pos": B.inpos.mean(), "mean_alloc_in": B.loc[B.inpos, "alloc"].mean(),
                                  "gross_gain_per_bar": B.gain.mean(), "fee_per_bar": B.fee.mean(),
                                  "hold_r1_mean": B.r1.mean(), "r1_in_pos": B.loc[B.inpos, "r1"].mean()})
        I = B[B.inpos].dropna(subset=["gain", "ret60"]).copy()
        I["q60"] = pd.qcut(I.ret60, 5, labels=False)
        out["in_by_ret60_q"] = I.groupby("q60").agg(n=("gain", "size"), gain=("gain", "mean"), r1=("r1", "mean"), ret60=("ret60", "median"), alloc=("alloc", "mean"))
        I["q20"] = pd.qcut(I.ret20, 5, labels=False)
        out["in_by_ret20_q"] = I.groupby("q20").agg(n=("gain", "size"), gain=("gain", "mean"), r1=("r1", "mean"), ret20=("ret20", "median"))
        I["qv"] = pd.qcut(I.rv20, 5, labels=False)
        out["in_by_vol_q"] = I.groupby("qv").agg(n=("gain", "size"), gain=("gain", "mean"), r1=("r1", "mean"), rv=("rv20", "median"))
        out["in_by_above50"] = I.groupby(I.ma50dist > 0).agg(n=("gain", "size"), gain=("gain", "mean"), r1=("r1", "mean"), sd=("gain", "std"))
        out["by_bar_since_entry"] = B[B.inpos].groupby(B.loc[B.inpos, "k"].clip(upper=6)).agg(n=("gain", "size"), gain=("gain", "mean"), r1=("r1", "mean"))
        out["by_coin"] = B.groupby("coin").agg(gain=("gain", "mean"), fee=("fee", "mean"), inpos=("inpos", "mean"))
        # worst book days: context of held coins
        B["day"] = pd.to_datetime(B.timestamp).dt.floor("D")
        held = B[B.inpos]
        out["held_loss_tail"] = pd.Series({"gain_p1": held.gain.quantile(0.01), "gain_p5": held.gain.quantile(0.05),
                                           "share_ret60neg_in_worst5pct": (held.loc[held.gain <= held.gain.quantile(0.05), "ret60"] < 0).mean(),
                                           "share_ret60neg_all_held": (held.ret60 < 0).mean()})
    except Exception as e:
        out["err"] = str(e)
    try:
        T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items()], ignore_index=True)
        T["days"] = T.duration_minutes / 1440
        out["trades"] = pd.Series({"n": len(T), "net": T.net_profit_loss_percent.mean(), "gross": T.profit_loss_percent.mean(),
                                   "med_days": T.days.median(), "win": (T.net_profit_loss_percent > 0).mean()})
        T["db"] = pd.cut(T.days, [0, 1.5, 3.5, 7.5, 1000])
        out["trades_by_dur"] = T.groupby("db").agg(n=("days", "size"), net=("net_profit_loss_percent", "mean"), gross=("profit_loss_percent", "mean"))
    except Exception as e:
        out["terr"] = str(e)
    return out
