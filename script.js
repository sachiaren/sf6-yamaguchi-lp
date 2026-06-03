// キービジュアル画像が読み込めないとき、代替表示へ切り替えます。
const posterImage = document.getElementById("eventPoster");

if (posterImage) {
  posterImage.addEventListener("error", () => {
    posterImage.closest(".hero__poster")?.classList.add("is-missing");
  });
}

// 申込締切までの日数を表示します。日付を変える場合はここを編集してください。
const deadlineStatus = document.getElementById("deadlineStatus");
const entryDeadline = new Date("2026-07-01T23:59:59+09:00");
const today = new Date();

if (deadlineStatus) {
  const diff = entryDeadline.getTime() - today.getTime();
  const daysLeft = Math.ceil(diff / (1000 * 60 * 60 * 24));

  if (daysLeft > 0) {
    deadlineStatus.textContent = `申込締切まであと${daysLeft}日`;
  } else if (daysLeft === 0) {
    deadlineStatus.textContent = "申込締切は本日まで";
  } else {
    deadlineStatus.textContent = "申込期間は終了しました";
  }
}

// ページ内リンクの移動を少しだけ滑らかにします。
document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener("click", (event) => {
    const target = document.querySelector(link.getAttribute("href"));

    if (!target) return;

    event.preventDefault();
    target.scrollIntoView({ behavior: "smooth", block: "start" });
  });
});
