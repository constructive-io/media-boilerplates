#!/usr/bin/env bash
# Scaffold a workspace, one of everything that goes in one, and a library of voices, as a
# person would, and check what came out.
#
#   bash scripts/verify.sh              # scaffold and check, then throw it away
#   bash scripts/verify.sh FOLDER       # the same, and keep what was made in FOLDER
#
# Needs pgpm (npm install -g pgpm), node, pnpm and python3. With Constructive Media
# installed (`media`), the same is scaffolded with `media init` and the two trees are compared:
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

# What goes into a workspace besides a deck: the template, what is made from it, and its script.
kinds=("walkthrough harbour-tour tour.conv" "animation harbour-film scene.conv" "document harbour-report reading.conv")

for folder in "$here"/media/*/; do
  name="$(basename "$folder")"
  case "$name" in workspace|module|library) continue ;; esac
  known=""
  for kind in "${kinds[@]}"; do [ "${kind%% *}" = "$name" ] && known=yes; done
  [ -n "$known" ] || { echo "media/$name is a template this script does not check"; exit 1; }
done

# Every answer is given: who made it is not left to whatever git says on this machine.
workspace=(--fullName "Ada Marsh" --email ada@example.com --repoName harbour-talks --license MIT)
deck=(--title "The harbour at night" --fullName "Ada Marsh" --role "Keeper of the light")

run() { "$@" > "$scratch/init.log" 2>&1 || { cat "$scratch/init.log"; exit 1; }; }

# The skills at the top of what was made are these, and no others.
skills() {
  local top="$1" found; shift
  found="$(cd "$top/.agents/skills" 2> /dev/null && ls | tr '\n' ' ')" || found=""
  [ "$found" = "$(printf '%s\n' "$@" | sort | tr '\n' ' ')" ] \
    || { echo "$top/.agents/skills holds: ${found:-nothing}; wanted: $*"; exit 1; }
  for skill in "$@"; do [ -f "$top/.agents/skills/$skill/SKILL.md" ] || { echo "$skill has no SKILL.md"; exit 1; }; done
}

echo "pgpm: a workspace, a deck from its top, a deck from further in, and one of everything else"
rm -rf "$made/pgpm" && mkdir -p "$made/pgpm"
(cd "$made/pgpm" && run $pgpm init workspace --repo "$scratch/templates" --name "Harbour Talks" \
    "${workspace[@]}" --no-tty --refresh)
(cd "$made/pgpm/harbour-talks" && run $pgpm init --repo "$scratch/templates" --moduleName first-talk \
    "${deck[@]}" --no-tty)
(cd "$made/pgpm/harbour-talks/packages" && run $pgpm init --repo "$scratch/templates" --moduleName "Second Talk" \
    "${deck[@]}" --no-tty)
for kind in "${kinds[@]}"; do
  read -r template name script <<< "$kind"
  (cd "$made/pgpm/harbour-talks" && run $pgpm init --repo "$scratch/templates" --template "$template" \
      --moduleName "$name" "${deck[@]}" --no-tty)
done
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
for kind in "${kinds[@]}"; do
  read -r template name script <<< "$kind"
  for file in package.json README.md AGENTS.md index.html "$script"; do
    [ -f "$out/packages/$name/$file" ] || { echo "missing: packages/$name/$file"; exit 1; }
  done
  grep -q "\"name\": \"$name\"" "$out/packages/$name/package.json"
  grep -q "out/$name.mp4" "$out/packages/$name/package.json"
  grep -q "The harbour at night" "$out/packages/$name/index.html"
  grep -q "name: Ada Marsh, title: Keeper of the light" "$out/packages/$name/$script"
done
grep -q "out/harbour-report.pdf" "$out/packages/harbour-report/package.json"
if find "$out" -name ".boilerplate*.json" -o -name .motd -o -name Makefile | grep .; then echo "a template's own file was copied in"; exit 1; fi
grep -q '"name": "harbour-talks"' "$out/package.json"
grep -q '"author": "Ada Marsh <ada@example.com>"' "$out/package.json"
grep -q "Ada Marsh <ada@example.com>" "$out/LICENSE"

echo "every page has what its script names"
for name in first-talk second-talk; do
  python3 "$here/scripts/follows.py" "$out/packages/$name/talk.conv" "$out/packages/$name/index.html"
done
for kind in "${kinds[@]}"; do
  read -r template name script <<< "$kind"
  python3 "$here/scripts/follows.py" "$out/packages/$name/$script" "$out/packages/$name/index.html"
done

if command -v media > /dev/null 2>&1; then
  echo "media: the same, and the two trees are the same"
  rm -rf "$made/media" && mkdir -p "$made/media"
  (cd "$made/media" && run media init workspace "Harbour Talks" --repo "$here" "${workspace[@]}" "${deck[@]}" --no-tty)
  (cd "$made/media/harbour-talks/packages" && run media init --repo "$here" --moduleName "Second Talk" "${deck[@]}" --no-tty)
  for kind in "${kinds[@]}"; do
    read -r template name script <<< "$kind"
    (cd "$made/media/harbour-talks" && run media init "$template" "$name" --repo "$here" "${deck[@]}" --no-tty)
  done
  # The skills are fetched, each tool keeping its own copy for a while: they are counted below, not compared.
  diff -r -x .agents "$made/pgpm/harbour-talks" "$made/media/harbour-talks"
  skills "$made/media/harbour-talks" constructive-media conv media-workspace narrated-video narrated-document
else
  echo "media is not installed: scaffolded with pgpm only"
fi

echo "the skills came with it"
skills "$out" constructive-media conv media-workspace narrated-video narrated-document

echo "the workspace installs, and every script is a script"
(cd "$out" && pnpm install --silent && pnpm lint)

# A library is a repository of its own: it is made outside any workspace.
library=(--description "The keepers of the light." --fullName "Ada Marsh" --license "CC-BY-4.0")

echo "pgpm: a library of voices, with nothing in it yet"
rm -rf "$made/pgpm-library" && mkdir -p "$made/pgpm-library"
(cd "$made/pgpm-library" && run $pgpm init --repo "$scratch/templates" --template library \
    --moduleName lighthouse-voices "${library[@]}" --no-tty)
kept="$made/pgpm-library/lighthouse-voices"
skills "$kept" constructive-media conv voice-library build-a-voice

echo "library: every answer landed"
if grep -rn "____" "$kept"; then echo "a blank was left in"; exit 1; fi
for file in media-library.json README.md AGENTS.md .gitignore .github/workflows/check.yml scripts/check.py \
            voices/README.md banks/README.md sounds/README.md faces/README.md originals/README.md CONSENT.md; do
  [ -f "$kept/$file" ] || { echo "missing: $file"; exit 1; }
done
if find "$kept" -name ".boilerplate*.json" -o -name .motd -o -name package.json | grep .; then
  echo "a library is not a package, and a template's own file is not copied in"; exit 1
fi
python3 - "$kept/media-library.json" <<'PY'
import json, sys
manifest = json.load(open(sys.argv[1]))
assert manifest["library"] == "lighthouse-voices", manifest
assert manifest["license"] == "CC-BY-4.0", manifest
assert manifest["summary"] == "The keepers of the light.", manifest
assert manifest["voices"] == [], manifest
PY

echo "library: the engine can write its table of voices, and only the page about recordings is kept of originals/"
grep -q "^<!-- voices -->$" "$kept/README.md" && grep -q "^<!-- /voices -->$" "$kept/README.md" \
  || { echo "the README has lost the marks around its table of voices"; exit 1; }
git -C "$kept" init --quiet
touch "$kept/originals/narrator.wav"
git -C "$kept" add --all
committed="$(git -C "$kept" ls-files originals)"
[ "$committed" = "originals/README.md" ] || { echo "originals/ would commit: $committed"; exit 1; }
rm -rf "$kept/.git" "$kept/originals/narrator.wav"

echo "library: it is a library, by its own check"
PYTHONDONTWRITEBYTECODE=1 python3 "$kept/scripts/check.py" | tee "$scratch/check.log"
grep -q "^ok: lighthouse-voices, 0 voice(s)$" "$scratch/check.log"

if command -v media > /dev/null 2>&1; then
  echo "media: the same library"
  rm -rf "$made/media-library" && mkdir -p "$made/media-library"
  (cd "$made/media-library" && run media init library lighthouse-voices --repo "$here" "${library[@]}" --no-tty)
  diff -r -x .agents "$kept" "$made/media-library/lighthouse-voices"
  skills "$made/media-library/lighthouse-voices" constructive-media conv voice-library build-a-voice
fi

echo "ok"
