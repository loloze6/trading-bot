# Where the live bot can run when the PC is off: research (2026-11-19)

Research only: nothing bought, no account created, no secret stored, no code of the bot changed.
Criteria, in the operator's order: 1 cost, 2 simplicity, 3 performance, 4 flexibility.

**Words used below.**
- **Server**: a computer that stays on in a data centre. You reach it from your PC over the internet.
- **VPS** (virtual private server): a slice of a big server, rented by the month. It behaves like a small
  computer of your own.
- **Fixed IP**: the server's internet address never changes. Kraken can then be told to accept your key from that
  address only.
- **Service**: a program the server's system starts by itself at boot and restarts after a crash. On Linux the
  part of the system that does this is called systemd.
- **HT / TTC**: price before VAT / with VAT. French VAT is 20%, and a French private customer of an EU host pays
  French VAT.

**How sure each price is.** This session's network blocked most providers' own pages. Every price comes from one
of four places, marked in the tables:
- **[O]**: the provider's own page or blog, read through a search extract;
- **[3]**: a third-party comparison, with its date;
- **[M]**: my own memory, not checked today;
- **[calc]**: my arithmetic.

Dollar prices are converted at about 1 USD = 0.86 EUR, a rate I did not check today. **Before paying, open the
provider's order page once by hand: prices rose several times in 2026.**

---

## 1. What the bot needs (measured)

| Need | Value | Where it comes from |
|---|---|---|
| Memory per live run | **250 MB after loading, 273 MB at peak** | measured today on Linux, Python 3.13: a 912-day warm-up of `first_paper`'s strategy, then 30 simulated days. Offline, on synthetic candles through the parity test's fake Kraken, because this container's network refuses futures.kraken.com |
| Memory, 3 runs at once | about 820 MB, plus about 250–400 MB for the server's own system | 3 × 273 MB [calc] |
| So: server size | **1 GB is too tight for 3 runs; 2 GB is enough; 4 GB leaves room** for more coins and the research viewer | |
| CPU | negligible: warm-up plus 30 days of polls took 6 s | measured |
| Disk | Python libraries 490 MB, the repository clone about 1 GB, a run folder 2.3 MB after 30 days | measured |
| ARM processors (cheaper machines) | fine: every pinned package has a ready-made Python 3.13 ARM file | checked on PyPI today |
| Network | outbound HTTPS to futures.kraken.com only; nothing comes in | `live/kraken.py` |
| Key | read from two environment variables, `KRAKEN_FUTURES_API_KEY` and `KRAKEN_FUTURES_API_SECRET` | `live/kraken.py` |
| Restart of an existing run | `python main.py run_live --run NAME`. It reads the folder's own `strategy_config.json`. **It needs the key**: `start_value` is null, so the local book starts at the real account's value | `live/runner.py` |

**Two facts from the code that matter for any host.**
1. **The bot stops cleanly only on Ctrl+C.** A server stops a program with a different signal (SIGTERM) by default.
   On that signal the bot dies on the spot: `local_book.csv` is not written and no "stop requested" line is
   logged. Tested today: SIGTERM ends the process with code 143 and its `finally` block never runs; SIGINT (what
   Ctrl+C sends) gives "clean stop" and code 0. This is what the three runs show from 2026-11-18. On a server the
   fix is one line in the service file (`KillSignal=SIGINT`, see the setup plan): no code change.
2. **Every restart is a new session**: a new warm-up, and the local book starts again at the real account's value
   (card, "Open"). Automatic restarts after a crash or a reboot will therefore add sessions to a run. That is
   expected, but each one is visible in the record.

---

## 2. Comparison of all options

Cost is per month with VAT unless said otherwise. Simplicity runs from 1 (hard) to 5 (easy) for someone who has
never used a server. "Fit" says whether 3 runs (about 820 MB) fit.

### 2a. Rented small servers (VPS)

