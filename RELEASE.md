# Release process

Releases are tagged from `main` by a maintainer. The release workflow builds the artifacts and attaches them to the GitHub release.

## Before tagging

1. `python3 tools/build.py`
2. `python3 tools/check_drift.py`
3. `python3 tools/phi_scan.py .`
4. `python3 -m unittest discover -s tests`
5. `bash tools/validate.sh`
6. `bash tools/release_check.sh`
7. Update `CHANGELOG.md` and the version in `src/skill.md`, `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`.

## Tag

```text
git tag -a vX.Y.Z -m "recoupr Out-of-Network Claims vX.Y.Z"
git push origin vX.Y.Z
```

The `release` workflow attaches `recoupr-out-of-network-claims.zip`, `SKILL.md` and `paste-in-prompt.md` to the release. The site's download links always point at the latest release.

## After tagging

Download the ZIP from the release page and confirm it unzips to a single `recoupr-out-of-network-claims` folder with `SKILL.md` at its top level.
