const { task, file, desc, directory, Task } = require("jake");
const fs = require("fs");
const path = require("path");
const cp = require("child_process");
const { Console } = require("node:console");
const { parseName, fileExists } = require("../lib/jake_actions");

const tsc = path.resolve("../..", "node_modules/.bin", "tsc");

const BIN_DIR = path.resolve("../..", "bin");

const ext = /.+\.ts$/;
const jsExt = /.+\.js$/;

const srcFiles = fs.readdirSync(".")
  .filter((file) => ext.test(file));
const outFiles = srcFiles.map(parseName)
  .filter((file) => file)
  .map((file) => path.resolve(BIN_DIR, file));

const getSrc = (file) => path.resolve(".", fs.readdirSync(".")
  .filter((tsFile) => ext.test(tsFile))
  .find((tsFile) => parseName(tsFile) === path.basename(file)));

for (const link of outFiles) {
  file(link, [BIN_DIR, "tsc"], () => {
    const target = path.resolve("dist", fs.readdirSync("dist")
      .filter((jsFile) => jsExt.test(jsFile))
      .find((jsFile) => parseName(jsFile) === path.basename(link)));

    if (!target) throw new Error("couldn’t find target");
    const writeStream = fs.createWriteStream(link, { mode: 0o755 });
    const output = new Console({ stdout: writeStream });
    const content = fs.readFileSync(target).toString();

    if (!content) throw new Error("cannot read file");
    const linesOfCode = content.toString().trim().split("\n");
    linesOfCode.shift();
    linesOfCode.unshift("#!/usr/bin/env node");
    const code = linesOfCode.join("\n");

    output.log(code);
  });

  Task[link].on("start", () => {
    const stream = fs.createWriteStream(link, { mode: 0o755 });
    stream.close();
  });
}

directory("dist");

const shouldRun = [];
if (outFiles.every(fileExists)) shouldRun.push(false);

task("tsc", shouldRun, () => {
  cp.execFileSync(tsc);
});

task("clean", () => {
  fs.rmSync("dist", { force: true, recursive: true });
});
