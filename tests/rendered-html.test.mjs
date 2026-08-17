import assert from "node:assert/strict";
import test from "node:test";

async function render(path = "/") {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}-${Math.random()}`);
  const { default: worker } = await import(workerUrl.href);
  const response = await worker.fetch(new Request(`http://localhost${path}`, { headers: { accept: "text/html" } }), { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } }, { waitUntil() {}, passThroughOnException() {} });
  return { response, html: await response.text() };
}

function withoutRenderComments(html) { return html.replace(/<!--.*?-->/g, ""); }

test("home renders the clubhouse hero and links to every live room", async () => {
  const { response, html: rawHtml } = await render("/");
  const html = withoutRenderComments(rawHtml);
  assert.equal(response.status, 200);
  assert.match(html, /Welcome to the Clubhouse/);
  assert.match(html, /Espinosa Fantasy Football Clubhouse/);
  assert.match(html, /href="\/champions"/);
  assert.match(html, /href="\/seasons"/);
  assert.match(html, /href="\/managers"/);
  assert.match(html, /href="\/rivalries"/);
  assert.match(html, /Coming Soon/);
});

test("home features the reigning 2025 champion and the full trophy shelf", async () => {
  const { html: rawHtml } = await render("/");
  const html = withoutRenderComments(rawHtml);
  assert.match(html, /2025 League Champion/);
  assert.match(html, /Elliot/);
  assert.match(html, /118\.4/);
  assert.match(html, /80\.8/);
  assert.match(html, />2023</);
  assert.match(html, />2024</);
  assert.match(html, />2025</);
});

test("home shows a rivalry spotlight with an all-time head-to-head score", async () => {
  const { html: rawHtml } = await render("/");
  const html = withoutRenderComments(rawHtml);
  assert.match(html, /Rivalry Spotlight/);
  assert.match(html, /ALL TIME/);
});

test("trophy room lists every champion and the championship records", async () => {
  const { response, html: rawHtml } = await render("/champions");
  const html = withoutRenderComments(rawHtml);
  assert.equal(response.status, 200);
  assert.match(html, /Reigning Champion/);
  assert.match(html, /Shawn/);
  assert.match(html, /Jennifer/);
  assert.match(html, /Elliot/);
  assert.match(html, /Closest Championship/);
  assert.match(html, /0\.2/);
  assert.match(html, /Biggest Margin/);
  assert.match(html, /37\.6/);
  assert.match(html, /Still Waiting/);
  assert.match(html, /Daphne/);
});

test("locker room shows four active managers and Wyatt's reserved family spot", async () => {
  const { response, html: rawHtml } = await render("/managers");
  const html = withoutRenderComments(rawHtml);
  assert.equal(response.status, 200);
  for (const name of ["Shawn", "Jennifer", "Daphne", "Elliot"]) assert.match(html, new RegExp(name));
  assert.match(html, /Wyatt/);
  assert.match(html, /Future Manager/);
  assert.match(html, /Head-to-Head Matrix/);
  assert.match(html, /Career Totals/);
  assert.match(html, /Year-by-Year Records/);
});

test("rivalry arena renders all six pairs and the playoff-encounters table", async () => {
  const { response, html: rawHtml } = await render("/rivalries");
  const html = withoutRenderComments(rawHtml);
  assert.equal(response.status, 200);
  // Every one of the 6 combinations of the 4 active managers should appear as a rivalry card.
  const managers = ["Shawn", "Jennifer", "Daphne", "Elliot"];
  for (let i = 0; i < managers.length; i += 1) {
    for (let j = i + 1; j < managers.length; j += 1) {
      const pairShowsUp = new RegExp(`${managers[i]}[\\s\\S]{0,400}${managers[j]}|${managers[j]}[\\s\\S]{0,400}${managers[i]}`).test(html);
      assert.ok(pairShowsUp, `expected a rivalry card pairing ${managers[i]} and ${managers[j]}`);
    }
  }
  assert.match(html, /ALL TIME/);
  assert.match(html, /Playoff Encounters/);
  assert.match(html, /🏆 Championship/);
});

test("seasons index redirects to the latest completed season", async () => {
  const { response } = await render("/seasons");
  assert.equal(response.status, 307);
  assert.match(response.headers.get("location") ?? "", /\/seasons\/2025$/);
});

test("a specific season page renders standings, bracket, and draft day", async () => {
  const { response, html: rawHtml } = await render("/seasons/2024");
  const html = withoutRenderComments(rawHtml);
  assert.equal(response.status, 200);
  assert.match(html, /2024 Champion/);
  assert.match(html, /Jennifer/);
  assert.match(html, /Regular Season Standings/);
  assert.match(html, /Playoff Bracket/);
  assert.match(html, /Championship — Week 17/);
  assert.match(html, /Draft Day/);
  assert.match(html, /Round 1/);
});

test("an out-of-range season and an unknown route both 404 with the designed page", async () => {
  for (const path of ["/seasons/1999", "/seasons/abc", "/nope"]) {
    const { response, html } = await render(path);
    assert.equal(response.status, 404, path);
    assert.match(html, /isn.t in the Clubhouse/, path);
  }
});
