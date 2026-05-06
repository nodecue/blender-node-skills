#!/usr/bin/env node
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";

const packageRoot = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const sourceSkill = path.join(packageRoot, "skills", "geometry-nodes");

function usage() {
  console.log(`Usage:
  npx @nodecue/geometry-nodes-skill install [--target <skills-dir>] [--force]

Defaults:
  --target ~/.codex/skills

Installs:
  <target>/geometry-nodes`);
}

function parseArgs(argv) {
  const args = {
    command: "install",
    target: path.join(os.homedir(), ".codex", "skills"),
    force: false,
  };
  const rest = [...argv];
  if (rest[0] && !rest[0].startsWith("-")) {
    args.command = rest.shift();
  }
  while (rest.length) {
    const token = rest.shift();
    if (token === "--target") {
      const value = rest.shift();
      if (!value) throw new Error("--target requires a directory");
      args.target = value;
    } else if (token === "--force") {
      args.force = true;
    } else if (token === "--help" || token === "-h") {
      args.command = "help";
    } else {
      throw new Error(`unknown argument: ${token}`);
    }
  }
  return args;
}

function shouldSkip(name) {
  return name === ".DS_Store" || name === "__pycache__" || name.endsWith(".pyc");
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    if (shouldSkip(entry.name)) continue;
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else if (entry.isFile()) {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.command === "help") {
    usage();
    return;
  }
  if (args.command !== "install") {
    throw new Error(`unsupported command: ${args.command}`);
  }
  if (!fs.existsSync(path.join(sourceSkill, "SKILL.md"))) {
    throw new Error(`missing bundled skill at ${sourceSkill}`);
  }
  const targetRoot = path.resolve(args.target.replace(/^~(?=$|\/|\\)/, os.homedir()));
  const dest = path.join(targetRoot, "geometry-nodes");
  if (fs.existsSync(dest)) {
    if (!args.force) {
      throw new Error(`${dest} already exists. Re-run with --force to replace it.`);
    }
    fs.rmSync(dest, { recursive: true, force: true });
  }
  copyDir(sourceSkill, dest);
  console.log(`Installed NodeCue Geometry Nodes skill to ${dest}`);
}

try {
  main();
} catch (error) {
  console.error(`Error: ${error.message}`);
  process.exit(1);
}