| Option | Exact plan | Cost / month | Simp. | Fit (3 runs) | Flexibility | Main risk |
|---|---|---|---|---|---|---|
| **OVHcloud VPS-1** (France) | 2 vCores, 4 GB, 40 GB NVMe, unlimited traffic at 500 Mbit/s, **daily backup and IPv4 included**, 99.9% uptime promise. Datacentres in France | **€4.57** with a 12-month commitment (€3.81 HT); **€5.39** with none (€4.49 HT) [O] OVH blog "VPS 2027" + [3] dev.to, Nov 2026 | 4 | yes, with room | good: bigger plans in one click | OVH raised its previous range by 45% in April 2026 [3] next.ink; the renewal price after the commitment is not known |
| netcup VPS nano G11.5s (Germany) | 2 vCores, 2 GB, 60 GB, IPv4 included | **€3.69** with German VAT, about €3.72 with French VAT [calc]; **6-month contract** [O] netcup.com/en/server/vps-lite (extract) | 3 | yes, without much room | medium | German company, English/German panel; backups: I do not know |
| netcup VPS pico G11.5s | 1 vCore, 1 GB, 30 GB | €2.21 with VAT, 12-month contract [O] same page | 3 | **no** (1 run only) | low | too small for 3 runs |
| IONOS VPS XS (France/Germany) | 1 vCore, 1 GB, 10 GB | €1.20 [calc from €1 HT] **+ €12 setup fee**, probably a long commitment [3] experte.com/whtop 2026 | 3 | **no** | low | promotional price; renewal unclear |
| Contabo Cloud VPS 10 (Germany) | 3 vCPU, 8 GB, 75 GB [M] | €4.40 first term, then €5.50 (VAT unclear) **+ a setup fee of unknown amount** [3] pricingsaas Jun 2026 + [O] Contabo support | 3 | yes | high (8 GB) | many reports of slow, overloaded CPUs and of new servers getting IP addresses blacklisted for earlier abuse (r/VPS 2024–25, many users) |
| Hetzner CX23 (Germany/Finland) | 2 vCPU, 4 GB, 40 GB, 20 TB [M] | **€7.19** [calc: €5.49 + €0.50 IPv4 HT, since 15 June 2026] [3] northflank/bitdoze 2026 | 4 | yes | good | **reported impossible to order on several dates in Sept–Oct 2026** [3] bitdoze; sign-up asks for an ID document plus a selfie, and some sign-ups are refused without reason [O] Hetzner FAQ + many users |
| Vultr Regular (Paris) | 1 vCPU, 1 GB, 25 GB, 1 TB | about €5.2 [calc from $5 + VAT] [3] costbench 2026 | 4 | **no** (2 GB plan needed, price not checked) | good | billed in USD |
| Linode/Akamai Nanode (Paris) | 1 vCPU, 1 GB, 25 GB, 1 TB | about €5.2 [calc from $5] [3] activepieces Nov 2026 | 4 | **no** | good | billed in USD |
| DigitalOcean Basic (Frankfurt/Amsterdam) | 1 vCPU, 1 GB, 25 GB, 1 TB | about €6.2 [calc from $6] [3] costbench Oct 2026; backups +20% [M] | 4 | **no** | good | no Paris datacentre [M] |
| Scaleway DEV1-S (Paris) | 2 vCPU, 2 GB, 20 GB | about €11.5 [calc: €6.55 + about €3 for IPv4, HT] [O] Scaleway pricing blog, June 2026 | 3 | yes | good | **IPv4 billed on top**; the cheap Stardust1-S (1 GB, about €4 with IPv4) is often out of stock [M] |
| Hostinger KVM 1 (Paris) | 1 vCPU, 4 GB, 50 GB | €5.49 only if 24 months are paid upfront, **€11.99 at renewal** [3] ouiheberg 2026 | 4 | yes | medium | renewal price twice the entry price |

### 2b. The big clouds' free or small machines

| Option | What is free, for how long | Cost / month | Simp. | Fit | Main risk |
|---|---|---|---|---|---|
| Oracle Cloud Always Free | ARM machine up to **2 OCPU / 12 GB** (halved from 4/24 on 2026-06-15), no end date; only in the region chosen at sign-up (France has Paris and Marseille [M]) | **€0** | **1–2** (complex console; often "out of capacity") | yes | Oracle **reclaims idle free machines**: under 20% CPU, network and memory over 7 days [O] Oracle docs. This bot is far below all three, so it would be reclaimed unless the account is upgraded to pay-as-you-go (card, billing risk). Many reports of whole accounts closed without warning [many users, 2024–26]. The free allowance was cut without notice in 2026 [3] InfoQ July 2026 |
| AWS Lightsail (Paris region exists [M]) | free plan = $100–200 of credits for 6 months, then the account closes unless upgraded [O] AWS, 2025-07-15 | after credits: about €7.2 for 1 GB (**$7**), about €12.4 for 2 GB ($12), IPv4 included [O] Lightsail docs (extract) | 3 | 2 GB plan | not free for long; English console |
| Google Cloud e2-micro | free with no end date, **in US regions only** (us-west1, us-central1, us-east1) [O] | €0 (a user reports a network charge) | 2 | **no** (1 GB) | **US server: Kraken's EU perpetuals are not offered in the US** (see section 4) |
| Azure free account | B1s 750 h/month for **12 months**, then about $8.7 in France Central [3] | €0, then about €9 | 2 | **no** (1 GB) | ends after 12 months |

