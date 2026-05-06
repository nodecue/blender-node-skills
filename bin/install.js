#!/usr/bin/env node
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";

const packageRoot = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const sourceRoot = path.join(packageRoot, "skills");
const defaultSkill = "geometry-nodes";

function usage() {
  console.log(`Usage:
  npx @nodecue/blender-node-skills install [--target <skills-dir>] [--skill <name>] [--all] [--force]

Defaults:
  --target ~/.codex/skills
  --skill geometry-nodes

Installs:
  <target>/<skill-name>

Available now:
  geometry-nodes

Reserved future skill areas:
  shader-nodes
  compositing-nodes`);
}

function parseArgs(argv) {
  const args = {
    command: "install",
    target: path.join(os.homedir(), ".codex", "skills"),
    force: false,
    skill: defaultSkill,
    all: false,
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
    } else if (token === "--skill") {
      const value = rest.shift();
      if (!value) throw new Error("--skill requires a skill name");
      args.skill = value;
    } else if (token === "--force") {
      args.force = true;
    } else if (token === "--all") {
      args.all = true;
    } else if (token === "--help" || token === "-h") {
      args.command = "help";
    } else {
      throw new Error(`unknown argument: ${token}`);
    }
  }
  return args;
}

function isAvailableSkill(name) {
  return fs.existsSync(path.join(sourceRoot, name, "SKILL.md"));
}

function availableSkills() {
  return fs
    .readdirSync(sourceRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && isAvailableSkill(entry.name))
    .map((entry) => entry.name)
    .sort();
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
  const skills = args.all ? availableSkills() : [args.skill];
  if (!skills.length) {
    throw new Error(`no bundled skills found in ${sourceRoot}`);
  }
  for (const skill of skills) {
    if (!isAvailableSkill(skill)) {
      throw new Error(`missing bundled skill '${skill}'. Available skills: ${availableSkills().join(", ") || "none"}`);
    }
  }
  const targetRoot = path.resolve(args.target.replace(/^~(?=$|\/|\\)/, os.homedir()));
  for (const skill of skills) {
    const src = path.join(sourceRoot, skill);
    const dest = path.join(targetRoot, skill);
    if (fs.existsSync(dest)) {
      if (!args.force) {
        throw new Error(`${dest} already exists. Re-run with --force to replace it.`);
      }
      fs.rmSync(dest, { recursive: true, force: true });
    }
    copyDir(src, dest);
    console.log(`Installed NodeCue ${skill} skill to ${dest}`);
  }
}

try {
  main();
} catch (error) {
  console.error(`Error: ${error.message}`);
  process.exit(1);
}
