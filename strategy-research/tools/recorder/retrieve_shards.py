"""
Shard retrieval — pull the capture host's data to the analysis host
(dispatch W15 step 4).
=====================================================================

    python -m recorder.retrieve_shards pull \
        --host kraken-vps --remote-out /data/kraken_ws_v2 \
        --local-out trading-bot/local_data/recorded_reserved/kraken_ws_v2 \
        [--identity ~/.ssh/kraken_vps]

    python -m recorder.retrieve_shards prune --yes-delete-confirmed-only \
        --host kraken-vps --remote-out /data/kraken_ws_v2 \
        --local-out trading-bot/local_data/recorded_reserved/kraken_ws_v2

WHY THIS EXISTS
----------------
Analysis (whale_persistence, whale_report, prescreen) runs on the local
machine; once the recorder moves to a server (W15), the data has to get
back here. A forward recording has no upstream to re-fetch from if a
transfer drops or corrupts a shard, so the three properties in the dispatch
are not optional:

  INCREMENTAL   — never re-pull a file already confirmed received; only new
                  or previously-failed shards, and only the unconfirmed tail
                  of the ever-growing coverage journal.
  RESUMABLE     — a killed/interrupted run leaves the local ledger showing
                  exactly what was and wasn't confirmed; rerunning `pull`
                  picks up from there with no operator bookkeeping.
  INTEGRITY-VERIFIED — verified against a hash computed ON THE CAPTURE HOST
                  (`retrieval_manifest.py`, run over SSH), not merely
                  "the transfer protocol didn't complain" and not a hash
                  this process computed by reading the remote file itself
                  (which would let a transport defect corrupt the very
                  check meant to catch it).

THE LEDGER IS THE SAFETY INTERLOCK
------------------------------------
`_retrieval_ledger.json` at the root of `--local-out` records, per relative
path, the sha256 this process independently verified after pulling, and
when. It is the ONLY thing `prune` trusts, and even then `prune` re-fetches
a fresh manifest and re-hashes the local file before deleting anything
remote — see `prune_confirmed`. `pull` never deletes anything, on either
side, ever. This mirrors `compaction.py`'s ordering discipline (verify
before delete, never the other way) one hop further down the pipeline.

TRANSPORT IS INJECTABLE
-------------------------
`SshRsyncTransport` is the real one (ssh for the manifest, rsync for the
bytes). `LocalDirTransport` treats another local directory as "remote" and
exists so this module is testable without a network, an SSH host, or rsync
installed on the test runner — see tests/test_retrieve_shards.py. It is also
a legitimate transport in its own right for a mounted network drive or a
same-host dry run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol

if __package__ in (None, ""):  # allow direct execution
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from recorder.retrieval_manifest import (  # type: ignore
        sha256_of_file,
        sha256_of_prefix,
    )
else:
    from .retrieval_manifest import sha256_of_file, sha256_of_prefix

LEDGER_FILENAME = "_retrieval_ledger.json"


# ---------------------------------------------------------------------------
# Transports
# ---------------------------------------------------------------------------


class Transport(Protocol):
    def fetch_manifest(self) -> Dict[str, Dict[str, Any]]: ...
    def pull(self, relative_path: str, dest: Path) -> None: ...
    def delete(self, relative_path: str) -> None: ...


class TransportError(RuntimeError):
    """A remote command (manifest fetch, pull, or delete) failed."""


class SshRsyncTransport:
    """
    Manifest over `ssh host python3 -m recorder.retrieval_manifest`, bytes
    over `rsync -e ssh`. Both binaries must be on the analysis host's PATH;
    Linux and macOS ship both, and Windows needs rsync from Git-for-Windows,
    Cygwin, or WSL — this is called out in RUNBOOK.md rather than assumed.
    """

    def __init__(
        self,
        host: str,
        remote_out: str,
        identity: Optional[str] = None,
        ssh_bin: str = "ssh",
        rsync_bin: str = "rsync",
        remote_python: str = "python3",
        remote_module_root: Optional[str] = None,
    ):
        self.host = host
        self.remote_out = remote_out.rstrip("/")
        self.identity = identity
        self.ssh_bin = ssh_bin
        self.rsync_bin = rsync_bin
        self.remote_python = remote_python
        # Directory on the remote host containing the `recorder` package,
        # i.e. its strategy-research/. Defaults to the same relative layout
        # as this repo; override if the remote install path differs.
        self.remote_module_root = remote_module_root

    def _ssh_prefix(self) -> List[str]:
        cmd = [self.ssh_bin]
        if self.identity:
            cmd += ["-i", self.identity]
        cmd.append(self.host)
        return cmd

    def fetch_manifest(self) -> Dict[str, Dict[str, Any]]:
        remote_cmd = f"{self.remote_python} -m recorder.retrieval_manifest --out {self.remote_out!r}"
        if self.remote_module_root:
            remote_cmd = f"cd {self.remote_module_root!r} && {remote_cmd}"
        proc = subprocess.run(
            self._ssh_prefix() + [remote_cmd],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            raise TransportError(
                f"manifest fetch failed (exit {proc.returncode}): {proc.stderr}"
            )
        try:
            return json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            raise TransportError(
                f"manifest fetch returned non-JSON stdout: {proc.stdout[:500]!r}"
            ) from exc

    def pull(self, relative_path: str, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        remote_spec = f"{self.host}:{self.remote_out}/{relative_path}"
        cmd = [self.rsync_bin, "-az", "--checksum"]
        if self.identity:
            cmd += ["-e", f"{self.ssh_bin} -i {self.identity}"]
        cmd += [remote_spec, str(dest)]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            raise TransportError(
                f"rsync pull of {relative_path!r} failed (exit {proc.returncode}): {proc.stderr}"
            )

    def delete(self, relative_path: str) -> None:
        remote_cmd = f"rm -f {self.remote_out}/{relative_path}"
        proc = subprocess.run(
            self._ssh_prefix() + [remote_cmd],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            raise TransportError(
                f"remote delete of {relative_path!r} failed (exit {proc.returncode}): {proc.stderr}"
            )


class LocalDirTransport:
    """
    Treats another local directory as "remote". Used by tests, and usable
    for real against a mounted network share or a same-host smoke test.
    """

    def __init__(self, remote_dir: Path):
        self.remote_dir = Path(remote_dir)

    def fetch_manifest(self) -> Dict[str, Dict[str, Any]]:
        if __package__ in (None, ""):
            from recorder.retrieval_manifest import build_manifest  # type: ignore
        else:
            from .retrieval_manifest import build_manifest
        return build_manifest(self.remote_dir)

    def pull(self, relative_path: str, dest: Path) -> None:
        src = self.remote_dir / relative_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)

    def delete(self, relative_path: str) -> None:
        (self.remote_dir / relative_path).unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Ledger
# ---------------------------------------------------------------------------


def load_ledger(local_out: Path) -> Dict[str, Dict[str, Any]]:
    path = Path(local_out) / LEDGER_FILENAME
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_ledger(local_out: Path, ledger: Dict[str, Dict[str, Any]]) -> None:
    path = Path(local_out) / LEDGER_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(ledger, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(path)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Pull
# ---------------------------------------------------------------------------


@dataclass
class RetrievalResult:
    pulled: List[str] = field(default_factory=list)
    verified: List[str] = field(default_factory=list)
    failed: List[str] = field(default_factory=list)
    already_confirmed: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failed


def _verify_local(dest: Path, entry: Dict[str, Any]) -> str:
    """Returns the locally-computed hash used for comparison against `entry`."""
    if entry.get("prefix"):
        return sha256_of_prefix(dest, entry["bytes"])
    return sha256_of_file(dest)


def pull(transport: Transport, local_out: Path) -> RetrievalResult:
    """
    Fetch the remote manifest, pull anything not already confirmed at the
    manifest's hash, verify each pull against the manifest independently,
    and update the ledger only for what verified. Never deletes anything.
    """
    local_out = Path(local_out)
    manifest = transport.fetch_manifest()
    ledger = load_ledger(local_out)
    result = RetrievalResult()

    for rel_path, entry in sorted(manifest.items()):
        confirmed = ledger.get(rel_path)
        if (
            confirmed
            and confirmed.get("sha256") == entry["sha256"]
            and confirmed.get("bytes") == entry.get("bytes")
        ):
            result.already_confirmed.append(rel_path)
            continue

        dest = local_out / rel_path
        transport.pull(rel_path, dest)
        result.pulled.append(rel_path)

        try:
            got = _verify_local(dest, entry)
        except (OSError, ValueError):
            got = None

        if got != entry["sha256"]:
            result.failed.append(rel_path)
            continue

        result.verified.append(rel_path)
        ledger[rel_path] = {
            "sha256": entry["sha256"],
            "bytes": entry["bytes"],
            "prefix": entry.get("prefix", False),
            "confirmed_at": _now_iso(),
        }

    save_ledger(local_out, ledger)
    return result


# ---------------------------------------------------------------------------
# Prune — separate, explicit, re-verified at the instant of deletion
# ---------------------------------------------------------------------------


@dataclass
class PruneResult:
    deleted: List[str] = field(default_factory=list)
    skipped_not_confirmed: List[str] = field(default_factory=list)
    skipped_changed_since_confirmation: List[str] = field(default_factory=list)
    skipped_local_mismatch: List[str] = field(default_factory=list)


def prune_confirmed(transport: Transport, local_out: Path) -> PruneResult:
    """
    Delete remote copies of files this ledger has confirmed received —
    NEVER a file the ledger has not confirmed, and never on the ledger's
    say-so alone: a fresh remote manifest is fetched here and compared
    against both the ledger AND the local file's hash right now, so a
    remote file that changed (should not happen for an already-compacted
    shard, but this is the check that would catch it if it somehow did) is
    left alone rather than deleted. Only the coverage journal is expected to
    legitimately grow past its ledger entry between `pull` and `prune`; that
    file's prefix is excluded from deletion entirely — see below.
    """
    local_out = Path(local_out)
    ledger = load_ledger(local_out)
    manifest = transport.fetch_manifest()
    result = PruneResult()

    for rel_path, remote_entry in sorted(manifest.items()):
        if remote_entry.get("prefix"):
            # The coverage journal is never deleted server-side by this tool
            # — it is small, still growing, and the whole point of retrieval
            # is to have it; there is no storage pressure it relieves.
            continue

        confirmed = ledger.get(rel_path)
        if not confirmed:
            result.skipped_not_confirmed.append(rel_path)
            continue

        if confirmed.get("sha256") != remote_entry["sha256"]:
            result.skipped_changed_since_confirmation.append(rel_path)
            continue

        dest = local_out / rel_path
        if not dest.exists():
            result.skipped_local_mismatch.append(rel_path)
            continue
        try:
            local_hash = sha256_of_file(dest)
        except OSError:
            result.skipped_local_mismatch.append(rel_path)
            continue
        if local_hash != remote_entry["sha256"]:
            result.skipped_local_mismatch.append(rel_path)
            continue

        transport.delete(rel_path)
        result.deleted.append(rel_path)

    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_transport(args: argparse.Namespace) -> Transport:
    if args.local_source:
        return LocalDirTransport(Path(args.local_source))
    if not args.host or not args.remote_out:
        raise SystemExit(
            "--host and --remote-out are required (or use --local-source for testing)"
        )
    return SshRsyncTransport(
        host=args.host,
        remote_out=args.remote_out,
        identity=args.identity,
        remote_python=args.remote_python,
        remote_module_root=args.remote_module_root,
    )


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Retrieve recorder shards from a capture host (W15 step 4)"
    )
    sub = ap.add_subparsers(dest="mode", required=True)

    def common(p):
        p.add_argument("--host")
        p.add_argument("--remote-out")
        p.add_argument("--identity")
        p.add_argument("--remote-python", default="python3")
        p.add_argument("--remote-module-root", default=None)
        p.add_argument("--local-out", required=True)
        p.add_argument(
            "--local-source",
            default=None,
            help="testing/mounted-drive only: treat this local directory as remote, bypassing SSH/rsync",
        )

    p_pull = sub.add_parser(
        "pull", help="incrementally pull and verify new/unconfirmed files"
    )
    common(p_pull)

    p_prune = sub.add_parser(
        "prune", help="delete remote copies already confirmed received"
    )
    common(p_prune)
    p_prune.add_argument(
        "--yes-delete-confirmed-only",
        action="store_true",
        help="required: acknowledges this deletes remote files (only ones re-verified as confirmed)",
    )

    args = ap.parse_args(argv)
    transport = _build_transport(args)

    if args.mode == "pull":
        result = pull(transport, Path(args.local_out))
        print(
            f"pulled {len(result.pulled)}, verified {len(result.verified)}, "
            f"failed {len(result.failed)}, already-confirmed {len(result.already_confirmed)}"
        )
        if result.failed:
            print("FAILED (not added to ledger, will retry next run):")
            for rel in result.failed:
                print(f"  {rel}")
        return 0 if result.ok else 1

    if args.mode == "prune":
        if not args.yes_delete_confirmed_only:
            print(
                "refusing to prune without --yes-delete-confirmed-only", file=sys.stderr
            )
            return 2
        result = prune_confirmed(transport, Path(args.local_out))
        print(
            f"deleted {len(result.deleted)}, "
            f"skipped (not confirmed) {len(result.skipped_not_confirmed)}, "
            f"skipped (changed since confirmation) {len(result.skipped_changed_since_confirmation)}, "
            f"skipped (local mismatch) {len(result.skipped_local_mismatch)}"
        )
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
