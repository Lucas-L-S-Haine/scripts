#!/usr/bin/env coffee
os = require "node:os"
{ Console } = require "node:console"
path = require "path"
fs = require "fs/promises"
{ createWriteStream } = require "fs"
{ exec } = require "child_process"
{ promisify } = require "util"
minimist = require "minimist"

{ _: args, options... } = minimist process.argv.slice 2

try
    run = promisify exec

    output_dir = await fs.mkdtemp [os.tmpdir(), null].join(path.sep)
    output_file = path.join(output_dir, "table#{Date.now()}")

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

    [labels, containers...] = (row.split /\s{2,}/ for row in docker_output)

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
        .replace /'/g, ""
        .replace "  (index)   ", "CONTAINER ID"
        .slice 0, -1

    output_table = table_string.split "\n"

    lines = output_table[0]
        .split "┬"
        .map (value, index) ->
            if index then value.slice(2) else value
        .join "┬"
    output_table[0] = lines

    names = output_table[1]
        .split "│"
        .map (value, index) ->
            if index > 1 then value.slice(1, -1) else value
        .join "│"
    output_table[1] = names

    lines = output_table[2]
        .split "┼"
        .map (value, index) ->
            if index then value.slice(2) else value
        .join "┼"
    output_table[2] = lines

    n = output_table.indexOf output_table.at -1
    lines = output_table[n]
        .split "┴"
        .map (value, index) ->
            if index then value.slice(2) else value
        .join "┴"
    output_table[n] = lines
    table_string = output_table.join "\n"

    table_width = table_string.split("\n")[0].length
    window_width = process.stdout.columns
    if table_width > window_width
        throw new Error "table too large to fit on output window"

catch error
    console.error error

finally
    if file? then await file.close()
    await fs.unlink output_file
    await fs.rmdir output_dir

    if table_string? then console.log table_string
