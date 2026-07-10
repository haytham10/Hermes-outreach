---
name: git-recovery
description: "Recover dropped stashes, inspect dangling commits, verify merge safety, and perform careful git surgery without data loss."
tags: [git, recovery, debugging, surgery, stash]
---

# Git Recovery & Surgery

Recover lost work, inspect dangling objects, verify merge correctness, and perform careful git operations without losing data.

## When to Use

- A `git stash drop` or `git stash pop` failure lost uncommitted changes
- You need to verify whether a branch was actually merged or just sitting on origin
- A merge or rebase went wrong and you need to inspect the object graph before recovering
- You need to confirm exactly what changed between two states before committing or pushing

## Prerequisites

- Standard git installation
- The repo's object store must not have been garbage collected (`git gc`) since the loss — recovered objects are dangling and will be pruned by `git gc`

## Stash Recovery

### Find a Dropped Stash

`git stash drop` removes the ref from the stash list, but the underlying commit object persists until `git gc` runs. Find it:

```bash
git fsck --unreachable 2>/dev/null | grep commit
```

This prints dangling commit hashes. The stash is always a **merge commit** (two parents: the original HEAD and the index tree). Its message starts with `On <branch>: <stash message>`.

### Identify Which Commit Is the Stash

```bash
# Show summary of changed files
git show --stat <commit-hash>

# Show the full combined diff (what the stash changed)
git show --format="" <commit-hash>

# Compare against first parent (original HEAD at stash time)
git diff <commit-hash>^ <commit-hash>

# Check just specific files
git diff <commit-hash>^ <commit-hash> -- <path/to/file>
```

**PITFALL — `git stash pop` fails when the working tree is dirty.** If you modified a file that the stash also touched, `git stash pop` aborts with `error: Your local changes... would be overwritten by merge`. The stash still exists — this is a conflict, not a loss. Options:
1. `git stash push -m "current work"` first, then pop the recovered stash
2. Read the diff and apply changes to specific files manually
3. `git checkout -b recovery-branch <stash-commit-parent>` and apply the stash there

### Selective Apply of Recovered Changes

When you only want some files from a recovered stash (the rest were already handled differently):

```bash
# View just that file's diff
git diff <commit-hash>^ <commit-hash> -- <path/to/file>

# Then patch manually with the old/new strings against the current file content
# (or use git checkout <stash> -- <path> for wholesale file replacement,
#  but only if you're certain the intermediate commits didn't affect it)
```

## Merge Safety — Verify Before Push

### Check If a Commit Was Actually Merged

```bash
# Is <commit> an ancestor of HEAD? YES = merged, NO = not merged
git merge-base --is-ancestor <commit> HEAD && echo "MERGED" || echo "NOT MERGED"

# Confirm the merge base
git merge-base HEAD <other-branch>
```

### Verify What's Ahead of Origin Before Push

```bash
# Files changed and their sizes
git diff origin/<branch> --stat

# Full diff — confirm only expected changes
git diff origin/<branch>

# Log since the divergence point
git log origin/<branch>..HEAD --oneline
```

### Fast-Forward Merge Pattern

```bash
# Check if it's a fast-forward (no merge commit needed)
git merge-base --is-ancestor HEAD <target-branch>
# Exit 0 = fast-forward possible

# Merge
git merge <target-branch>
# Confirm: `git log --oneline -1` shows the target's tip hash
```

## Discern Merge vs. Fast-Forward in History

A fast-forward makes the branch tip point to the same commit as the merged branch — there's no merge commit. A true merge creates a merge commit with two parents.

```bash
# Check if a specific commit is a merge commit
git cat-file -p <commit> | head -5
# If it has two "parent" lines, it's a merge commit

# View the graph between two references
git log --oneline --graph HEAD <other-ref> | head -20
# A merge shows a fork/join pattern; a fast-forward shows a straight line
```

## Inspecting Dangling Commits

Besides stashes, `git fsck --unreachable` can find:
- Lost commits from a reset (`git reset --hard` before pushing)
- Orphaned commits from a rebase (`git rebase` creates new commits; the old ones dangle)
- Aborted operations that left objects behind

```bash
# List all unreachable objects
git fsck --unreachable 2>/dev/null

# Just commits (the most useful for recovery)
git fsck --unreachable 2>/dev/null | grep commit

# Show one
git show <hash>

# If it's a commit you want back:
git branch recovered-branch <hash>
```

## Pitfalls

- **Don't count on this working after `git gc`.** Once gc prunes the dangling objects, they're unrecoverable via normal git commands.
- **`git fsck` can list hundreds of objects** if gc hasn't run in a while. Pipe to `grep commit` to focus on what matters.
- **A stash merge commit has the **parent** as the original HEAD** — `git diff <hash>^ <hash>` gives you the working tree diff. `git diff <hash>^2 <hash>` gives you the staged (index) diff. The combined diff from `git show --format=""` shows both.
- **Don't `git stash drop` on a stash you might need** until you're sure. If in doubt, `git stash apply` instead of `git stash pop`.