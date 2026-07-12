import subprocess
from functools import lru_cache
import re

def git(cmd):
    return subprocess.check_output(
        cmd, stderr=subprocess.DEVNULL
    ).decode().strip()

@lru_cache(maxsize=1)
def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
    except Exception:
        return "UNKNOWN"

@lru_cache(maxsize=1)
def git_version() -> str:
    try:
        return subprocess.check_output(
            ["git", "describe", "--tags", "--exact-match"],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
    except Exception:
        return f"{git_commit()}"

@lru_cache(maxsize=1)
def commit_date_str() -> str:
    try:
        return git(["git", "show", "-s", "--format=%cd", "HEAD"])
    except Exception:
        return "unknown"

SEMVER_RE = re.compile(r"^v?\d+(\.\d+)+$")

def isstable(tag: str) -> bool:
    return bool(SEMVER_RE.match(tag))

ICY_VERSION = git_version()
ICY_COMMIT_DATE = commit_date_str()

def icyversion():
    return ICY_VERSION

def icycommitdate():
    return ICY_COMMIT_DATE