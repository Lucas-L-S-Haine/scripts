#!/usr/bin/env coffee
{ Console } = require "node:console"
fs = require "fs/promises"
{ createWriteStream } = require "fs"
{ _: argv, ...options } = require("minimist")(process.argv.slice 2)
{ exec } = require "child_process"
{ promisify } = require "util"

run = promisify exec

output_file = "./table#{Date.now()}.txt"

stdout = createWriteStream output_file
stderr = process.stderr

{ stdout: docker_output } = await run "docker ps --format table'{{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}'"

[labels, entries...] = docker_output
    .split "\n"
    .slice 0, -1

labels = labels.split /\s{2,}/
containers = [(entry.split /\s{2,}/ for entry in entries)...]

table = {}
for row in containers
    id = row[0]
    table[id] = {}
    container = row.slice 1
    for value, col in container
        table[id][labels[col + 1]] = value

writer = new Console { stdout, stderr }
await run "touch #{output_file}"
writer.table(table)

table_string = await fs.readFile output_file, encoding: "UTF-8"
table_string = table_string
    .replace /'/g, " "
    .replace "  (index)   ", "CONTAINER ID"
await fs.unlink output_file

console.log(table_string)
