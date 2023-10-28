function showHamburgerMenu() {
  let x = document.getElementById("mobileLinks");
  if (x.style.display === "flex") {
    x.style.display = "none";
  } else {
    x.style.display = "flex";
  }
}

console.log("Who needs a front-end framework?")