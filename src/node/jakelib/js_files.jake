const { file } = require("jake");
const fs = require("fs");
const path = require("path");
const { parseName } = require("../lib/jake_actions");

const BIN_DIR = path.resolve("../..", "bin");

const ext = /^.+\.(js|cjs|mjs)$/;

const srcFiles = fs.readdirSync(".")
  .filter((file) => ext.test(file));
const outFiles = srcFiles.map(parseName)
  .filter((file) => file)
  .map((file) => path.resolve(BIN_DIR, file));

for (const link of outFiles) {
  file(link, [BIN_DIR], () => {
    const target = path.resolve(".", fs.readdirSync(".")
      .filter((jsFile) => ext.test(jsFile))
      .find((jsFile) => parseName(jsFile) === path.basename(link)));
    try {
      fs.symlinkSync(target, link);
    } catch (error) {
      if (error.code === "EEXIST") {
        fs.unlinkSync(link);
        fs.symlinkSync(target, link);
      } else {
        throw error;
      }
    }
  });
}
