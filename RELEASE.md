> The founder must approve this document before publication or use.

# Release process

Nothing in this document has been released, tagged, or pushed. The founder performs and approves each release.

## Before the first release

After the founder gives the word, open the repository on GitHub. Open Settings, choose General, find Change repository visibility, and make the repository public. This is a one-time step. Do not do it before the founder gives the word.

## Cut a release

1. Choose the next version number without a leading `v`.
2. Put that same version in `.claude-plugin/plugin.json` at `version`.
3. Put that same version in `.claude-plugin/marketplace.json` at the listed skill's `version`.
4. Put that same version in `src/skill.md` at `metadata.version` in the frontmatter.
5. Add a dated entry for that version to `CHANGELOG.md`.
6. Run the full repository checks, including `bash tools/release_check.sh`, and review the generated files.
7. Commit the version and changelog changes together.
8. Create the tag `v<version>` from that commit.
9. Push only the tag `v<version>` when the founder approves the release.

The tag starts the release workflow in `.github/workflows/release.yml`. It builds and attaches these three files:

- `dist/recoupr-out-of-network-claims.zip`
- `dist/recoupr-out-of-network-claims/SKILL.md`
- `dist/paste-in-prompt.md`

## Verify the release page

Open the GitHub release page for `v<version>`. Confirm that the page shows the intended tag and commit. Confirm that all three files above appear with their exact names and each download is non-empty. Download the ZIP and compare its SHA-256 with the value printed by `bash tools/release_check.sh` from the tagged commit.

## Submit to the directory

follow the directory's submission form from the founder's account
