/*
 * Private browser calculator. This file is embedded inline in private-calculator.html
 * by scripts/build_canonical.py so the blank page can be saved and used offline.
 * No network APIs, browser storage, cookies, or form submission are used.
 */
(function (factory) {
  "use strict";
  var api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  }
  if (typeof document !== "undefined") {
    api.init(document);
  }
})(function () {
  "use strict";

  var FIELD_IDS = [
    "horizon-years",
    "discount-rate",
    "sale-gross",
    "sale-costs",
    "sale-transfer",
    "sale-debt",
    "sale-tax",
    "sale-other",
    "hold-annual-net",
    "hold-terminal-net",
    "renew-annual-net",
    "renew-terminal-net"
  ];

  var FIELD_LABELS = {
    "horizon-years": "Comparison horizon",
    "discount-rate": "Required return / discount rate",
    "sale-gross": "Current written sale price",
    "sale-costs": "Current transaction costs",
    "sale-transfer": "Current transfer taxes",
    "sale-debt": "Current debt and lien payoff",
    "sale-tax": "Current CPA-estimated income taxes",
    "sale-other": "Other current sale costs",
    "hold-annual-net": "Hold annual after-tax cash flow",
    "hold-terminal-net": "Hold terminal after-tax proceeds",
    "renew-annual-net": "Renewal annual after-tax cash flow",
    "renew-terminal-net": "Renewal terminal after-tax proceeds"
  };

  function isFiniteNumber(value) {
    return typeof value === "number" && Number.isFinite(value);
  }

  function annuityFactor(rate, years) {
    if (!isFiniteNumber(rate) || rate < 0) {
      throw new RangeError("Discount rate must be a finite nonnegative rate.");
    }
    if (!Number.isSafeInteger(years) || years < 1) {
      throw new RangeError("Comparison horizon must be a positive whole number.");
    }
    if (rate === 0) return years;
    return (1 - Math.pow(1 + rate, -years)) / rate;
  }

  function presentValue(levelAnnualCashFlow, terminalNetProceeds, rate, years) {
    if (!isFiniteNumber(levelAnnualCashFlow) || !isFiniteNumber(terminalNetProceeds)) {
      throw new TypeError("Cash-flow and terminal-proceeds inputs must be finite numbers.");
    }
    var factor = annuityFactor(rate, years);
    return levelAnnualCashFlow * factor + terminalNetProceeds / Math.pow(1 + rate, years);
  }

  function netSaleProceeds(sale) {
    var keys = ["grossPrice", "transactionCosts", "transferTaxes", "debtPayoff", "incomeTaxes", "otherCosts"];
    keys.forEach(function (key) {
      if (!isFiniteNumber(sale[key])) {
        throw new TypeError("Sale input " + key + " must be a finite number.");
      }
    });
    return sale.grossPrice - sale.transactionCosts - sale.transferTaxes - sale.debtPayoff - sale.incomeTaxes - sale.otherCosts;
  }

  function compare(input) {
    if (!input || !isFiniteNumber(input.years) || !isFiniteNumber(input.discountRatePct)) {
      throw new TypeError("Horizon and discount rate are required.");
    }
    var rate = input.discountRatePct / 100;
    var saleNow = netSaleProceeds(input.sale);
    var holdValue = presentValue(input.hold.annualNetCashFlow, input.hold.terminalNetProceeds, rate, input.years);
    var renewalValue = presentValue(input.renewal.annualNetCashFlow, input.renewal.terminalNetProceeds, rate, input.years);
    var values = [saleNow, holdValue, renewalValue];
    if (!values.every(isFiniteNumber)) {
      throw new RangeError("The entered values exceed the calculator's supported numeric range.");
    }
    return {
      saleNow: saleNow,
      holdPresentValue: holdValue,
      renewalPresentValue: renewalValue,
      holdDifferenceVsSale: holdValue - saleNow,
      renewalDifferenceVsSale: renewalValue - saleNow,
      annuityFactor: annuityFactor(rate, input.years)
    };
  }

  function readInputs(doc) {
    var raw = {};
    var missing = [];
    FIELD_IDS.forEach(function (id) {
      var element = doc.getElementById(id);
      var text = element && typeof element.value === "string" ? element.value.trim() : "";
      if (text === "") {
        missing.push(FIELD_LABELS[id]);
      } else {
        raw[id] = Number(text);
      }
    });
    if (missing.length) {
      return { error: "Complete every input before calculating. Enter 0 when a documented amount is zero; do not invent a missing value. Missing: " + missing.join(", ") + "." };
    }
    if (!Object.keys(raw).every(function (id) { return isFiniteNumber(raw[id]); })) {
      return { error: "Use finite numeric values only. Leave no field blank; enter 0 only when the verified amount is zero." };
    }
    if (!Number.isSafeInteger(raw["horizon-years"]) || raw["horizon-years"] < 1) {
      return { error: "The comparison horizon must be a positive whole number." };
    }
    if (raw["discount-rate"] < 0) {
      return { error: "The required return must be a nonnegative finite percentage. This is an owner/adviser assumption, not a market forecast." };
    }
    ["sale-gross", "sale-costs", "sale-transfer", "sale-debt", "sale-tax", "sale-other"].forEach(function (id) {
      if (raw[id] < 0) missing.push(FIELD_LABELS[id] + " (must not be negative)");
    });
    if (missing.length) {
      return { error: "Check these inputs: " + missing.join(", ") + "." };
    }
    return {
      value: {
        years: raw["horizon-years"],
        discountRatePct: raw["discount-rate"],
        sale: {
          grossPrice: raw["sale-gross"],
          transactionCosts: raw["sale-costs"],
          transferTaxes: raw["sale-transfer"],
          debtPayoff: raw["sale-debt"],
          incomeTaxes: raw["sale-tax"],
          otherCosts: raw["sale-other"]
        },
        hold: {
          annualNetCashFlow: raw["hold-annual-net"],
          terminalNetProceeds: raw["hold-terminal-net"]
        },
        renewal: {
          annualNetCashFlow: raw["renew-annual-net"],
          terminalNetProceeds: raw["renew-terminal-net"]
        }
      }
    };
  }

  function init(doc) {
    var calculateButton = doc.getElementById("calculate-button");
    var clearButton = doc.getElementById("clear-button");
    var errorBox = doc.getElementById("calculator-error");
    var results = doc.getElementById("calculator-results");
    if (!calculateButton || !clearButton || !errorBox || !results) return;

    function showError(message) {
      errorBox.textContent = message;
      errorBox.hidden = !message;
    }

    function clearResults() {
      ["result-sale", "result-hold", "result-renew", "result-hold-gap", "result-renew-gap"].forEach(function (id) {
        doc.getElementById(id).textContent = "—";
      });
      results.hidden = true;
    }

    calculateButton.addEventListener("click", function () {
      showError("");
      var parsed = readInputs(doc);
      if (parsed.error) {
        clearResults();
        showError(parsed.error);
        return;
      }
      var result;
      try {
        result = compare(parsed.value);
      } catch (error) {
        clearResults();
        showError(error && error.message ? error.message : "The entered values could not be calculated.");
        return;
      }
      var money = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 2 });
      doc.getElementById("result-sale").textContent = money.format(result.saleNow);
      doc.getElementById("result-hold").textContent = money.format(result.holdPresentValue);
      doc.getElementById("result-renew").textContent = money.format(result.renewalPresentValue);
      doc.getElementById("result-hold-gap").textContent = money.format(result.holdDifferenceVsSale);
      doc.getElementById("result-renew-gap").textContent = money.format(result.renewalDifferenceVsSale);
      results.hidden = false;
    });

    clearButton.addEventListener("click", function () {
      FIELD_IDS.forEach(function (id) {
        var element = doc.getElementById(id);
        if (element) element.value = "";
      });
      showError("");
      clearResults();
    });
  }

  return Object.freeze({
    FIELD_IDS: Object.freeze(FIELD_IDS.slice()),
    annuityFactor: annuityFactor,
    presentValue: presentValue,
    netSaleProceeds: netSaleProceeds,
    compare: compare,
    init: init
  });
});
