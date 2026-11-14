def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            b["ts"] = pd.to_datetime(b["timestamp"])
            lc = np.log(b["close"])
            b["r1"] = lc.diff()
            b["f12"] = lc.shift(-12) - lc
            b["f1"] = lc.shift(-1) - lc
            b["p12"] = lc - lc.shift(12)
            b["p1"] = b["r1"]
            b["vol24"] = b["r1"].rolling(24).std()
            b["raw"] = b["debug_info.components.rsi_high.last_history_value"]
            b["pos"] = b["postRebalance_current_allocation"]
            pv = b["postRebalance_total_value"]
            b["bookr1"] = np.log(pv).diff().shift(-1)  # book return over next bar
            b["coin"] = coin; b["win"] = w
            b["drift12"] = b["f12"].mean()
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    d["ex12"] = d["f12"] - d["drift12"]
    # raw RSI pullback deciles (both sides)
    d["rawdec"] = d.groupby("coin")["raw"].transform(lambda s: pd.qcut(s, 10, labels=False, duplicates="drop"))
    g = d.groupby(["rawdec"]).agg(raw_mean=("raw","mean"), ex12_bp=("ex12", lambda x: 1e4*x.mean()),
                                   f1_bp=("f1", lambda x: 1e4*x.mean()), n=("ex12","count"))
    g2 = d[d.index % 12 == 0].groupby("rawdec")["ex12"].apply(lambda x: x.mean()/x.std()*np.sqrt(x.count()))
    g["t_nonovl"] = g2
    out["ex12 by raw(50-RSI) decile pooled"] = g.round(3)
    out["ex12 bp by coin x raw decile"] = (d.groupby(["rawdec","coin"])["ex12"].mean().unstack()*1e4).round(1)
    # past 12h move deciles
    d["p12dec"] = d.groupby("coin")["p12"].transform(lambda s: pd.qcut(s, 10, labels=False))
    out["ex12 bp by past12h move decile x coin"] = (d.groupby(["p12dec","coin"])["ex12"].mean().unstack()*1e4).round(1)
    # past 1h move deciles, next 1h
    d["p1dec"] = d.groupby("coin")["p1"].transform(lambda s: pd.qcut(s, 10, labels=False))
    out["next1h bp by past1h decile x coin"] = (d.groupby(["p1dec","coin"])["f1"].mean().unstack()*1e4).round(2)
    # vol tercile
    d["voltc"] = d.groupby("coin")["vol24"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["ex12 bp by vol tercile x coin; book next-bar bp"] = pd.concat([
        (d.groupby(["voltc","coin"])["ex12"].mean().unstack()*1e4).round(1),
        (d.groupby("voltc")["bookr1"].mean()*1e4).round(2).rename("book_bp")], axis=1)
    # hour / weekday
    d["hour"] = d["ts"].dt.hour; d["wd"] = d["ts"].dt.weekday
    h = d.groupby("hour").agg(f1_bp=("f1", lambda x: 1e4*x.mean()), t=("f1", lambda x: x.mean()/x.std()*np.sqrt(x.count())),
                              absr_bp=("f1", lambda x: 1e4*x.abs().mean()), book_bp=("bookr1", lambda x: 1e4*x.mean()))
    out["by hour"] = h.round(2)
    wd = d.groupby("wd").agg(f1_bp=("f1", lambda x: 1e4*x.mean()), t=("f1", lambda x: x.mean()/x.std()*np.sqrt(x.count())),
                             absr_bp=("f1", lambda x: 1e4*x.abs().mean()), book_bp=("bookr1", lambda x: 1e4*x.mean()))
    out["by weekday"] = wd.round(2)
    # book
    d["pos_on"] = d["pos"].abs() > 1e-6
    out["book summary"] = pd.Series({
        "share bars in position": d["pos_on"].mean(),
        "mean pos when on": d.loc[d.pos_on,"pos"].mean(),
        "book next-bar bp when on": 1e4*d.loc[d.pos_on,"bookr1"].mean(),
        "book next-bar bp when off": 1e4*d.loc[~d.pos_on,"bookr1"].mean(),
        "coin next-bar bp when on": 1e4*d.loc[d.pos_on,"f1"].mean(),
        "mean |pos change| per bar": d["pos"].diff().abs().mean(),
        "corr pos vs f1": d[["pos","f1"]].corr().iloc[0,1],
    }).round(4)
    tr = pd.concat([t.assign(coin=c, win=w) for c, ws in data["trades"].items() for w, t in ws.items()], ignore_index=True)
    out["trades"] = pd.Series({
        "n": len(tr), "mean gross %": tr.profit_loss_percent.mean(), "mean net %": tr.net_profit_loss_percent.mean(),
        "win rate gross": (tr.profit_loss_percent>0).mean(), "median dur h": tr.duration_minutes.median()/60,
        "mean commission": tr.total_commission.mean(),
        "share side SHORT": (tr.side=="SHORT").mean()}).round(4)
    tr["durq"] = pd.qcut(tr.duration_minutes, 4, labels=False, duplicates="drop")
    out["trades by duration quartile"] = tr.groupby("durq").agg(dur_h=("duration_minutes", lambda x: x.mean()/60),
        gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"), n=("side","count")).round(4)
    days = pd.concat([t.assign(coin=c, win=w) for c, ws in data["days"].items() for w, t in ws.items()], ignore_index=True)
    out["book vs coin daily by coin x window"] = days.groupby(["coin","win"]).agg(book=("book_return","mean"), coin_r=("coin_return","mean"),
        corr=("book_return", lambda x: np.nan)).drop(columns="corr").mul(1e4).round(1)
    return out
