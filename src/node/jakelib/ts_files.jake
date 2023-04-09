const { task, file, desc, directory, Task } = require("jake");
const fs = require("fs");
const fsp = require("fs/promises");
const path = require("path");
const cp = require("child_process");
const { parseName, fileExists, fileIsDir } = require("../lib/jake_actions");

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
  file(link, [BIN_DIR, "tsc"], async () => {
    let fileHandle;
    try {
      const target = path.resolve("dist", fs.readdirSync("dist")
        .filter((jsFile) => jsExt.test(jsFile))
        .find((jsFile) => parseName(jsFile) === path.basename(link)));
      if (!target) throw new Error("couldn’t find target");

      fileHandle = await fsp.open(target);
      if (!fileHandle) throw new Error("cannot read file");

      const linesOfCode = [];
      for await (const line of fileHandle.readLines()) linesOfCode.push(line);
      linesOfCode.shift();
      linesOfCode.unshift("#!/usr/bin/env node");

      const code = linesOfCode.join("\n");
      fs.writeFileSync(link, code, { mode: 0o755 });
    } finally {
      fileHandle.close();
    }
  });
}

directory("dist");

const shouldRun = [];
if (outFiles.every(fileExists)) shouldRun.push(false);

task("tsc", shouldRun, () => {
  cp.execFileSync(tsc);
});

task("clean", ["tsc"], () => {
  for (const file of fs.readdirSync("dist")) {
    if (fileIsDir(file)) {
      const oldPath = path.resolve("dist", file);
      const newPath = path.resolve(BIN_DIR, path.basename(file));

      fs.rmSync(newPath, { force: true, recursive: true });
      fs.renameSync(oldPath, newPath);
    }
  }

  fs.rmSync("dist", { force: true, recursive: true });
});
