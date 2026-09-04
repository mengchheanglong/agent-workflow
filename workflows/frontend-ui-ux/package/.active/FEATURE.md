# Active Feature

No feature is currently initialized.

To start one:

1. Copy `.agent/templates/FEATURE_TEMPLATE.md` into this file.
2. Fill the change baseline before editing.
3. Synchronize `.active/STATE.md` and `.active/STATE.json`.
4. Run `python .agent/scripts/validate_workflow.py`.

Do not initialize a new feature over a `PAUSED`, `BLOCKED`, or otherwise unfinished feature without a
safe human-directed handoff.
