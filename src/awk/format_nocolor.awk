#!/usr/bin/awk -f
{
  modified = gensub(/:\s/, ":\t", 1)
  printf " - %s %s %s\n", $1, $2, substr(modified, index(modified, $5))
}
