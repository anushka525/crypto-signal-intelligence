const output = document.getElementById("output");
const statusBadge = document.getElementById("statusBadge");
const signalCount = document.getElementById("signalCount");
const assetCount = document.getElementById("assetCount");

async function apiRequest(path, method, body) {
  const options = {
    method,
    headers: { "Content-Type": "application/json" }  // This tells the server, "Hey, I'm sending you a JSON package, please parse it as such."
  };
  if (body) {
    options.body = JSON.stringify(body); // This line takes the JavaScript object you created (the "body") and turns it into a JSON string, which is the format that the backend API expects to receive. It's like translating your data into a language that the server can understand.
  }
  const response = await fetch(path, options);
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || data.message || "Request failed");
  }
  return data;
}

function showOutput(payload) {
  output.textContent = JSON.stringify(payload, null, 2);
}

function setStatus(ok) {
  statusBadge.textContent = ok ? "API Ready" : "API Error";
  statusBadge.className = ok ? "value ok" : "value";
}

async function refreshLists() {
  try {
    const [assets, signals] = await Promise.all([
      apiRequest("/api/assets/", "GET"),
      apiRequest("/api/signals/", "GET")
    ]);
    assetCount.textContent = assets.length;
    signalCount.textContent = signals.length;

    setStatus(true);
  } catch (err) {
    setStatus(false);
    showOutput({ error: err.message });
  }
}

function formToObject(form) {
  const formData = new FormData(form);
  const data = {};
  for (const [key, value] of formData.entries()) {
    if (value === "") {
      continue;
    }
    const numeric = Number(value);  // The cursor checks if the input is a number. It converts "1" into an actual integer 1 so the backend database can recognize it as a primary key
    data[key] = Number.isNaN(numeric) ? value : numeric; 
    /*
    This uses a ternary operator (a shorthand if/else) to decide what to actually store in your data object.
    The Check: Number.isNaN(numeric) asks: "Did the conversion above fail?"
    The Result (True): If it is NaN (meaning the input was text like "hello"), it keeps the original value.
    The Result (False): If it is a valid number, it saves the new numeric version.
    */
  }
  return data;
}

function bindForm(formId, path) {
  const form = document.getElementById(formId);
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      const payload = formToObject(form);
      const response = await apiRequest(path, "POST", payload);
      showOutput(response);
      await refreshLists();
      form.reset();
    } catch (err) {
      showOutput({ error: err.message });
    }
  });
}

function bindAiForm() {
  const form = document.getElementById("aiForm");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      const payload = formToObject(form);
      const market = {
        last_price: payload.last_price,
        rsi: payload.rsi,
        macd: payload.macd,
        volatility: payload.volatility
      };
      delete payload.last_price;
      delete payload.rsi;
      delete payload.macd;
      delete payload.volatility;
      payload.market = market;

      const response = await apiRequest("/api/ai/summary", "POST", payload);
      showOutput(response);
    } catch (err) {
      showOutput({ error: err.message });
    }
  });
}

bindForm("assetForm", "/api/assets/");
bindAiForm();

const autoSignalForm = document.getElementById("autoSignalForm");
autoSignalForm.addEventListener("submit", async (event) => {
  event.preventDefault();  // This is a crucial "Stop" command. The cursor tells the browser, "Do not refresh the page like a normal website; I will handle this with JavaScript
  try {
    const payload = formToObject(autoSignalForm);  // it scrapes the asset_id and timeframe from the HTML input fields.
    const response = await apiRequest("/api/signals/auto", "POST", payload);
    showOutput(response);
    await refreshLists();
    autoSignalForm.reset();
  } catch (err) {
    showOutput({ error: err.message });
  }
});

const refreshAll = document.getElementById("refreshAll");
refreshAll.addEventListener("click", refreshLists);

document.getElementById("clearOutput").addEventListener("click", () => {
  output.textContent = "Ready.";
});

refreshLists();
