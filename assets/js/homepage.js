// Enhance the theme's existing menu without replacing its layout or theme controls.
// The in-page navigation remains available when JavaScript is disabled.
function initHomepageNavigation() {
  const source = document.querySelector("[data-homepage-navigation]");
  const menu = document.querySelector("#navbarNav .navbar-menu-list");
  if (!source || !menu) return;

  const themeControl = menu.querySelector(".toggle-container");
  source.querySelectorAll("a").forEach((link) => {
    const item = document.createElement("li");
    item.className = "nav-item";
    const navLink = link.cloneNode(true);
    navLink.className = "nav-link";
    item.append(navLink);
    menu.insertBefore(item, themeControl);
  });
  source.hidden = true;

  menu.addEventListener("click", (event) => {
    const link = event.target.closest("a[href^='#']");
    const toggle = document.querySelector('[data-nav-toggle="navbarNav"]');
    if (link && toggle?.getAttribute("aria-expanded") === "true") toggle.click();
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initHomepageNavigation, { once: true });
} else {
  initHomepageNavigation();
}
