/* Offline browser computation smoke tests; no external Node dependencies. */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const html = fs.readFileSync("web/index.html", "utf8");
const code = html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
assert.ok(code, "inline browser script present");
new vm.Script(code, {filename:"web-inline.js"});
const context = vm.createContext({
  document: {getElementById: () => ({addEventListener() {}})},
  console, Map, Set, Error,
});
vm.runInContext(code, context);
function run(expression) { return JSON.parse(JSON.stringify(vm.runInContext(expression, context))); }
assert.equal(run('reverseComplement("AAGC")'), "GCTT");
assert.equal(run('compare("AAAAAAAA", "AAAAAAAA").longest'), 0);
assert.equal(run('compare("TTTTAAAAA", "TTTTTCCCC").risk'), "high");
assert.equal(run('parseCsv("name,sequence\\nA,ACGT\\nB,TTTT").length'), 2);
assert.equal(run('parseCsv("name,sequence\\n\"Primer, one\",ACGT")[0].name'), "Primer, one");
assert.throws(() => vm.runInContext('parseCsv("x,ACGN")', context), /A\/C\/G\/T/);
assert.throws(() => vm.runInContext('parseCsv("x,ACGT\\nX,ACGT")', context), /Duplicate/);
assert.equal(html.includes("fetch('/api/audit'"), false);
assert.equal(html.includes("HMAC_SHA256_"), false);
console.log("Browser script syntax, CSV parser, matching, and offline checks passed.");
