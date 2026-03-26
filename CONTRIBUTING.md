# Contributing Guide

Thank you for your interest in contributing to this project!
This repository contains a **Streamlit-based communication system visualization app**.
Contributions should improve correctness, clarity, performance, or educational value.

---

## Contribution Workflow

### 1. Raise an Issue

Before writing any code:

- Open a GitHub Issue
- Clearly describe the bug, feature, or improvement
- Add screenshots, references, or examples if relevant
- Suggest a possible technical approach (optional but recommended)

**Direct PRs without an issue are not accepted** (except trivial fixes like typos or docs formatting).

---

### 2. Get the Issue Claimed

- Comment on the issue to request assignment
- Maintainer will assign the issue
- Only one contributor per issue (to prevent duplicate work)

---

### 3. Create a Branch in your Fork

Create a new branch from `main`:

Always keep updating your main branch from upstream fork.

```bash
git checkout -b feature/issue-<id>-short-name
git checkout -b fix/issue-<id>-short-name
```

Example:

```bash
git checkout -b feature/issue-12-qpsk-visualization
```

---

### 4. Develop Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

Follow existing project structure and coding style.
Keep changes minimal and scoped to the issue.

---

### 5. Create a Pull Request (PR)

When ready:

- Push your branch
- Open a PR to `main`
- Reference the issue number in the PR title or description

Example:

```
Fix: QPSK constellation scaling (#12)
```

---

## Contribution Rules

- One issue → one PR
- No unrelated changes in the same PR
- Code must run locally without errors
- Visualizations must be technically correct
- No broken UI flows

---

## What You Can Contribute

- New Features visualizations
- Notes in Existing Modules
- UI/UX improvements
- Performance optimizations
- Documentation
- Educational explanations

---

## Code Quality Standards

- Clear variable naming
- Modular functions
- No hardcoded constants without explanation
- Reusable components
- No dead code

---

## Maintainer Rights

Maintainers may:

- Reject low-quality PRs
- Request changes
- Close inactive issues
- Reassign abandoned issues

---

## Philosophy

This project prioritizes:

- Technical correctness
- Educational value
- Clean architecture
- Simplicity over complexity

If it doesn’t improve learning, correctness, or usability — it doesn’t belong here.

---

**Thank you for contributing to open communication systems education.**
