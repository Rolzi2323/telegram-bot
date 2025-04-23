Telegram.WebApp.ready();

document.getElementById("buyButton").addEventListener("click", () => {
  const initData = Telegram.WebApp.initData;

  fetch("https://your-server.com/buy-stars", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ initData })
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        alert("✅ Покупка успешна!");
        Telegram.WebApp.close();
      } else {
        alert("❌ Ошибка при покупке.");
      }
    });
});

