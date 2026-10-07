"""Earn the GitHub achievements that a single account can legitimately unlock on its own repository.

Usage (from this folder, with the GitHub CLI logged in):
    python logros.py quickdraw            # Quickdraw: open an issue and close it within 5 minutes
    python logros.py yolo                 # YOLO: merge a pull request without a review
    python logros.py pullshark --n 16     # Pull Shark: N merged pull requests (tiers at 2, 16, 128, 1024)
    python logros.py pair --coautor "Name <id+login@users.noreply.github.com>"
                                          # Pair Extraordinaire: merged PR with a co-authored commit
    python logros.py todo                 # quickdraw + yolo + pullshark (16)

Each step works on throwaway branches of THIS repo and leaves a line in registro.md.
Achievements that need other people (Starstruck, Galaxy Brain) or money (Public Sponsor) are explained in README.md.
"""
import argparse
import datetime as dt
import subprocess
import sys
import time

GH = "gh"


def run(*cmd, check=True):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if check and r.returncode != 0:
        sys.exit(f"fallo: {' '.join(cmd)}\n{r.stderr.strip()}")
    return r.stdout.strip()


def registrar(texto):
    with open("registro.md", "a", encoding="utf-8") as f:
        f.write(f"- {dt.datetime.now():%Y-%m-%d %H:%M} {texto}\n")


def rama_por_defecto():
    return run(GH, "repo", "view", "--json", "defaultBranchRef", "--jq", ".defaultBranchRef.name")


def pr_mergeado(titulo, cuerpo, coautor=None):
    """Branch -> commit -> push -> PR -> merge without review -> delete branch. Returns the PR URL."""
    base = rama_por_defecto()
    run("git", "checkout", "-q", base)
    run("git", "pull", "-q", "--ff-only")
    rama = f"logro-{int(time.time() * 1000)}"
    run("git", "checkout", "-q", "-b", rama)
    registrar(titulo)
    msg = titulo + (f"\n\nCo-authored-by: {coautor}" if coautor else "")
    run("git", "commit", "-q", "-am", msg)
    run("git", "push", "-q", "-u", "origin", rama)
    url = run(GH, "pr", "create", "--base", base, "--head", rama, "--title", titulo, "--body", cuerpo)
    run(GH, "pr", "merge", url, "--squash" if not coautor else "--merge", "--delete-branch")
    run("git", "checkout", "-q", base)
    run("git", "pull", "-q", "--ff-only")
    run("git", "branch", "-q", "-D", rama, check=False)
    return url


def quickdraw():
    url = run(GH, "issue", "create", "--title", "Quickdraw", "--body", "Se cierra en menos de 5 minutos.")
    run(GH, "issue", "close", url)
    print("Quickdraw:", url)


def yolo():
    print("YOLO:", pr_mergeado("YOLO: merge sin revision", "Merge sin pedir revision."))


def pullshark(n):
    for i in range(1, n + 1):
        url = pr_mergeado(f"Pull Shark {i}/{n}", "PR mergeado para Pull Shark.")
        print(f"Pull Shark {i}/{n}:", url)
        time.sleep(2)  # be gentle with the API


def pair(coautor):
    if "<" not in coautor or "@" not in coautor:
        sys.exit('El coautor va como "Nombre <correo>", con el correo de SU cuenta de GitHub (o su noreply).')
    print("Pair Extraordinaire:", pr_mergeado("Pair Extraordinaire", "Commit en pareja.", coautor))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logro", choices=["quickdraw", "yolo", "pullshark", "pair", "todo"])
    ap.add_argument("--n", type=int, default=16)
    ap.add_argument("--coautor")
    a = ap.parse_args()
    if a.logro in ("quickdraw", "todo"):
        quickdraw()
    if a.logro in ("yolo", "todo"):
        yolo()
    if a.logro in ("pullshark", "todo"):
        pullshark(a.n)
    if a.logro == "pair":
        pair(a.coautor or "")


if __name__ == "__main__":
    main()
