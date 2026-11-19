#!/usr/bin/env bash

set -eu

branch="${VERCEL_GIT_COMMIT_REF:-}"

echo "Branch detectada pela Vercel: $branch"

if [ "$branch" = "main" ] || [ "$branch" = "develop" ]; then
  echo "Branch autorizada para deploy: $branch"
  exit 1
fi

echo "Branch não foi autorizada para deploy: $branch"
exit 0
