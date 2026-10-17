---
name: go
description: "Review, commit, and push eligible workspace changes to the configured Git remote without asking for its URL."
argument-hint: "Optional commit message"
agent: agent
---

Push the latest eligible changes from the current Git repository. Invocation of `/go` authorizes you to commit and push; do not ask for the GitHub URL.

1. Verify the repository root, current branch, configured `origin`, and upstream. Never assume or change the remote URL.
2. Review `git status`, tracked diffs, and untracked files before staging. Use the current branch and its upstream; if no upstream exists, use `git push -u origin HEAD`.
3. Do not stage secrets or local credentials, including `.env*`, `auth.json`, `**/login.json`, private keys, tokens, or credential files. Do not stage generated output such as `reports/`, `tta-report/`, `test-results/`, `playwright-report/`, `allure-results/`, `allure-report/`, `node_modules/`, `.venv/`, `dist/`, or `build/`.
4. Never force-add ignored files. If ignored source changes appear relevant, leave them out and report their paths so they can be reviewed separately.
5. Stage only reviewed, eligible changes. Run `git diff --cached --check` and inspect the staged path list and diff. If anything looks sensitive or unrelated, unstage that path before continuing.
6. If there are no eligible staged changes, stop without creating an empty commit.
7. Commit with the provided argument when present; otherwise derive a concise message from the staged changes.
8. Push with `git push` and verify the resulting commit and branch status. Never force-push, reset, clean, or alter the remote.

Report the commit hash, pushed branch, excluded paths, and any validation limitations.
