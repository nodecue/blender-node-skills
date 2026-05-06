import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { spawnSync } from "node:child_process";

const repoRoot = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const target = fs.mkdtempSync(path.join(os.tmpdir(), "nodecue-skill-install-"));
const installer = path.join(repoRoot, "bin", "install.js");

const result = spawnSync(process.execPath, [installer, "install", "--target", target, "--force"], {
  cwd: repoRoot,
  encoding: "utf8",
});

if (result.status !== 0) {
  console.error(result.stdout);
  console.error(result.stderr);
  process.exit(result.status ?? 1);
}

const installed = path.join(target, "geometry-nodes");
const required = [
  "SKILL.md",
  "SYSTEM_PROMPT.md",
  "rules/node-role-catalog.md",
  "patterns/density-controlled-scatter.md",
];

for (const rel of required) {
  const file = path.join(installed, rel);
  if (!fs.existsSync(file)) {
    console.error(`Missing installed file: ${file}`);
    process.exit(1);
  }
}

const forbidden = [];
function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const current = path.join(dir, entry.name);
    if (entry.name === ".DS_Store" || entry.name === "__pycache__" || entry.name.endsWith(".pyc")) {
      forbidden.push(current);
    }
    if (entry.isDirectory()) walk(current);
  }
}
walk(installed);
if (forbidden.length) {
  console.error(`Forbidden files installed:\n${forbidden.join("\n")}`);
  process.exit(1);
}

console.log(`Install smoke passed: ${installed}`);

const secondTarget = fs.mkdtempSync(path.join(os.tmpdir(), "nodecue-skill-install-all-"));
const allResult = spawnSync(process.execPath, [installer, "install", "--target", secondTarget, "--all", "--force"], {
  cwd: repoRoot,
  encoding: "utf8",
});

if (allResult.status !== 0) {
  console.error(allResult.stdout);
  console.error(allResult.stderr);
  process.exit(allResult.status ?? 1);
}

const allInstalled = path.join(secondTarget, "geometry-nodes", "SKILL.md");
if (!fs.existsSync(allInstalled)) {
  console.error(`Missing --all install file: ${allInstalled}`);
  process.exit(1);
}
