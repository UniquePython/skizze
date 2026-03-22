# Skizze Changelogs

## v0.1.0 -> v0.1.1
### Dated: 3rd March, 2026

- Fixed broken import in `__main__.py` (`skizze_cli` → `skizze.skizze_cli`)

- Fixed closure bug where `SkizzeFnNode` was mutated at runtime to store `closure_env`, causing incorrect behavior when functions are defined multiple times or in nested scopes. Functions are now wrapped in a `SkizzeFnValue` runtime object that is separate from the AST node.

- `if`/`else` and `while` now return their evaluated value instead of discarding it