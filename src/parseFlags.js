#!/usr/bin/env node

const { _: args, ...options } = require('minimist')(process.argv.slice(2));
const { exec } = require('shelljs');

console.log('args:', args);
console.log('options:', options);
