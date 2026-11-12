def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            b["ts"] = pd.to_datetime(b["timestamp"])
            lc = np.log(b["close"])
            b["r1"] = lc.diff()
            b["f12"] = lc.shift(-12) - lc
            b["f1"] = lc.shift(-1) - lc
            b["p12"] = lc - lc.shift(12)
            b["p48"] = lc - lc.shift(48)
            b["vol24"] = b["r1"].rolling(24).std()
            b["vol24_rel"] = b["vol24"] / b["vol24"].rolling(240, min_periods=60).median()
            b["raw"] = b["debug_info.components.rsi_high.last_history_value"]
            b["pos"] = b["postRebalance_current_allocation"]
            pv = b["postRebalance_total_value"]
            b["bookr1"] = np.log(pv).diff().shift(-1)
            b["gross1"] = b["pos"] * b["f1"]
            b["fee1"] = b["gross1"] - b["bookr1"]
            b["dpos"] = b["pos"].diff().abs()
            b["grid"] = (np.arange(len(b)) % 12 == 0)
            b["coin"] = coin; b["win"] = w
            b["ex12"] = b["f12"] - b["f12"].mean()
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    def tstat(x):
        x = x.dropna(); return x.mean()/x.std()*np.sqrt(len(x)) if len(x) > 2 else np.nan
    # momentum past 12h deciles, non-overlapping t, by coin
    d["p12dec"] = d.groupby("coin")["p12"].transform(lambda s: pd.qcut(s, 10, labels=False))
    g = d[d.grid].groupby(["p12dec","coin"])["ex12"].agg(lambda x: tstat(x)).unstack()
    out["t nonovl ex12 by past12h decile x coin"] = g.round(2)
    # top-bottom spread by window
    sp = d.groupby(["coin","win"]).apply(lambda x: 1e4*(x.loc[x.p12dec==9,"ex12"].mean()-x.loc[x.p12dec==0,"ex12"].mean()))
    out["p12 top-minus-bottom decile ex12 bp by coin x win"] = sp.unstack().round(1)
    # p48 momentum
    d["p48dec"] = d.groupby("coin")["p48"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["ex12 bp by past48h quintile x coin"] = (d.groupby(["p48dec","coin"])["ex12"].mean().unstack()*1e4).round(1)
    # momentum x vol regime
    d["vq"] = d.groupby("coin")["vol24_rel"].transform(lambda s: pd.qcut(s, 3, labels=False))
    d["p12sgn"] = np.where(d.p12dec>=7, "up", np.where(d.p12dec<=2, "down", "mid"))
    out["ex12 bp by rel-vol tercile x past12h group"] = (d.groupby(["vq","p12sgn"])["ex12"].mean().unstack()*1e4).round(1)
    # book decomposition
    on = d.pos.abs() > 1e-6
    out["book decomposition bp per bar"] = pd.Series({
        "book": 1e4*d.bookr1.mean(), "gross pos*f1": 1e4*d.gross1.mean(), "fee+slip": 1e4*d.fee1.mean(),
        "mean |dpos|": d.dpos.mean(), "share bars dpos>0": (d.dpos>1e-6).mean(),
        "gross when on": 1e4*d.loc[on,"gross1"].mean()}).round(3)
    # position size buckets -> gross pnl and coin move
    d["posb"] = pd.cut(d.pos, [-1.01,-0.95,-0.5,-0.1,-1e-6,1e-6], labels=["<-0.95","-0.95..-0.5","-0.5..-0.1","-0.1..0","flat"])
    out["by position bucket"] = d.groupby("posb").agg(n=("f1","count"), coin_f1_bp=("f1", lambda x:1e4*x.mean()),
        ex12_bp=("ex12", lambda x:1e4*x.mean()), gross_bp=("gross1", lambda x:1e4*x.mean()), fee_bp=("fee1", lambda x:1e4*x.mean())).round(2)
    # hour 19/21 and 0 by coin
    d["hour"] = d.ts.dt.hour
    hh = d[d.hour.isin([0,12,16,19,20,21])].groupby(["hour","coin"])["f1"].agg(lambda x: tstat(x)).unstack()
    out["t next1h by selected hour x coin"] = hh.round(2)
    hy = d[d.hour.isin([0,19,21])].assign(yr=d.ts.dt.year).groupby(["hour","yr"])["f1"].mean().unstack()*1e4
    out["next1h bp selected hours by year"] = hy.round(1)
    # around book's largest losses/gains (bar level)
    d["idx"] = d.groupby(["coin","win"]).cumcount()
    q_lo, q_hi = d.bookr1.quantile(0.01), d.bookr1.quantile(0.99)
    res = {}
    for name, mask in [("worst1%", d.bookr1<=q_lo), ("best1%", d.bookr1>=q_hi)]:
        s = d[mask]
        res[name] = {"n": len(s), "past12 bp": 1e4*s.p12.mean(), "raw": s.raw.mean(), "pos": s.pos.mean(),
                     "coin f1 bp": 1e4*s.f1.mean(), "next12 ex bp": 1e4*s.ex12.mean(), "rel vol": s.vol24_rel.mean(),
                     "share hour 12-16": s.hour.between(12,16).mean()}
    out["around largest book bars"] = pd.DataFrame(res).round(3)
    # trades by entry forecast size and duration
    tr = pd.concat([t.assign(coin=c, win=w) for c, ws in data["trades"].items() for w, t in ws.items()], ignore_index=True)
    tr["fq"] = pd.qcut(tr.entry_forecast.abs(), 4, labels=False, duplicates="drop")
    out["trades by |entry forecast| quartile"] = tr.groupby("fq").agg(f=("entry_forecast", lambda x: x.abs().mean()),
        dur_h=("duration_minutes", lambda x: x.mean()/60), gross=("profit_loss_percent","mean"),
        win=("profit_loss_percent", lambda x:(x>0).mean()), n=("side","count")).round(3)
    return out
