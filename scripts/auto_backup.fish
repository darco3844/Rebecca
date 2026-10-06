#!/usr/bin/env fish

cd ~/Rebecca

set changes (git status --porcelain)

if test (count $changes) -eq 0
    exit 0
end

git add -A

if git diff --cached --quiet
    exit 0
end

git commit -m "Backup automatico "(date "+%Y-%m-%d %H:%M")
git push
