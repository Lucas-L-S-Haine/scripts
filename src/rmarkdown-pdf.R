#!/usr/bin/env r

require("rmarkdown")

render(
  input = argv[1],
  output_format = pdf_document(latex_engine = "xelatex"),
  output_file = NULL,
  output_dir = getwd(),
  runtime = "auto",
  clean = TRUE,
  params = list(mainfont = "DejaVuSans"),
  envir = new.env(),
  run_pandoc = TRUE,
  quiet = FALSE
)
