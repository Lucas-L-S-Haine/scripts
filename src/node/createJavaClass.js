#!/usr/bin/env node
const fs = require('fs');
const { basename } = require('path');
const { _: classes, ...options } = require('minimist')(process.argv.slice(2));

const dirname = basename(process.env.PWD);

const packageName = options.package || options.p || dirname;
const code = (packageName, className) =>
  `package ${packageName};

public class ${className} {

}\n`;

classes
  .map((className) => [`${className}.java`, className])
  .forEach(([file, className]) => fs.writeFileSync(file, code(packageName, className),
    { encoding: 'utf-8', mode: 0o644, flag: 'w' }))
