import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

const root = new URL("..", import.meta.url).pathname;
const appSource = readFileSync(join(root, "src/App.jsx"), "utf8");
const styleSource = readFileSync(join(root, "src/styles.css"), "utf8");

test("prototype exposes the three primary mobile tabs", () => {
  for (const label of ["对话", "记录", "我的"]) {
    assert.match(appSource, new RegExp(label));
  }
});

test("prototype covers the PRD core scenarios and safety concepts", () => {
  for (const label of [
    "历史知识",
    "项目变更",
    "需求提炼",
    "系统问题",
    "PII",
    "钉钉流程",
    "结构化输出",
  ]) {
    assert.match(appSource, new RegExp(label));
  }
});

test("prototype includes interactive state for tabs, uploads, output, and submission", () => {
  for (const stateName of [
    "activeTab",
    "uploadPanelOpen",
    "outputOpen",
    "submitted",
    "maskSensitive",
  ]) {
    assert.match(appSource, new RegExp(stateName));
  }
});

test("mobile shell keeps a fixed 390px canvas and safe bottom input", () => {
  assert.match(styleSource, /max-width:\s*390px/);
  assert.match(styleSource, /position:\s*sticky/);
  assert.match(styleSource, /bottom:\s*0/);
});
