const API_URL = "https://n7v42sywek.execute-api.us-east-1.amazonaws.com/count";

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
