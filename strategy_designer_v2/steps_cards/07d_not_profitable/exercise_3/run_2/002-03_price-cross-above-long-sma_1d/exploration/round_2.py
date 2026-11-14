import numpy as np, pandas as pd

def explore(data):
    out = {}
    H = 20
    pm = {c: pd.concat([b["close"].pct_change().dropna() for b in ws.values()]).mean() for c, ws in data["bars"].items()}
    dl = []; nb = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; raw = b["debug_info.components.above_ma.last_history_value"]
            sma = cl/(1+raw/100.0)
            slope = sma/sma.shift(20)-1
            al = b["postRebalance_current_allocation"]
            r1 = cl.shift(-1)/cl-1
            f = b["forecast"].values
            run = np.zeros(len(b))
            for i in range(len(b)):
                run[i] = (run[i-1]+1 if i>0 else 1) if f[i] > 0 else 0
            tv = b["postRebalance_total_value"]
            dd = tv/tv.cummax()-1
            ddc = cl/cl.cummax()-1
            past60 = cl/cl.shift(60)-1
            df = pd.DataFrame(dict(coin=c, win=w, al=al, g=al*r1, r1=r1, f=b["forecast"], slope=slope,
                                   run=run, dd=dd, ddc=ddc, raw=raw, past60=past60))
            dl.append(df)
            for i in range(0, len(b)-H, H):
                nb.append(dict(coin=c, f=f[i], slope=slope.iloc[i], run=run[i],
                               ex=cl.iloc[i+H]/cl.iloc[i]-1-H*pm[c], al=al.iloc[i]))
    d = pd.concat(dl)
    h = d[(d.al > 0)].dropna(subset=["g"])
    def tab(gb):
        return pd.DataFrame({"n": gb.size(), "mean_gain": gb["g"].mean(), "sum_gain": gb["g"].sum(),
                             "t": gb["g"].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s)))), "mean_al": gb["al"].mean()})
    h = h.copy()
    h["slb"] = pd.cut(h["slope"], [-1, -0.05, 0, 0.05, 0.15, 10])
    out["held days by SMA200 20d slope"] = tab(h.groupby("slb", observed=True))
    h["runb"] = pd.cut(h["run"], [0, 10, 30, 60, 150, 10000])
    out["held days by days since on"] = tab(h.groupby("runb", observed=True))
    h["ddb"] = pd.cut(h["dd"], [-1.01, -0.6, -0.4, -0.2, -0.0001, 0.01])
    out["held days by book drawdown depth"] = tab(h.groupby("ddb", observed=True))
    h["p60"] = pd.cut(h["past60"], [-1, 0, 0.3, 0.8, 100])
    out["held days by past60 return"] = tab(h.groupby("p60", observed=True))
    # share of losses: worst 5% held days
    q = h["g"].quantile(0.05)
    w5 = h[h.g <= q]
    out["worst5pct held days profile"] = pd.DataFrame({"mean_slope": [w5.slope.mean(), h.slope.mean()],
        "mean_run": [w5.run.mean(), h.run.mean()], "mean_al": [w5.al.mean(), h.al.mean()],
        "mean_raw": [w5.raw.mean(), h.raw.mean()]}, index=["worst5", "all_held"])
    n = pd.DataFrame(nb); a = n[n.f > 0].copy()
    a["slb"] = pd.cut(a["slope"], [-1, 0, 0.05, 0.15, 10])
    g = a.groupby("slb", observed=True)["ex"]
    out["nonoverlap active excess20 by slope"] = pd.DataFrame({"n": g.size(), "mean": g.mean(),
        "t": g.apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s))))})
    # time held fraction and book-days in drawdown
    allb = d.dropna(subset=["g"])
    out["share days held"] = float((allb.al > 0).mean())
    # Sharpe/calmar-like sim: gain only when slope>0
    sim = allb.copy(); sim["g2"] = np.where(sim.slope > 0, sim.g, 0.0)
    out["daily-bar sharpe all vs slope>0 only"] = pd.Series({
        "all": sim.g.mean()/sim.g.std()*np.sqrt(365), "slope_pos": sim.g2.mean()/sim.g2.std()*np.sqrt(365),
        "hold": sim.r1.mean()/sim.r1.std()*np.sqrt(365)})
    return out
