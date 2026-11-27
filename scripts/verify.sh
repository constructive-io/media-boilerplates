#!/usr/bin/env bash
# Scaffold a workspace and two decks as a person would, and check what came out.
#
#   bash scripts/verify.sh              # scaffold and check, then throw it away
#   bash scripts/verify.sh FOLDER       # the same, and keep what was made in FOLDER
#
# Needs pgpm (npm install -g pgpm), node, pnpm and python3. With Constructive Media
# installed (`me`), the same is scaffolded with `me init` and the two trees are compared:
# both tools must write the same files. PGPM="npx -y pgpm@latest" tries another pgpm.
# It does not say or film anything: that takes the engine and a voice.
set -euo pipefail

here="$(cd "$(dirname "$0")/.." && pwd)"
scratch="$(mktemp -d)"
trap 'rm -rf "$scratch"' EXIT
made="${1:-$scratch/made}"
mkdir -p "$made"
made="$(cd "$made" && pwd)"
pgpm="${PGPM:-pgpm}"

# pgpm reads a template repository from git, so it is given a commit of what is here now.
mkdir "$scratch/templates"
(cd "$here" && tar --exclude .git --exclude node_modules -cf - .) | tar -xf - -C "$scratch/templates"
git -C "$scratch/templates" init --quiet
git -C "$scratch/templates" add --all
git -C "$scratch/templates" -c user.name=verify -c user.email=verify@example.com -c commit.gpgsign=false \
  commit --quiet --message "what is here now"

for folder in "$here"/media/*/; do
  name="$(basename "$folder")"
  case "$name" in workspace|module) ;; *) echo "media/$name is a template this script does not check"; exit 1 ;; esac
done

# Every answer is given: who made it is not left to whatever git says on this machine.
workspace=(--fullName "Ada Marsh" --email ada@example.com --repoName harbour-talks --license MIT)
deck=(--title "The harbour at night" --fullName "Ada Marsh" --role "Keeper of the light")

run() { "$@" > "$scratch/init.log" 2>&1 || { cat "$scratch/init.log"; exit 1; }; }

echo "pgpm: a workspace, a deck from its top, a deck from further in"
rm -rf "$made/pgpm" && mkdir -p "$made/pgpm"
(cd "$made/pgpm" && run $pgpm init workspace --repo "$scratch/templates" --name "Harbour Talks" \
    "${workspace[@]}" --no-tty --refresh)
(cd "$made/pgpm/harbour-talks" && run $pgpm init --repo "$scratch/templates" --moduleName first-talk \
    "${deck[@]}" --no-tty)
(cd "$made/pgpm/harbour-talks/packages" && run $pgpm init --repo "$scratch/templates" --moduleName "Second Talk" \
    "${deck[@]}" --no-tty)
out="$made/pgpm/harbour-talks"

echo "every answer landed"
if grep -rn "____" "$out"; then echo "a blank was left in"; exit 1; fi
for file in package.json pnpm-workspace.yaml README.md AGENTS.md LICENSE .gitignore .github/workflows/ci.yml; do
  [ -f "$out/$file" ] || { echo "missing: $file"; exit 1; }
done
for name in first-talk second-talk; do
  for file in package.json README.md AGENTS.md index.html talk.conv; do
    [ -f "$out/packages/$name/$file" ] || { echo "missing: packages/$name/$file"; exit 1; }
  done
  grep -q "\"name\": \"$name\"" "$out/packages/$name/package.json"
  grep -q "out/$name.mp4" "$out/packages/$name/package.json"
  grep -q "The harbour at night" "$out/packages/$name/index.html"
  grep -q "name: Ada Marsh, title: Keeper of the light" "$out/packages/$name/talk.conv"
done
if find "$out" -name ".boilerplate*.json" -o -name .motd | grep .; then echo "a template's own file was copied in"; exit 1; fi
grep -q '"name": "harbour-talks"' "$out/package.json"
grep -q '"author": "Ada Marsh <ada@example.com>"' "$out/package.json"
grep -q "Ada Marsh <ada@example.com>" "$out/LICENSE"

echo "the page of each deck has what its script names"
for name in first-talk second-talk; do
  python3 "$here/scripts/follows.py" "$out/packages/$name/talk.conv" "$out/packages/$name/index.html"
done

if command -v me > /dev/null 2>&1; then
  echo "me: the same, and the two trees are the same"
  rm -rf "$made/me" && mkdir -p "$made/me"
  (cd "$made/me" && run me init workspace "Harbour Talks" --repo "$here" "${workspace[@]}" "${deck[@]}" --no-tty)
  (cd "$made/me/harbour-talks/packages" && run me init --repo "$here" --moduleName "Second Talk" "${deck[@]}" --no-tty)
  diff -r "$made/pgpm/harbour-talks" "$made/me/harbour-talks"
else
  echo "me is not installed: scaffolded with pgpm only"
fi

echo "the workspace installs, and every script is a script"
(cd "$out" && pnpm install --silent && pnpm lint)

echo "ok"
