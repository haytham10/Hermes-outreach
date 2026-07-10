---
name: project-bootstrapping
description: "Initialize a git repo for an existing project — pre-init assessment, credential scanning, .gitignore design, path sanitization, and pre-commit verification."
tags: [git, init, bootstrapping, credentials, secrets, .gitignore, security]
---

# Project Bootstrapping — Pre-First-Commit Safety

Initialize a git repo for an existing project without accidentally committing credentials, hardcoded local paths, or sensitive directories.

**Use when:** you're about to `git init` in a directory that already has files — especially config dirs, credential files, or scripts with machine-specific paths.

## 1. Assess What Exists

```bash
# Is this already a repo?
git status 2>/dev/null || echo "Not a repo yet"

# Any remotes?
git remote -v 2>/dev/null || echo "No remotes"

# Full file tree — identify everything that would be staged
ls -laR --ignore=<large-scratch-dir> .

# Check for common credential directories
ls -la .hermes .config/secrets credentials/ .env .env.* 2>/dev/null
```

## 2. Scan for Credentials

Look for live secrets before they can be committed:

```bash
grep -rnE '(sk-[a-zA-Z0-9]{20,}|client_secret|ghp_|gho_|xox[baprs]-|AKIA[0-9A-Z]{16}|eyJ[a-zA-Z0-9_-]+\.eyJ)' \
  --include='*.{json,yaml,yml,toml,ini,env,py,js,ts,sh,bat,md,txt}' \
  . 2>/dev/null | grep -v node_modules | grep -v '\.git/'
```

Focus especially on files named `client_secret*`, `credentials*`, `secrets*`, `*.env`, `*.pem`, `*.key`, `token*`, `auth*`.

## 3. Write the .gitignore (Two-Layer Defense)

**Layer 1 — project-specific exclusions.** Every project that has a config/credential directory should exclude it:

```
.hermes/
cached-evidences/
secrets/
credentials/
config/secrets/
```

**Layer 2 — safety net patterns.** Universal patterns that prevent common slips:

```
# Environment / secrets
.env
.env.local
.env.*.local
*.env
*.pem
*.key
*.cert
*.keystore
*.jks

# OS artifacts
.DS_Store
Thumbs.db
Desktop.ini
*.swp
*.swo
*~

# Editor / agent configs
.vscode/
.idea/
*.sublime-*
.claude/

# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/
*.egg
.venv/
venv/
env/

# Logs / temp
*.log
*.tmp
*.bak
```

## 4. Sanitize Hardcoded Local Paths

Before staging, scan scripts for hardcoded user paths. Common patterns to look for:

| Pattern | Example | Fix |
|---|---|---|
| Windows absolute | `C:\Users\cnara\AppData\...` | `os.environ.get("LOCALAPPDATA")` or `os.environ.get("USERPROFILE")` |
| WSL /mnt/c | `/mnt/c/Users/cnara/...` | Same — use `LOCALAPPDATA` env var (works via WSL) |
| Unix home | `/home/haytham/...` | `os.path.expanduser("~/...")` |
| Signed path | `C:\Users\cnara\projects\...` | Make relative to the project root using `os.path.dirname(__file__)` |

**PITFALL:** The hardcoded path may be in the project's *scripts* that read from the system config (e.g. Hermes `config.yaml`). Don't remove the path entirely — make it portable by reading from an env var with a sensible fallback:

```python
CONFIG_PATH = os.path.join(
    os.environ.get("LOCALAPPDATA", os.path.expanduser("~/.hermes")),
    "hermes",
    "config.yaml",
)
```

## 5. Preserve Config Guidance Before Gitignoring

When you find a config file that contains useful setup information but is too machine-specific to commit (e.g. `.claude/settings.local.json` with permission rules, `.vscode/` with launch configs):

1. **Extract the generalizable guidance** — what would someone cloning this repo need to know? Permission rules, env var requirements, extension recommendations.
2. **Add it to README.md** under a setup/prerequisites section rather than committing the raw config file.
3. **Then add the directory to .gitignore** and unstage any copies already added: `git rm --cached <path>`.

