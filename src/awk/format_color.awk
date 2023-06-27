#!/usr/bin/awk -f
function red(str) {
  return "\033[38;2;210;45;45m" str "\033[39m"
}

function yellow(str) {
  return "\033[38;2;210;195;60m" str "\033[39m"
}

function dark_cyan(str) {
  return "\033[38;2;21;161;161m" str "\033[39m"
}

function orange(str) {
  return "\033[38;2;225;128;30m" str "\033[39m"
}

function commit_type(str) {
  if (str == "feat!:") return red(str)
  else if (str == "feat:") return orange(str)
  else if (str == "fix:") return yellow(str)
  else return str
}

{
  match($0, /(feat!:)|(feat:)|(fix:)|(build:)/)
  printf " - %s %s %s\t%s\n", $1, $2, commit_type($5), substr($0, RSTART + RLENGTH + 1)
}
