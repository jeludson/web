// LOADER
window.addEventListener("load", () => {
  document.querySelector(".loader").style.display = "none";
});

// THEME
function toggleTheme() {
  document.body.classList.toggle("light");
}
document.querySelectorAll(".contact-card").forEach(card => {
  card.addEventListener("click", () => {
    card.style.transform = "scale(0.95)";
    setTimeout(() => {
      card.style.transform = "";
    }, 150);
  });
});