This keeps the repo portable while preserving the institutional knowledge.

## 6. Verify the Staged File List

```bash
# Stage everything
git add --all

# Inspect what's about to be committed
git status
```

**Confirm the following are NOT in the staged list:**
- `.hermes/` or any subdirectory of it
- `cached-evidences/`
- `.claude/`
- `secrets/` or `credentials/`
- `*.env` files
- Any `client_secret*` or `token*` files

If any appear, fix `.gitignore` and re-stage. **Show the `git status` output to the user and let them review before you commit** — they may want to exclude additional files or notice something you missed.

## 7. Pre-Commit Checklist

- [ ] `.gitignore` exists and covers all project-specific sensitive dirs
- [ ] Credential scan returned only false positives or known-safe matches
- [ ] No hardcoded local usernames or machine-specific paths in staged files
- [ ] Dangerous dirs (`.hermes/`, `cached-evidences/`, `secrets/`) absent from `git status`
- [ ] Scripts referencing external config use env vars, not absolute paths
- [ ] Staged file list matches what you intend to push

## 8. Verification

After staging, run a targeted verification script:

```python
#!/usr/bin/env python3
"""Verify no credentials, no hardcoded paths, and correct .gitignore exclusion."""
import ast, os, subprocess

errors = []
working_dir = "."

# 1. Syntax-check any changed .py files
for root, dirs, files in os.walk(working_dir):
    for f in files:
        if f.endswith(".py"):
            path = os.path.join(root, f)
            try:
                with open(path) as fh:
                    ast.parse(fh.read())
            except SyntaxError as e:
                errors.append(f"Syntax error in {path}: {e}")

# 2. Check no hardcoded local usernames in staged scripts
result = subprocess.run(
    ["git", "diff", "--cached", "--name-only"],
    capture_output=True, text=True, cwd=working_dir
)
for staged_file in result.stdout.strip().splitlines():
    if staged_file.endswith(".py"):
        with open(staged_file) as f:
            content = f.read()
        if r"C:\Users\\" in content or "/home/" in content:
            errors.append(f"Hardcoded user path in {staged_file}")

# 3. Confirm dangerous dirs not staged
status = subprocess.run(
    ["git", "status", "--porcelain"],
    capture_output=True, text=True, cwd=working_dir
)
for bad in [".hermes", "cached-evidences", ".env"]:
    if bad in status.stdout:
        errors.append(f"{bad} IS STAGED — .gitignore isn't working")

if errors:
    for e in errors:
        print(f"❌  {e}")
    exit(1)
else:
    print("✅  All checks passed — no secrets staged, no hardcoded paths.")
```

Run with: `python3 <tempfile-path>/hermes-verify-bootstrap.py`

## Pitfalls

- **Don't gitignore `.git/`** — that breaks git itself. The `.git` directory is already not tracked.
- **CRLF warnings on first `git add`** are harmless on Windows — they mean Git will normalize line endings. Not a blocker.
- **`client_secret*` files can hide in unexpected places.** A `desktop-attachments/` subdirectory, `.claude/`, or `.hermes/` folder are common hiding spots. Always recurse and list everything before committing.
- **Set `git config user.name` and `user.email` before the first commit.** Fresh `git init` has no author identity set, and the first commit will fail with `Author identity unknown`. Set repo-local (`--local`, the default) rather than `--global`:

  ```bash
  git config user.email "you@example.com"
  git config user.name "Your Name"
  ```

  Check with `git config user.email` before committing if unsure.
- **A script that reads a token from an external config file is safe** — the actual token isn't in the repo. The hardcoded *path* to that config file is the problem. Replace the path with an env var, not the token itself.
- **Empty directories** (`cached-evidences/` with no files) won't show in `git status` staged list even without .gitignore — but any future file inside them would be tracked. Still gitignore them proactively.