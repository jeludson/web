// Small click feedback
document.querySelector("button").addEventListener("click", () => {
  document.querySelector(".login-card").style.transform = "scale(0.98)";
  setTimeout(() => {
    document.querySelector(".login-card").style.transform = "scale(1)";
  }, 150);
});
