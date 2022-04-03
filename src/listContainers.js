#!/usr/bin/env node

const { _: argv, ...options } = require('minimist')(process.argv.slice(2));
const { exec } = require('shelljs');

const output = exec('docker ps --format table"{{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Command}}\t{{.Status}}"', {silent: true}).stdout;
console.log(output);

/*
  - .ID           - Container ID.
  - .Image        - Image ID.
  - .Command      - Quoted command.
  - .CreatedAt    - Time when the container was created.
  - .RunningFor   - Elapsed time since the container was started.
  - .Ports        - Exposed ports.
  - .Status       - Container status.
  - .Size         - Container disk size.
  - .Names        - Container names.
  - .Labels       - All labels assigned to the container.
  - .Label        - Value of a specific label for this container.
                    For example '{{.Label "com.docker.swarm.cpu"}}'.
  - .Mounts       - Names of the volumes mounted in this container.
  - .Networks     - Names of the networks attached to this container.
*/

// container id
// image
// command
// created
// status
// ports
