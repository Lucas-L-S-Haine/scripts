const path = require("path");
const fs = require("fs");
const { desc, task } = require("jake");

const SRC_DIR = path.join(__dirname, "..");
const BIN_DIR = path.resolve(SRC_DIR, "../..", "bin");
const ext = /\.(js|cjs|mjs|ts)$/;

function fileExists(file) {
  let exists = true;
  try {
    const stats = fs.statSync(file);
    if (stats.size === 0) exists = false;
  } catch (error) {
    if (error.code === "ENOENT") {
      exists = false;
    }
  }

  return exists;
}

function fileIsDir(file) {
  if (!fileExists(file)) return false;
  return fs.statSync(file).isDirectory();
}

function directoryIsEmpty(directory) {
  let isEmpty = false;
  try {
    if (fs.readdirSync(directory).length === 0) isEmpty = true;
  } catch {
    return false;
  }

  return isEmpty;
}

function readDirectoryTree(file = ".", full = false) {
  if (!fileIsDir(file)) return [file];

  const result = [];
  for (const filename of fs.readdirSync(file)) {
    let filepath;
    if (full) {
      filepath = path.resolve(file, filename);
    } else {
      filepath = path.join(file, filename);
    }

    result.push(...readDirectoryTree(filepath));
  }

  return result;
}

function getListedLinks() {
  let result;
  const links = path.join(SRC_DIR, "links.txt");
  try {
    result = fs.readFileSync(links, { encoding: "utf-8" });
  } catch {
    result = "";
  }
  return result;
}

function parseName(file) {
  let symlink;
  try {
    symlink = getListedLinks()
      .trim()
      .split("\n")
      .filter((filename) => RegExp(file).test(filename))[0]
      .split(":")[1];
  } catch {
    symlink = file
      .replace(/_/, "-")
      .replace(ext, "");
  }

  if (symlink !== "") return symlink;
}

function runUnlink() {
  const tree = [];

  fs.readdirSync(".")
    .filter((file) => ext.test(file))
    .map(parseName)
    .filter((file) => file)
    .map((file) => path.resolve(BIN_DIR, file))
    .forEach((file) => fs.rmSync(file, { force: true }));

  fs.readdirSync(".")
    .filter(fileIsDir)
    .map((dir) => readDirectoryTree(dir, false))
    .forEach((fileList) => tree.push(...fileList));

  tree
    .map((file) => path.resolve(BIN_DIR, file))
    .map((file) => file.replace(/\.ts$/, ".js"))
    .filter(fileExists)
    .forEach((file) => fs.rmSync(file));

  fs.readdirSync(BIN_DIR)
    .map((dir) => path.resolve(BIN_DIR, dir))
    .filter(directoryIsEmpty)
    .forEach((dir) => fs.rmdirSync(dir));
}

module.exports = { runUnlink, parseName, fileExists, fileIsDir, readDirectoryTree, directoryIsEmpty };
