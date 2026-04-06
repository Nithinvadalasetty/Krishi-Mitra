const form = document.getElementById("analyze-form");
const resultBox = document.getElementById("analysis-result");
const btn = document.getElementById("analyze-btn");
const preview = document.getElementById("preview-img");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  btn.disabled = true;
  btn.innerText = "Analyzing...";

  const data = new FormData(form);
  const img = data.get("image");

  preview.src = URL.createObjectURL(img);
  preview.style.display = "block";

  const res = await fetch("/analyze", {
    method: "POST",
    body: data
  });

  const r = await res.json();

  resultBox.innerHTML = `
    <b>Crop:</b> ${r.crop}<br>
    <b>Disease:</b> ${r.disease}<br>
    <b>Confidence:</b> ${r.confidence}%<br>
    <b>Health:</b> ${r.health}<br>
    <b>Cause:</b> ${r.cause}<br><br>
    <b>Recommended Actions:</b>
    <ul>${r.actions.map(a => `<li>${a}</li>`).join("")}</ul>
  `;

  btn.disabled = false;
  btn.innerText = "🔍 Analyze Crop";
});

async function sendChat() {
  const input = document.getElementById("chat-input");
  const msg = input.value.trim();
  if (!msg) return;

  input.value = "";

  const chat = document.getElementById("chat-box");
  chat.innerHTML += `<div class="chat-msg user">You: ${msg}</div>`;

  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: msg })
  });

  const r = await res.json();
  chat.innerHTML += `<div class="chat-msg bot">Krishi: ${r.reply}</div>`;
  chat.scrollTop = chat.scrollHeight;
}