### 2c. Managed app platforms (they run the program for you; no server to look after)

| Option | Cost / month for this bot | Simp. | Fit | Main risk |
|---|---|---|---|---|
| Railway Hobby | $5 plan including $5 of usage; RAM $10/GB → **about €11.5–12.5 for 1 GB** [O] docs.railway.com | 4 | yes (1 GB) | fixed outbound IP only on the $20 Pro plan; usage-based bill |
| Fly.io | 1 GB about $6.70 + volume $0.15/GB + IPv4 $3.60 → **about €9–11** [O] fly.io pricing, 2026 | 3 (command line and Docker) | yes | no free allowance for new accounts [3] |
| Render | worker 512 MB **$7 per run**, disk $0.25/GB → 3 runs about €22–23 [O] render.com/pricing | 4 | one run per 512 MB worker | dedicated IP $100/month |
| Northflank | 512 MB about $5.4 → 3 runs need more [O] northflank.com/pricing | 3 | partly | could not verify fixed IP |
| PythonAnywhere | Developer plan €10, **1 always-on task** [O] blog.pythonanywhere.com/222 | 4 | **1 run only** | memory limit of a task: I do not know |
| Heroku, Koyeb | Heroku: files wiped at every restart, maintenance-only since 2026-02 [O]; Koyeb: free tier closed to new users since Feb 2026 [O] | — | — | not suitable |

### 2d. Scheduled jobs instead of an always-on program

| Option | Cost | Verdict |
|---|---|---|
| GitHub Actions on a timer | free within 2,000 min/month on a private repository [O] GitHub docs. One daily run of about 2 min (installing 490 MB of libraries plus the warm-up) is about 60 min a month; hourly is about 1,440 | **Not suitable today.** |
| Google Cloud Run jobs + Scheduler, AWS Lambda + EventBridge | free quotas cover a daily run; Lambda's free quota is about 9 days of continuous 512 MB running [O] | Same rewrite needed. Cloud Run or Lambda add a cloud account and its console to learn. |

Why GitHub Actions is not suitable today:
- **The bot's design does not allow it.** A run keeps its strategy and local book in memory between bars, and
  every stop closes the local position. A timer job would need the strategy's state and the local book saved
  between runs: a code change to the shared bot, which needs the operator's go.
- **Timing.** Scheduled runs are delayed at busy hours, and the top of the hour is the busiest. That goes against
  step 3b, which aims to decide 3 s after the close.
- **No fixed IP.** Runs come from shared US addresses, so the key cannot be locked to one address, and US addresses
  are a risk with Kraken (section 4).
- **Terms of use.** GitHub's terms appear to rule out using Actions for work unrelated to the repository's
  software. I could not read the live text.

### 2e. A device at home

| Option | Cost | Simp. | Fit | Main risk |
|---|---|---|---|---|
| An old laptop you already own | €0 to buy; 15–20 W → **€26–35 a year, €2.2–2.9 a month** at €0.2001/kWh [3] Selectra/hellowatt, EDF Tarif Bleu Base from 2026-08-01 [calc] | 3 | yes | **home power or internet cut = bot stopped**. A laptop can go to sleep: the recorder's notes record a real 4-hour hole caused exactly by that (`deploy/kraken_recorder/install_systemd_unit.sh`). A battery left charging for years may swell |
| Raspberry Pi 5, 4 GB, with power supply, case and small SSD | about **€170–230 once** (board about $110 after the 2026 price rises [3] RPi forum; total is my estimate) + 3.5–5 W → about €6–9 a year | 2 | yes | same home risks. SD cards get corrupted by power cuts, so boot from an SSD [many users]. Raspberry Pi OS Trixie ships Python 3.13 [O]. Over 3 years about €5–7 a month: not cheaper than OVH |
| A NAS you already own (e.g. Synology) | about €26 a year at 14.7 W [O] Synology spec | 3 | depends on its memory | same home risks |

