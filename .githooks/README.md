# .githooks

Repo hooks. Enable once per clone:

```sh
git config core.hooksPath .githooks
```

`pre-commit` runs the token-size gate: any *staged* file above
5 000 tokens (20 000 B) is refused with a split plan. Escape hatches:
`git commit --no-verify` (one commit) or a reviewed glob in
`.token-gate-ignore`. Uninstall: delete the managed block in
`pre-commit` and `.githooks/token_size_gate.py`.
