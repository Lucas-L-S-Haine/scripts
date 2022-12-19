const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const { desc, task } = require('jake');

const SRC_DIR = path.join(__dirname, '..');

function runList() {
  const results = returnLinkNames();

  results.forEach(([jsFile, symlink]) => console.log(`${jsFile} -> ${symlink}`));
}

function runLink() {
  const filePairs = returnLinkNames();
  const targetDir = path.join(SRC_DIR, '../../bin');

  for (let index = 0; index < filePairs.length; index += 1) {
    let [jsFile, symlink] = filePairs[index];
    let target = [SRC_DIR, jsFile].join('/');
    let path = [targetDir, symlink].join('/');
    try {
      fs.symlinkSync(target, path);
    } catch (error) {
      if (error.code === 'EEXIST') {
        fs.unlinkSync(path);
        fs.symlinkSync(target, path);
      } else {
        throw error;
      }
    }
  }

  console.log("\x1b[32mLinks successfully created!\x1b[00m");
}

function runClean() {
  const filePairs = returnLinkNames();
  const targetDir = path.join(SRC_DIR, '../../bin');

  for (let index = 0; index < filePairs.length; index += 1) {
    let [_, symlink] = filePairs[index];
    let path = [targetDir, symlink].join('/');
    fs.unlink(path, handleClean);
  }
}

function handleClean(err) {
  if (err && err.code !== 'ENOENT') throw err;
}

function createLinkName(jsFileName) {
  const linkName = jsFileName
    .split('.')
    .at(0)
    .split('')
    .replace('-', '_')
    .join('');

  return linkName;
}

function returnLinkNames() {
  const listedLinks = getListedLinks();
  const jsFiles = getJsFiles();
  const linkMatrix = listedLinks
    .trim()
    .split('\n')
    .map((name) => name.split(':'));
  const linkedJsFiles = [];
  const resultingLinks = [];

  linkMatrix.forEach(([file, symlink]) => {
    linkedJsFiles.push(file);
    resultingLinks.push(symlink);
  });

  const result = [];
  for (let index = 0; index < jsFiles.length; index += 1) {
    const fileName = jsFiles[index];
    const fileIndex = linkedJsFiles.indexOf(fileName);
    let linkName;

    if (fileIndex !== -1) {
      linkName = resultingLinks[fileIndex];
    } else {
      linkName = createLinkName(fileName);
    }

    if (linkName !== '') result.push([fileName, linkName]);
  }

  return result;
}

function getJsFiles() {
  return fs.readdirSync(SRC_DIR)
    .filter((filename) => /\.(js|cjs|mjs)$/.test(filename));
}

function getListedLinks() {
  let result;
  const links = path.join(SRC_DIR, 'links.txt');
  try {
    result = fs.readFileSync(links, { encoding: 'utf-8' });
  } catch {
    result = '';
  }
  return result;
}

module.exports = { runList, runLink, runClean };