At home the fixed IP depends on the internet provider: I do not know yours. Without a fixed IP, the key cannot be
locked to the bot's address.

### 2f. Not suitable, confirmed

- **A Claude Code cloud session.** Its container is reclaimed after a period of inactivity (this environment's own
  documentation), so the bot would stop and its local files would be lost. Its network is also set per environment:
  **in this session futures.kraken.com was refused** (proxy answer 403), while the operator saw Kraken reachable in
  another environment.
- **Heroku**: files wiped at every restart. **Koyeb**: free tier closed to new users. **Google's free machine**: US
  only, 1 GB.

---

## 3. Recommendation

### Recommended: OVHcloud VPS-1, datacentre in France, Debian 13. €4.57 a month (12 months) or €5.39 (no commitment)

| Criterion | Why |
|---|---|
| 1 Cost | Among the cheapest options that are viable for 3 runs. Only netcup nano (€3.72, 2 GB, Germany, 6-month contract) and an old laptop you already own (about €2.5 of electricity) cost less, and both give up stability or room |
| | **Everything is included**: fixed IPv4, daily automatic backup, unlimited traffic. Hetzner and Scaleway bill the IPv4 apart; DigitalOcean and Vultr bill backups apart |
| 2 Simplicity | French company, French console and support, billed in euros with French VAT |
| | A web console in the browser for when the connection from the PC fails |
| | A standard Debian image that already has Python 3.13 (Debian 13 ships it [O] Debian release notes) |
| 3 Performance | 4 GB for about 820 MB of need; 2 vCores for one decision a day |
| 4 Flexibility | Several runs or coins (one service per run) |
| | The research viewer, reached privately through an SSH tunnel; no port opened |
| | A bigger plan later in one click. Heavy backtests stay on the PC: 2 vCores are not a backtest machine |
| Kraken rules | Server in France, inside the European Economic Area like you, which is what Kraken's EU terms expect |
| | Fixed IPv4, so the key can be locked to it |

What I recommend against, and why:
- **Oracle's free machine.** It is the only €0 option big enough, but this bot is so light that Oracle's idle rule
  would reclaim it. The way around (pay-as-you-go) brings back billing. The console is the hardest of all, and
  accounts have been closed without warning.
- **Hetzner.** It used to be the usual cheap pick. In 2026 it is pricier (€7.19), sign-up is strict, and its cheap
  plans were often not orderable.

### Second choice: netcup VPS nano (Germany), about €3.72 a month, 6-month contract

The cheapest plan with enough memory for 3 runs, IPv4 included, inside the EU. It is behind OVH because:
- 2 GB leaves little room for more coins or the viewer;
- its panel and support are in German/English;
- whether backups are included: I do not know;
- it has a contract term.

### Questions only the operator can answer (each would change the choice)

| Question | If yes | If no |
|---|---|---|
| Do you already own a laptop or NAS you can leave on at home, with a fixed internet address? | It is about €2/month cheaper than OVH. Accept power cuts, internet cuts and sleep as the risks; a Healthchecks alert (below) still warns you | OVH |
| Are you ready to commit 12 months? | €4.57/month | €5.39/month. I do not know whether a running VPS can move to the commitment price later |
| Will you run more than about 5 runs at once, or the research viewer on the server? | OVH VPS-1 (4 GB) | netcup nano (2 GB) is enough |

---

## 4. Kraken Futures from France: what the server's location changes

Kraken's own pages (support.kraken.com, docs.kraken.com) were blocked in this session, so these come from search
extracts and press articles. **Read them once by hand, or ask Kraken support, before real orders (step 5).**

