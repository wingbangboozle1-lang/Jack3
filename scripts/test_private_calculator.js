"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const calculator = require("./private_calculator.js");

function close(actual, expected, message) {
  assert.ok(Math.abs(actual - expected) < 1e-9, message || `${actual} != ${expected}`);
}

// Zero-rate and discounted-annuity cases.
assert.equal(calculator.annuityFactor(0, 3), 3);
close(calculator.annuityFactor(0.05, 3), (1 - Math.pow(1.05, -3)) / 0.05);
close(calculator.annuityFactor(1.01, 2), (1 - Math.pow(2.01, -2)) / 1.01);
close(calculator.presentValue(10, 100, 0, 3), 130);
close(calculator.presentValue(10, 100, 0.1, 1), 10 / 1.1 + 100 / 1.1);

// Sale proceeds are a transparent sum of user-entered quote / adviser items.
assert.equal(calculator.netSaleProceeds({
  grossPrice: 1000000,
  transactionCosts: 40000,
  transferTaxes: 10000,
  debtPayoff: 100000,
  incomeTaxes: 150000,
  otherCosts: 5000
}), 695000);

// Both hold and renewal outputs are present values; no pathway is ranked.
const sample = calculator.compare({
  years: 3,
  discountRatePct: 5,
  sale: {
    grossPrice: 1000000,
    transactionCosts: 40000,
    transferTaxes: 10000,
    debtPayoff: 100000,
    incomeTaxes: 150000,
    otherCosts: 5000
  },
  hold: { annualNetCashFlow: 50000, terminalNetProceeds: 800000 },
  renewal: { annualNetCashFlow: 60000, terminalNetProceeds: 850000 }
});
const factor = (1 - Math.pow(1.05, -3)) / 0.05;
close(sample.saleNow, 695000);
close(sample.holdPresentValue, 50000 * factor + 800000 / Math.pow(1.05, 3));
close(sample.renewalPresentValue, 60000 * factor + 850000 / Math.pow(1.05, 3));
close(sample.holdDifferenceVsSale, sample.holdPresentValue - sample.saleNow);
close(sample.renewalDifferenceVsSale, sample.renewalPresentValue - sample.saleNow);

// Negative operating cash flow / terminal proceeds are valid; missing or invalid model inputs are not.
assert.ok(calculator.presentValue(-100, -1000, 0.03, 5) < 0);
assert.throws(() => calculator.annuityFactor(-0.01, 3), RangeError);
assert.throws(() => calculator.annuityFactor(0.05, 0), RangeError);
assert.throws(() => calculator.compare(null), TypeError);

// Exercise the same click / validation / clear flow used by the generated browser page.
const allIds = calculator.FIELD_IDS.concat([
  "calculate-button", "clear-button", "calculator-error", "calculator-results",
  "result-sale", "result-hold", "result-renew", "result-hold-gap", "result-renew-gap"
]);
const elements = Object.fromEntries(allIds.map((id) => [id, {
  id,
  value: "",
  textContent: "",
  hidden: id === "calculator-results" || id === "calculator-error",
  listeners: {},
  addEventListener(event, callback) { this.listeners[event] = callback; }
}]));
const fakeDocument = { getElementById(id) { return elements[id] || null; } };
calculator.init(fakeDocument);
elements["calculate-button"].listeners.click();
assert.equal(elements["calculator-error"].hidden, false);
assert.match(elements["calculator-error"].textContent, /Complete every input/);
assert.equal(elements["calculator-results"].hidden, true);
const browserInputs = {
  "horizon-years": "3", "discount-rate": "5", "sale-gross": "1000000",
  "sale-costs": "40000", "sale-transfer": "10000", "sale-debt": "100000",
  "sale-tax": "150000", "sale-other": "5000", "hold-annual-net": "50000",
  "hold-terminal-net": "800000", "renew-annual-net": "60000", "renew-terminal-net": "850000"
};
Object.entries(browserInputs).forEach(([id, value]) => { elements[id].value = value; });
elements["calculate-button"].listeners.click();
assert.equal(elements["calculator-error"].hidden, true);
assert.equal(elements["calculator-results"].hidden, false);
assert.match(elements["result-sale"].textContent, /695,000/);
assert.notEqual(elements["result-hold"].textContent, "—");
assert.notEqual(elements["result-renew"].textContent, "—");
elements["clear-button"].listeners.click();
assert.ok(calculator.FIELD_IDS.every((id) => elements[id].value === ""));
assert.equal(elements["calculator-results"].hidden, true);
assert.equal(elements["calculator-error"].hidden, true);

// Guard the single-file page's client-only privacy contract against accidental APIs.
const source = fs.readFileSync(path.join(__dirname, "private_calculator.js"), "utf8");
for (const forbidden of [
  /\bfetch\s*\(/i,
  /\bXMLHttpRequest\b/i,
  /\bWebSocket\b/i,
  /\bEventSource\b/i,
  /\bsendBeacon\b/i,
  /\blocalStorage\b/i,
  /\bsessionStorage\b/i,
  /\bindexedDB\b/i,
  /document\s*\.\s*cookie/i,
  /serviceWorker/i,
  /\bWorker\s*\(/i
]) {
  assert.doesNotMatch(source, forbidden);
}

console.log("PASS: private calculator arithmetic, edge cases, and no-network/no-persistence source guard.");
