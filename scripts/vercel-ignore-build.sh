#!/usr/bin/env bash

set -eu

branch="${VERCEL_GIT_COMMIT_REF:-}"

if [ "$branch" = "main" ] || [ "$branch" = "develop" ]; then
  echo "Branch autorizada para deploy: $branch"
  exit 1
fi

echo "Branch não autorizada para deploy: $branch"
exit 0
