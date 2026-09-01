(function () {
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  const header = $(".app-header");
  const menuBtn = $("#menu-toggle");
  const sidebar = $("#sidebar");
  const scrim = $("#scrim");
  const searchToggle = $("#search-toggle");
  const searchInputs = $$("#site-search, #site-search-mobile");
  const resultBoxes = $$("#search-results, #search-results-mobile");

  const setNav = (open) => {
    if (!sidebar) return;
    sidebar.classList.toggle("open", open);
    if (scrim) scrim.classList.toggle("on", open);
    document.body.classList.toggle("nav-open", open);
    if (menuBtn) menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
  };

  if (menuBtn && sidebar) {
    menuBtn.addEventListener("click", () => setNav(!sidebar.classList.contains("open")));
  }
  if (scrim) scrim.addEventListener("click", () => setNav(false));
  $("#sidebar-close")?.addEventListener("click", () => setNav(false));
  $$(".sidebar a").forEach((a) => a.addEventListener("click", () => setNav(false)));

  if (searchToggle && header) {
    searchToggle.addEventListener("click", () => {
      header.classList.toggle("search-open");
      if (header.classList.contains("search-open")) {
        setTimeout(() => $("#site-search-mobile")?.focus(), 20);
      }
    });
  }

  $$(".sidebar a").forEach((a) => {
    const here = decodeURIComponent(location.pathname.split("/").pop() || "index.html");
    const href = (a.getAttribute("href") || "").split("/").pop();
    if (href === here) a.classList.add("active");
  });

  $$(".lesson").forEach((lesson) => {
    const head = $(".lesson-head", lesson);
    const box = $("input[type=checkbox]", lesson);
    if (head) {
      head.addEventListener("click", (e) => {
        if (e.target.closest(".taught")) return;
        lesson.classList.toggle("open");
      });
    }
    if (box) {
      const key = "taught:" + lesson.id;
      box.checked = localStorage.getItem(key) === "1";
      box.addEventListener("change", () => {
        localStorage.setItem(key, box.checked ? "1" : "0");
      });
    }
  });

  const buttons = $$("[data-timeline]");
  const applyTimeline = (key) => {
    buttons.forEach((b) => b.classList.toggle("on", b.dataset.timeline === key));
    $$(".lesson").forEach((lesson) => {
      const tags = (lesson.dataset.timelines || "6m").split(/\s+/);
      lesson.classList.toggle("hidden", key !== "all" && !tags.includes(key));
    });
    localStorage.setItem("timeline:" + location.pathname, key);
  };
  if (buttons.length) {
    applyTimeline(localStorage.getItem("timeline:" + location.pathname) || "3m");
    buttons.forEach((b) => b.addEventListener("click", () => applyTimeline(b.dataset.timeline)));
  }

  $("#open-all")?.addEventListener("click", () => $$(".lesson:not(.hidden)").forEach((l) => l.classList.add("open")));
  $("#close-all")?.addEventListener("click", () => $$(".lesson").forEach((l) => l.classList.remove("open")));
  $("#print-page")?.addEventListener("click", () => {
    $$(".lesson").forEach((l) => l.classList.add("open"));
    window.print();
  });

  const index = window.SEARCH_INDEX || [];
  let active = -1;
  const renderResults = (q) => {
    const query = q.trim().toLowerCase();
    if (query.length < 2) {
      resultBoxes.forEach((box) => {
        box.classList.remove("open");
        box.innerHTML = "";
      });
      return;
    }
    const hits = index.filter((item) =>
      (item.title + " " + item.hay + " " + item.group).toLowerCase().includes(query)
    ).slice(0, 12);
    const html = hits.length
      ? hits.map((h, i) => `<a href="${h.href}" data-i="${i}"><strong>${h.title}</strong><small>${h.group}</small></a>`).join("")
      : `<a>No matches for “${q}”</a>`;
    resultBoxes.forEach((box) => {
      box.innerHTML = html;
      box.classList.add("open");
    });
    active = -1;
  };

  searchInputs.forEach((input) => {
    input.addEventListener("input", () => renderResults(input.value));
    input.addEventListener("keydown", (e) => {
      const links = $$(".search-results.open a");
      if (e.key === "ArrowDown") {
        e.preventDefault();
        active = Math.min(active + 1, links.length - 1);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        active = Math.max(active - 1, 0);
      } else if (e.key === "Enter" && links[active]) {
        location.href = links[active].href;
      } else if (e.key === "Escape") {
        resultBoxes.forEach((box) => box.classList.remove("open"));
        header?.classList.remove("search-open");
      }
      links.forEach((a, i) => a.classList.toggle("active", i === active));
    });
  });
  document.addEventListener("click", (e) => {
    if (!e.target.closest(".search-wrap") && !e.target.closest("#search-toggle")) {
      resultBoxes.forEach((box) => box.classList.remove("open"));
    }
  });
})();
