# Research & Engineering Ledger — index

**Split 2026-08-16.** Two people (Jeremy on master, Dorian on the Mac fork) were both appending session entries to this single file on every sync, producing a merge conflict almost every time. Dorian proposed splitting into one file per writer plus this shared index, so syncs are trivially disjoint. Adopted.

- **[`ledger/win.md`](ledger/win.md)** — Jeremy's session log (Windows). All entries before the split live here (the file is the renamed original `LEDGER.md`, history preserved via `git mv`).
- **[`ledger/mac.md`](ledger/mac.md)** — Dorian's session log (Mac fork).

## How to use this (both writers)

- **Start of session:** `git status && git log --oneline -5`, then read **both** `ledger/win.md` and `ledger/mac.md` — the other writer's recent entries are often exactly the context you need (a kill, a bug, a landed fix).
- **End of session:** append 2-5 lines to **your own** file only (`win.md` if you're Jeremy, `mac.md` if you're Dorian). Never edit the other writer's file. Never end a work session without it.
- This index itself should rarely change — only when the split structure changes again.
