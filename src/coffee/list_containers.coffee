#!/usr/bin/env coffee
{ Console } = require "node:console"
fs = require "fs/promises"
{ createWriteStream } = require "fs"
{ exec } = require "child_process"
{ promisify } = require "util"
minimist = require "minimist"

{ _: args, options... } = minimist process.argv.slice 2

try
    run = promisify exec

    output_file = "./table#{Date.now()}.txt"

    stdout = createWriteStream output_file
    stderr = process.stderr

    docker_args = ["ps"]
    docker_args.push "-a" if options["a"] or options["all"]
    docker_args.push ["--format",
        "'table{{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}'"]...
    docker_command = ["docker"]
        .concat docker_args
        .join " "

    { stdout: docker_output } = await run docker_command

    docker_output = docker_output
        .split "\n"
        .slice 0, -1

    [labels, containers...] = [(row.split /\s{2,}/ for row in docker_output)...]

    table = {}
    for row in containers
        id = row[0]
        table[id] = {}
        container = row.slice 1
        for value, col in container
            table[id][labels[col + 1]] = value

    writer = new Console { stdout, stderr }
    writer.table table

    file = await fs.open output_file, "r"
    table_string = await file.readFile encoding: "UTF-8"
    table_string = table_string
        .replace /'/g, " "
        .replace "  (index)   ", "CONTAINER ID"
        .slice 0, -1

catch error
    console.error error

finally
    if file? then await file.close()
    await fs.unlink output_file

    if table_string? then console.log table_string
