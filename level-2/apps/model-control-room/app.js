const API = window.GFIS_API_BASE || "http://127.0.0.1:8010";
const docsLink = document.getElementById("apiDocsLink");
if (docsLink) docsLink.href = `${API}/docs`;

const specs = [
  ["temperature", "Temperature", 25, 45, 37, "C"],
  ["pH", "pH", 6, 8.5, 7.1, ""],
  ["OLR", "OLR", 1, 6.5, 3.2, "kg VS/m3d"],
  ["HRT", "HRT", 10, 45, 25, "days"],
  ["TS", "TS", 4, 16, 9, "%"],
  ["VS", "VS", 2.5, 13, 6.8, "%"],
  ["C_N_ratio", "C/N", 12, 38, 25, ""],
  ["ambient_temperature", "Ambient", 15, 40, 28, "C"],
  ["moisture", "Moisture", 65, 95, 82, "%"]
];

const controls = document.getElementById("controls");
const state = {};

function initControls() {
  specs.forEach(([key, label, min, max, value, unit]) => {
    state[key] = value;
    const wrapper = document.createElement("div");
    wrapper.className = "control";
    wrapper.innerHTML = `
      <label><span>${label}</span><strong id="${key}Value">${value} ${unit}</strong></label>
      <input id="${key}" type="range" min="${min}" max="${max}" value="${value}" step="0.1" />
    `;
    controls.appendChild(wrapper);
    wrapper.querySelector("input").addEventListener("input", (event) => {
      state[key] = Number(event.target.value);
      document.getElementById(`${key}Value`).textContent = `${state[key]} ${unit}`;
      predict();
    });
  });
}

async function api(path, options = {}) {
  const response = await fetch(`${API}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options
  });
  if (!response.ok) throw new Error(`${path} failed`);
  return response.json();
}

async function checkApi() {
  const pill = document.getElementById("apiStatus");
  try {
    await api("/health");
    pill.textContent = "API Online";
    pill.className = "status-pill ok";
  } catch {
    pill.textContent = "API Offline";
    pill.className = "status-pill fail";
  }
}

function setStability(label) {
  const badge = document.getElementById("stabilityBadge");
  badge.textContent = label;
  badge.style.color = label === "Stable" ? "var(--green)" : label === "Warning" ? "var(--amber)" : "var(--red)";
}

async function predict() {
  try {
    const result = await api("/predict", { method: "POST", body: JSON.stringify(state) });
    document.getElementById("methaneMetric").textContent = result.methane_yield.toFixed(2);
    document.getElementById("boundMetric").textContent = result.physics_upper_bound.toFixed(2);
    document.getElementById("vfaMetric").textContent = result.vfa_alk_ratio.toFixed(3);
    document.getElementById("violationMetric").textContent = result.physics_violation ? "Yes" : "No";
    setStability(result.stability_label);
  } catch (error) {
    document.getElementById("methaneMetric").textContent = "API down";
  }
}

async function simulate() {
  const scenarios = [2.0, 2.6, 3.2, 3.8, 4.4, 5.0].map((OLR) => ({ OLR }));
  const outputs = await api("/simulate", {
    method: "POST",
    body: JSON.stringify({ base: state, scenarios })
  });
  drawChart(outputs);
}

async function plantTrace() {
  const outputs = await api("/plant-run?hours=48", {
    method: "POST",
    body: JSON.stringify(state)
  });
  drawChart(outputs.filter((_, index) => index % 6 === 0).map((item) => ({
    OLR: `${item.hour}h`,
    methane_yield: item.methane_yield
  })));
}

function drawChart(outputs) {
  const chart = document.getElementById("chart");
  chart.innerHTML = "";
  const max = Math.max(...outputs.map((item) => item.methane_yield), 1);
  outputs.forEach((item) => {
    const bar = document.createElement("div");
    bar.className = "bar";
    bar.style.height = `${Math.max(8, (item.methane_yield / max) * 230)}px`;
    bar.title = `OLR ${item.OLR}: ${item.methane_yield}`;
    bar.innerHTML = `<span>${item.OLR}</span>`;
    chart.appendChild(bar);
  });
}

async function optimize() {
  const result = await api("/optimize", { method: "POST", body: JSON.stringify(state) });
  ["temperature", "pH", "OLR"].forEach((key) => {
    if (result[key] !== undefined) {
      state[key] = result[key];
      const input = document.getElementById(key);
      input.value = result[key];
      input.dispatchEvent(new Event("input"));
    }
  });
}

async function loadEvaluation() {
  try {
    const result = await api("/evaluate");
    document.getElementById("evaluationBox").textContent = JSON.stringify(result, null, 2);
  } catch {
    document.getElementById("evaluationBox").textContent = "Evaluation API unavailable.";
  }
}

document.getElementById("runSimulation").addEventListener("click", simulate);
document.getElementById("runPlantTrace").addEventListener("click", plantTrace);
document.getElementById("optimize").addEventListener("click", optimize);

initControls();
checkApi();
predict();
simulate();
loadEvaluation();