| Question | Finding | How sure |
|---|---|---|
| Who offers the perpetuals to a French resident? | Payward Europe Digital Solutions (CY) Ltd, a Cyprus investment firm (CySEC licence 342/17, EU MiFID II rules). EEA launch 2025-05-20 | press: CoinDesk and Cointelegraph, 2025-05-20 |
| Conditions | identity verification, tax number, retail or professional classification, an appropriateness test; leverage at most 10x for EEA clients (less for some contracts) | Kraken pages "derivatives eligibility requirements (EEA)" and "margin schedule (EEA)" (extracts, undated) |
| Is France excluded? | not in any extract of the restricted list (which names e.g. the UK, Canada, Australia). I did not see the full list, so the answer is "probably not", not "no" | extracts; a third-party site says the list was updated in July 2026 |
| Spot (separate) | Payward Europe Solutions Ltd (Ireland), on the AMF's white list since 2025-07-03 | [O] amf-france.org |
| Does the server's country matter? | Kraken's EU terms expect the client "located in an EEA jurisdiction"; the perpetuals are **not offered to the US**, which has its own Kraken product; its promotion rules treat a VPN as abuse. **A server in France or the EU is the safe case; a US server (Google's free machine, GitHub Actions) is the risky one.** Whether Kraken blocks US addresses on the API: I do not know | extracts and inference; no official statement on servers found |
| Kraken blocking data-centre addresses (like Binance's 451) | no report found for Kraken | none found |
| Can a key be locked to fixed addresses? | **Yes**: the futures API key form takes a list of allowed IPv4/IPv6 addresses; Kraken's docs recommend it and have a call that returns a key's allowed ranges | [O] docs.kraken.com "check v3 API key" + a third-party guide |
| Key access levels | general API: read-only or full; withdrawals: can be "No access" | third-party guide + Kraken help (extract) |
| Request limits | one candle request a minute is far below any limit found (private calls: 500 cost units per 10 s) | [O] docs.kraken.com "futures rate limits" |

---

## 5. Setup plan for OVH VPS-1, step by step, for a first server

**Nothing below has been run on a real server.** The service file is a draft: prove it on the server (step 10)
before trusting it.
- "Type in PowerShell" means on your Windows PC (Start menu → PowerShell).
- "On the server" means in the window that step 4 opens.
- Never paste the Kraken key anywhere except the one file in step 8.

1. **Make a login key on the PC (5 min).** An SSH key is a pair of files that replaces a password. The private
   one stays on your PC; the public one goes to the server.
   - Type in PowerShell: `ssh-keygen -t ed25519`, then press Enter three times.
   - Then type `type $HOME\.ssh\id_ed25519.pub` and copy the single line it shows. That line is the public half;
     it is safe to share.
2. **Order (10 min).** On ovhcloud.com/fr/vps, choose **VPS-1**, then:
   - a datacentre in **France**;
   - the image **Debian 13**;
   - paste the public line from step 1 where it asks for an SSH key;
   - no paid options (the daily backup is included).

   Note the **IPv4 address** shown in the OVH panel, and the user name in the delivery email (for Debian images it
   is usually `debian` [M]).
3. **Connect.** Type in PowerShell `ssh debian@YOUR_IP` and answer `yes` the first time. You are now "on the
   server". To leave, type `exit`.
4. **Mask any sleep.** A server should not sleep, but check once on the server:
   `sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target`.
5. **Update and protect (5 min), on the server:**
   - `sudo apt update && sudo apt full-upgrade -y`
   - `sudo apt install -y git python3-venv unattended-upgrades ufw curl`. Unattended-upgrades installs security
     fixes by itself.
   - `sudo ufw allow OpenSSH && sudo ufw enable`. The firewall now accepts only your logins; the bot needs nothing
     else, since it only calls out.
   - `python3 --version` must say 3.13.
6. **Get the code (10 min).** The server needs read-only access to the repository: a **deploy key**, an SSH key that
   can read this one repository and nothing else.
   - On the server: `ssh-keygen -t ed25519 -f ~/.ssh/github_deploy -N ""` then `cat ~/.ssh/github_deploy.pub`.
   - On GitHub: repository Settings → Deploy keys → Add. Paste the line and leave "Allow write access" unticked.
   - On the server: `GIT_SSH_COMMAND="ssh -i ~/.ssh/github_deploy" git clone --branch live-kraken-futures
     git@github.com:loloze6/trading-bot.git ~/trading-bot`
7. **Install the libraries (5–10 min).**
   - `python3 -m venv ~/venv`
   - `~/venv/bin/pip install -r ~/trading-bot/trading-bot/requirements.txt` (about 490 MB).
   - Check, from `~/trading-bot/trading-bot`: `~/venv/bin/python main.py live_check --symbol BTCUSD`. It must print
     the instrument and recent candles, and "key found: no".
8. **A new Kraken key for the server only (10 min).**
   - In Kraken Pro → Settings → Connections & API → **Futures** API, create a key:
     - general access **read-only**, for now;
     - withdrawals **No access**;
     - allowed IP: **the server's IPv4** from step 2.
   - Keep the PC's key separate, so either one can be deleted alone.
   - On the server, type `sudo mkdir -p /etc/trading-bot && sudo nano /etc/trading-bot/kraken.env` and write two
     lines:

     ```
     KRAKEN_FUTURES_API_KEY=...
     KRAKEN_FUTURES_API_SECRET=...
     ```

     Save with Ctrl+O, Enter, Ctrl+X.
   - Then `sudo chmod 600 /etc/trading-bot/kraken.env`. Only the system can read it now. It is not in git, not on
     your screen again, and the service hands it to the bot at start.
   - OVH's daily backup does contain this file. If the server is ever lost or handed back, delete the key in Kraken.
9. **Phone alerts (10 min).** Both are free:
   - **ntfy**: install the ntfy app on the phone and subscribe to a long, random topic name, e.g. 30 random
     letters. Anyone who knows the name can read the alerts, so treat it like a password. The service file below
     sends a message at every start and every stop: a crash, a reboot, or a stop by hand.
   - **Healthchecks.io**, the free "Hobbyist" plan with 20 checks [O]: it alerts you when the server goes *silent*.
     A message sent by the bot cannot cover a dead server; this can.
     - Create one check per run, with a period of 1 hour and a grace time of 1 hour.
     - Add your phone through its Telegram or email integration.
     - On the server, `crontab -e` and add one line per run:

       ```
       0 * * * * find ~/trading-bot/trading-bot/live_runs/first_paper/summary.md -mmin -1560 | grep -q . && curl -fsS -m 10 https://hc-ping.com/YOUR-CHECK-ID >/dev/null
       ```

       The line pings every hour while `summary.md` is less than 26 h old (it is rewritten after every bar).
       A stale summary or a dead server stops the pings, and Healthchecks warns you within about 2 hours.
10. **The service (15 min).** Type `sudo nano /etc/systemd/system/trading-bot-live@.service` and write:

    ```ini
    [Unit]
    Description=Trading bot live run %i
    After=network-online.target
    Wants=network-online.target
    StartLimitIntervalSec=3600
    StartLimitBurst=5

    [Service]
    User=debian
    WorkingDirectory=/home/debian/trading-bot/trading-bot
    EnvironmentFile=/etc/trading-bot/kraken.env
    ExecStart=/home/debian/venv/bin/python main.py run_live --run %i
    # The bot stops cleanly only on Ctrl+C (SIGINT); the default SIGTERM would skip writing local_book.csv.
    KillSignal=SIGINT
    TimeoutStopSec=60
    Restart=on-failure
    RestartSec=60
    ExecStartPost=-/usr/bin/curl -s -m 10 -d "live run %i started" https://ntfy.sh/YOUR_TOPIC
    ExecStopPost=-/usr/bin/curl -s -m 10 -d "live run %i stopped: ${SERVICE_RESULT} ${EXIT_STATUS}" https://ntfy.sh/YOUR_TOPIC

    [Install]
    WantedBy=multi-user.target
    ```

    How it behaves:
    - `%i` is the run's name.
    - The `-` before `/usr/bin/curl` means a failed alert never fails the run.
    - A crash restarts the run after 60 s, at most 5 times an hour; then it stays stopped and the phone has the
      messages.
    - A reboot starts every enabled run again.

    Then:
    - `sudo systemctl daemon-reload`
    - `sudo systemctl enable --now trading-bot-live@first_paper`, and the same for the other runs.

    **Proof before trusting it:**
    - Read `summary.md` and `run.log` once the next bar is decided.
    - `sudo systemctl stop trading-bot-live@first_paper` must write "stop requested" in `run.log` and an updated
      `local_book.csv`.
    - `sudo reboot` must bring the run back, with a new session folder and two ntfy messages.

    **Never run the same run on the PC and on the server at the same time.**
11. **Everyday use.**
    - Is it running? `systemctl status trading-bot-live@first_paper`
    - The run's own log: `tail -f ~/trading-bot/trading-bot/live_runs/first_paper/run.log` (Ctrl+C leaves the
      display; the bot keeps running)
    - What the system saw: `journalctl -u trading-bot-live@first_paper -n 100`
    - Today's state: `cat .../live_runs/first_paper/summary.md`
12. **Updating the bot.**
    - `cd ~/trading-bot && GIT_SSH_COMMAND="ssh -i ~/.ssh/github_deploy" git pull`
    - If `requirements.txt` changed, rerun the pip line from step 7.
    - Then `sudo systemctl restart trading-bot-live@NAME`. A restart is a new session (warm-up again, local book
      from the account's value), so do it well away from 00:00 UTC.
13. **Keep a copy at home.** The session files (`candles.csv`, books) are not committed, so the server is their only
    home besides OVH's daily backup. Weekly, type in PowerShell:
    `scp -r debian@YOUR_IP:trading-bot/trading-bot/live_runs C:\path\to\copy`.

---

## 6. What other people running small bots report

Weight runs high to low: official doc > maintained community doc > many consistent users > single anecdote >
seller's blog.

| Source, date | What it says | Weight |
|---|---|---|
| freqtrade docs, installation and advanced setup (stable, undated) | Docker is the recommended install; on Raspberry Pi use Docker. The bot can report to systemd so systemd restarts it after a failure. No VPS provider is named | official |
| hummingbot docs, installation (undated) | 4 GB RAM and 1 vCPU per instance; reach it through Tailscale rather than opening a port | official |
| Oracle docs, Always Free resources | idle machines are reclaimed (under 20% CPU, network and memory over 7 days) | official |
| InfoQ, 2026-07; linuxiac | Oracle halved the free ARM allowance without announcement (15 June 2026); machines above the new limit terminated from 18 August 2026 | press, consistent |
| community.oracle.com, r/oraclecloud, 2024–26 | accounts closed without warning and without recovery | many users |
| r/hetzner, LowEndTalk, 2024–26 | new accounts refused or cancelled after ID checks; staff advise not to use a VPN at sign-up | many users |
| r/VPS, Jun 2024 to Jan 2025 | Contabo: CPU "steal" of 20–80% (the host lends your processor to others); a new server suspended because its recycled IP had abuse reports; some long-term users satisfied | many users, mixed |
| Hetzner terms | crypto **mining** is forbidden; nothing about **trading** | official |
| theblock.co, 2022 | Hetzner told a customer that broader crypto activity breached its terms | single, old |
| ccxt blog "How far is your exchange", 2025–26 | Bybit refused data-centre addresses in 4 of 5 samples; Binance refuses most US addresses | community measurement |
| quotaguard blog | Kraken is "less aggressive" on IPs than other exchanges | seller's blog |
| Home Assistant community; Raspberry Pi white paper RP-003610-WP | SD cards corrupt on power cuts; use an SSD and a small backup battery | many users + official |
| GitHub Actions docs | scheduled runs delayed at peak hours; public-repo schedules disabled after 60 days without activity | official |

Hidden costs found:
- IPv4 billed apart: Hetzner €0.50, Scaleway about €3, Fly $3.60.
- Backups billed apart: DigitalOcean and Vultr, about +20%.
- Setup fees: IONOS €10 HT; Contabo, amount unknown.
- Renewal prices: Hostinger €5.49 → €11.99.
- Expiring credits: AWS (6 months), Azure (12 months).
- Price rises in 2026: Hetzner (twice), OVH's previous range (+45%), Scaleway, Contabo, Raspberry Pi (+55%).

Not found:
- I found no host whose written terms ban trading bots, and no verified case of an account suspended for running one.
- r/freqtrade, r/algotrading and Hacker News gave no usable result through search.

---

## 7. What I could not verify ("I do not know")

**Prices**
- **No price was read on a provider's own page**: this session's network blocked them, and all come from search
  extracts or third-party pages.
- OVH: the renewal price after the 12-month commitment, and whether a running VPS can move to it later.
- netcup: whether backups are included. Contabo: the setup fee. Hetzner: whether the cheap plans can be ordered
  today.
- The USD-to-EUR rate.

**Kraken**
- Whether France is absent from the **full** restricted list. Kraken's support pages could not be opened.
- Whether Kraken blocks US or data-centre addresses on the futures API.
- Whether IPv6 works for key restriction.
- Whether the server's country is checked at all.

**Home and monitoring**
- Whether your internet provider gives a fixed address at home.
- Whether Healthchecks.io's free plan sends to ntfy (Telegram and email are listed).

**The server itself**
- The OVH Debian image's default user name. I wrote `debian` from memory.
- The service file and the alerts **have not been run** on any server.
- The memory figure comes from Linux in this container with synthetic candles. It has not been measured on the VPS.

## Sources (read through search extracts on 2026-11-19 unless stated)

**OVH**
- blog.ovhcloud.com/vps-2027-fr/
- dev.to/neurau_tech/vps-pas-cher-en-novembre-2026-8-hebergeurs-compares-au-prix-officiel-25k6
- next.ink/225720/ovhcloud-augmente-fortement-le-prix-de-ses-vps-2026-et-ipv4/

**netcup**: netcup.com/en/server/vps-lite

**Hetzner**
- northflank.com/blog/hetzner-cloud-server-price-increases
- bitdoze.com/hetzner-cloud-cost-optimized-plans/
- findstack.com/resources/hetzner-price-increase-2026
- docs.hetzner.com/general/security-and-identify/fraud-prevention-faq/
- hetzner.com/legal/terms-and-conditions/

**Scaleway**: scaleway.com/en/blog/a-transparent-update-on-scaleway-pricing/

**Contabo**
- pricingsaas.com/companies/contabo.main/diffs/2026W25
- contabo.freshdesk.com/en/support/solutions/articles/103000398194

**IONOS**
- experte.com/fr/serveur/vps-pas-chers
- whtop.com/plans/ionos.fr/140732

**Vultr, DigitalOcean, Linode**
- costbench.com/software/cloud-infrastructure/vultr/
- activepieces.com/blog/digitalocean-pricing-plans-and-real-costs-in-2026.md
- activepieces.com/blog/linode-pricing-plans-costs-and-extra-fees-2026.md

**Hostinger**: ouiheberg.com/fr/comparatifs/meilleur-vps-france-2026

**Oracle**
- docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
- infoq.com/news/2026/07/oracle-cloud-free-tier-limits/
- linuxiac.com/oracle-quietly-cuts-free-tier-ampere-a1-resources-in-half/

**AWS**
- aws.amazon.com/about-aws/whats-new/2025/07/aws-free-tier-credits-month-free-plan
- docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-bundles.md

**Google Cloud**
- cloud.google.com/free/docs/compute-getting-started
- cloud.google.com/run/pricing

**Azure**
- azure.microsoft.com/en-us/free/virtual-machines
- costcalc.cloudoptimo.com/azure-pricing-calculator/vm/Standard-B1s

**Managed platforms**
- fly.io/docs/about/pricing/
- docs.railway.com/pricing/plans
- render.com/pricing
- northflank.com/pricing
- blog.pythonanywhere.com/222/
- techzine.eu/news/infrastructure/138611/salesforce-puts-heroku-development-on-hold/
- koyeb.com/blog/koyeb-is-joining-mistral-ai-to-build-the-future-of-ai-infrastructure

**GitHub Actions**
- docs.github.com/en/billing/concepts/product-billing/github-actions
- docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features

**Kraken**
- coindesk.com/business/2025/05/20/kraken-rolls-out-regulated-crypto-derivatives-in-europe
- support.kraken.com/articles/derivatives-eligibility-requirements-eea
- support.kraken.com/articles/360023786632-kraken-derivatives-eligibility
- amf-france.org/en/warnings/white-lists/daspcasp/payward-europe-solutions-limited-kraken-digital-asset-exchange-kraken
- docs.kraken.com/api-reference/api-keys/check-v3-api-key
- docs.kraken.com/api/docs/guides/futures-rate-limits

**Monitoring**
- healthchecks.io/pricing/
- docs.ntfy.sh/publish/
- pushover.net/pricing

**Home device and electricity**
- raspberrypi.com/news/price-increases-for-2gb-raspberry-pi-4-and-raspberry-pi-5/
- jeffgeerling.com/blog/2024/new-2gb-pi-5-has-33-smaller-die-30-idle-power-savings/
- raspberrypi.com/news/trixie-the-new-version-of-raspberry-pi-os/
- Selectra/hellowatt summaries of the CRE decision of 2026-07-15 (EDF Tarif Bleu)
- synology.com/en-us/products/DS224+?tab=specs

**Community**
- freqtrade.io/en/stable/installation and /advanced-setup/
- hummingbot.org/client/installation/
- docs.ccxt.com/blog/how-far-is-your-exchange
- quotaguard.com/blog/static-ip-crypto-trading-bot-binance-okx-bybit-kraken
