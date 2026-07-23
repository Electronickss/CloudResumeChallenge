const API_URL = "YOUR_API_GATEWAY_URL";

async function fetchVisitorCount() {
  const counterEl = document.getElementById("visitor-count");
  try {
    const response = await fetch(API_URL);
    const data = await response.json();
    counterEl.textContent = data.count;
  } catch (err) {
    counterEl.textContent = "—";
  }
}

document.addEventListener("DOMContentLoaded", fetchVisitorCount);
