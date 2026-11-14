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

// This is a display preference, not authentication. Keep the image request active
// for visitor counting even while the map is hidden.
function initHomepageVisitors() {
  const visitors = document.querySelector(".home-visitors");
  if (!visitors) return;

  const preference = new URLSearchParams(window.location.search).get("stats");
  const storageKey = "homepage-show-stats";
  let showStats = preference === "on";

  try {
    if (preference === "on" || preference === "off") {
      window.localStorage.setItem(storageKey, preference);
    } else {
      showStats = window.localStorage.getItem(storageKey) === "on";
    }
  } catch {
    // The URL switch still works when browser storage is unavailable.
  }

  const image = visitors.querySelector("img");
  visitors.hidden = !showStats || (image.complete && image.naturalWidth === 0);
}

function initHomepage() {
  initHomepageNavigation();
  initHomepageVisitors();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initHomepage, { once: true });
} else {
  initHomepage();
}
