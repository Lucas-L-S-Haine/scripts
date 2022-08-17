#!/usr/bin/env r

if (isatty(stdin())) {
  system2("docker", args = "container exec -it mongo mongosh", argv)
} else {
  system2("docker", args = "container exec -i mongo mongosh", argv)
  cat("\n")
}
