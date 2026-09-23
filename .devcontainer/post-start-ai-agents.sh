#!/bin/bash
# this script is used as part of "postStartCommand" in devcontainer.json (called from post-start.sh)
#
# WORKAROUND (temporary, see docs/ai-agents.md and .devcontainer/ai-agents.md):
# `auggie` (Auggie CLI) silently finds zero rules through the symlink `.augment/rules ->
# ../.agents/rules` - it appears to resolve directory entries by their raw (non-dereferenced)
# type, under which a symlinked directory looks like neither a file nor a directory, so it gets
# silently skipped. A real, non-symlinked directory in the same location is read correctly.
#
# Until this is fixed upstream, materialize the symlink into a real directory containing a fresh
# copy of the source `.md` files on every container start. The materialize flag below (true/1 to
# materialize, false/0 to keep/restore the plain symlink instead) makes this easy to toggle.

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT" || exit 1

# materialize $target_dir (normally a symlink to $source_dir, created as $symlink_target) into a
# real directory with a fresh copy of $source_dir's content, so tools that don't resolve
# symlinked directories can still read it; with $materialize set to false/0, ensure $target_dir
# is the plain symlink instead
materialize_dir() {
  local target_dir="$1"
  local source_dir="$2"
  local symlink_target="$3"
  local materialize="$4"

  case "$materialize" in
    false|0|"") materialize=false ;;
    *) materialize=true ;;
  esac

  if [ "$materialize" = false ]; then
    if [ ! -L "$target_dir" ]; then
      rm -rf "$target_dir"
      ln -s "$symlink_target" "$target_dir"
    fi
    return
  fi

  rm -rf "$target_dir"
  mkdir -p "$target_dir"
  find "$source_dir" -mindepth 1 -maxdepth 1 ! -name ".gitkeep" -exec cp -a {} "$target_dir/" \;
  command -v git >/dev/null 2>&1 && echo "*" > "$target_dir/.gitignore"
}

echo "" && echo "Materializing .augment/rules (auggie symlinked-rules workaround)..."
materialize_dir ".augment/rules" ".agents/rules" "../.agents/rules" true
