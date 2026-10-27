#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$repo_root"

claude plugin validate --strict --profile directory .
claude plugin validate --strict dist/recoupr-out-of-network-claims
