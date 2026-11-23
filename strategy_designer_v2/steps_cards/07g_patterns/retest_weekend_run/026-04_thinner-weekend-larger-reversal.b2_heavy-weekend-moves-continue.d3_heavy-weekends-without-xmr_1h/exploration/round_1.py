def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; hr = []
    for coin, wins in data["bars"].items():
        # usual 48h move
        g = []
        for w, b in wins.items():
            c = b["close"].values
            g += list(c[48::48]/c[:-48:48][:len(c[48::48])]-1)
        sd48 = np.std(g); mu48 = np.mean(g)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]); c = b["close"].values; v = b["volume"].values.astype(float)
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            hr.append(pd.DataFrame({"coin":coin,"hour":ts.dt.hour,"wd":ts.dt.weekday,"r":r1,
                                    "absr":np.abs(np.r_[np.nan, r1[:-1]]), "rprev":np.r_[np.nan, r1[:-1]]}))
            idx = np.where(ts.dt.hour.values==23)[0]
            for i in idx:
                if i-168 < 0 or i+72 >= len(c): continue
                past = c[i]/c[i-48]-1
                vr = v[i-47:i+1].mean()/max(v[i-167:i-47].mean(),1e-12)
                f24 = c[i+24]/c[i]-1; f48 = c[i+48]/c[i]-1; f72 = c[i+72]/c[i]-1
                rows.append(dict(coin=coin, win=w, year=ts[i].year, wd=ts[i].weekday(), pz=past/sd48,
                                 vr=vr, f48=(f48-mu48)/sd48, f24=f24/sd48, f72=f72/sd48, raw48=f48-mu48,
                                 fc=b["forecast"].iloc[i]))
    d = pd.DataFrame(rows)
    def slope(x, y):
        m = np.isfinite(x)&np.isfinite(y); x=x[m]; y=y[m]
        r = stats.linregress(x, y); return r.slope, r.slope/r.stderr, len(x)
    res = []
    for wd in range(7):
        s = d[d.wd==wd]
        for lab, ss in [("all", s), ("heavy", s[s.vr>1]), ("light", s[s.vr<=1])]:
            b_, t_, n = slope(ss.pz.values, ss.f48.values)
            sg = np.sign(ss.pz)*ss.f48
            res.append(dict(endday=wd, grp=lab, n=n, slope48=b_, t=t_, signed_mean=sg.mean(),
                            t_signed=sg.mean()/sg.std()*np.sqrt(len(sg))))
    out["follow48_by_day_ending_23h"] = pd.DataFrame(res)
    s = d[d.wd==6].copy()
    s["sg48"]=np.sign(s.pz)*s.f48; s["sg24"]=np.sign(s.pz)*s.f24; s["sg72"]=np.sign(s.pz)*s.f72
    s["pzq"]=pd.qcut(s.pz.abs(),5,labels=False); s["vrq"]=pd.qcut(s.vr,5,labels=False)
    out["sun_by_absmove_q"] = s.groupby("pzq")[["sg24","sg48","sg72","vr"]].agg(["mean","count"]).iloc[:, [0,2,4,6,1]]
    out["sun_by_volratio_q"] = s.groupby("vrq")[["sg24","sg48","sg72","vr"]].mean()
    out["sun_vr_x_move_sign_mean"] = s.groupby(["vrq", s.pz>0])["sg48"].mean().unstack()
    out["sun_by_coin"] = s.groupby("coin")["sg48"].agg(["mean","count"])
    out["sun_by_year"] = s.groupby("year")["sg48"].agg(["mean","count"])
    out["sun_raw_fwd_by_vrq"] = s.groupby("vrq")["f48"].agg(["mean","count"])
    h = pd.concat(hr).dropna()
    hh = h.groupby("hour")["r"].agg(["mean","std","count"]); hh["t"]=hh["mean"]/hh["std"]*np.sqrt(hh["count"])
    out["hour_mean_ret"] = hh[["mean","t"]]
    ww = h.groupby("wd")["r"].agg(["mean","std","count"]); ww["t"]=ww["mean"]/ww["std"]*np.sqrt(ww["count"])
    out["weekday_hourly_mean"] = ww[["mean","t"]]
    return out
