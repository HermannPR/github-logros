# github-logros

Script to unlock, quickly and within the rules, the GitHub achievements that one account can earn on its own repository.

| Achievement | How you earn it | Here |
|---|---|---|
| **Quickdraw** | Close an issue or PR within 5 minutes of opening it | `python logros.py quickdraw` |
| **YOLO** | Merge a PR without a review | `python logros.py yolo` |
| **Pull Shark** | Merged PRs: 2 (bronze), 16 (silver), 128 (gold), 1024 | `python logros.py pullshark --n 16` |
| **Pair Extraordinaire** | Merged PR with a co-authored commit (`Co-authored-by:`) | `python logros.py pair --coautor "Name <email>"` |
| **Galaxy Brain** | 2 / 8 / 16 / 32 answers marked as accepted in Discussions | Needs other people: answer real questions in projects you use |
| **Starstruck** | A repo of yours reaches 16 / 128 / 512 / 4096 stars | Needs other people: publish something useful |
| **Public Sponsor** | Sponsor someone through GitHub Sponsors | Costs money (from $1 a month) |
| **Heart On Your Sleeve**, **Open Sourcerer** | Reactions, and PRs merged into several public repos | Contribute to other projects |

Retired, no longer earnable: Arctic Code Vault Contributor, Mars 2020 Contributor.

## Use
1. Needs the GitHub CLI logged in (`gh auth status`) and Python 3.
2. `python logros.py todo` gives Quickdraw, YOLO and Pull Shark silver (16 PRs) in a few minutes.
3. For Pair Extraordinaire, the co-author must be another real GitHub account that agrees to it; use its email or its `noreply`.

Achievements can take minutes to a few hours to show on the profile.

## Note
Do not create fake accounts to give yourself stars or accepted answers: it breaks GitHub's terms and can get the account suspended. Keep Pull Shark to reasonable numbers (16, or 128 at most); a thousand automatic PRs looks like spam.
