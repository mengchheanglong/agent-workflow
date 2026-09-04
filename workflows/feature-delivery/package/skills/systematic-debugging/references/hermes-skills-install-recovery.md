# Hermes Skills Install — Failure Diagnosis

## Symptom
`hermes skills install official/<category>/<skill>` fails with:
```
Fetching: official/<category>/<skill>
Error: Could not fetch '<identifier>' from any source.
```

Yet `hermes skills search <skill>` finds it.

## Root Cause

The `OfficialSkillSource` in Hermes reads from the `optional-skills/` directory shipped with the Hermes install. If the skill isn't in that directory (e.g., it was added to the registry after your Hermes version was released), the search still finds it via the centralized index or other sources, but the install fails because the filesystem path doesn't exist.

## Recovery Options

1. **Update Hermes first:** `hermes update` — pulls the latest code including new optional skills
2. **Direct URL install:** `hermes skills install https://raw.githubusercontent.com/.../SKILL.md` — bypasses the registry entirely
3. **Manual copy:** Download the skill directory from upstream and place it in `~/.hermes/skills/<category>/<skill>/`

## Prevention

Before trying to install a registry-referenced skill, check if your Hermes version ships it:

```bash
hermes --version
ls ~/AppData/Local/hermes/hermes-agent/optional-skills/<category>/
```

If the skill isn't there and search still finds it, you're behind the latest release.