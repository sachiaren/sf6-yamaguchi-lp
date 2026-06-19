// キービジュアル画像が読み込めないとき、代替表示へ切り替えます。
const posterImage = document.getElementById("eventPoster");

if (posterImage) {
  posterImage.addEventListener("error", () => {
    posterImage.closest(".hero__poster")?.classList.add("is-missing");
  });
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
