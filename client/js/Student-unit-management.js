
function showNotification(message, type = "info", duration = 3000) {
  let notif = document.getElementById("globalNotification");

  if (!notif) {
    notif = document.createElement("div");
    notif.id = "globalNotification";
    notif.className = "notification hidden";
    document.body.appendChild(notif);
  }

  notif.textContent = message;
  notif.className = `notification ${type}`;

  setTimeout(() => {
    notif.classList.add("hidden");
  }, duration);
}

const KEY = "ces_unit_settings";

document.addEventListener("DOMContentLoaded", () => {
  const minUnits = document.getElementById("minUnits");
  const maxUnits = document.getElementById("maxUnits");
  const saveBtn = document.getElementById("saveBtn");
  const resetBtn = document.getElementById("resetBtn");

  function loadSettings() {
    const data = JSON.parse(localStorage.getItem(KEY)) || {
      min: 12,
      max: 20
    };
    minUnits.value = data.min;
    maxUnits.value = data.max;
  }

  saveBtn.addEventListener("click", () => {
    const min = Number(minUnits.value);
    const max = Number(maxUnits.value);

    if (min < 0 || max < 0 || min > max) {
      showNotification("Invalid unit range", "error");
      return;
    }

    localStorage.setItem(KEY, JSON.stringify({ min, max }));
    showNotification("Unit settings saved successfully", "success");
  });

  resetBtn.addEventListener("click", () => {
    localStorage.removeItem(KEY);
    loadSettings();
    showNotification("Settings reset to default", "info");
  });

  loadSettings();
});
