const STORAGE_KEY = "skala-planner";
const THEME_KEY = "skala-theme";

let goals = [];
let filter = "all";

const savedTheme = localStorage.getItem(THEME_KEY);
const systemPrefersDark = window.matchMedia(
  "(prefers-color-scheme: dark)"
).matches;

// Element Selectors
const form = document.getElementById("goal-form");
const input = document.getElementById("goal-input");
const category = document.getElementById("goal-category");
const dueday = document.getElementById("goal-due");
const searchInput = document.getElementById("search-input");
const themeToggle = document.getElementById("theme-toggle");
const listEl = document.getElementById("goal-list");
const emptyEl = document.getElementById("list-empty");
const errorEl = document.getElementById("form-error");
const tabsEl = document.getElementById("filter-tabs");
const fillEl = document.getElementById("progress-fill");
const textEl = document.getElementById("progress-text");
const restEl = document.getElementById("rest-text");

function load() {
  const saved = localStorage.getItem(STORAGE_KEY);
  return saved ? JSON.parse(saved) : [];
}

function save() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(goals));
}

function visible() {
  if (filter === "active") return goals.filter((g) => !g.done);
  if (filter === "done") return goals.filter((g) => g.done);
  return goals;
}

function GetCurrentDate() {
  return new Date().toLocaleDateString("ko-KR", { dateStyle: "long" });
}

function searchForId(id) {
  return goals.find((g) => g.id === id);
}

function searchFor(text) {
  if (text === "") {
    render();
    return;
  }
  const list = goals.filter((g) => g.title.includes(text));
  render(list);
}

function escapeHtml(value) {
  // 입력값이 없거나 문자열이 아닌 경우 예외 처리
  if (!value) return "";

  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function getDDay(targetDateStr) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const [year, month, day] = targetDateStr.split("-").map(Number);
  const targetDate = new Date(year, month - 1, day); // 월(month)은 0부터 시작하므로 -1

  const diffTime = targetDate - today;
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

  if (diffDays > 0) {
    return `D-${diffDays}`;
  } else if (diffDays === 0) {
    return "D-Day";
  } else {
    return `D+${Math.abs(diffDays)}`;
  }
}

function applyTheme(theme) {
  const isDark = theme === "dark";
  document.body.classList.toggle("dark", isDark);
  themeToggle.textContent = isDark ? "☀️" : "🌙";
  themeToggle.setAttribute(
    "aria-label",
    isDark ? "라이트 모드로 전환" : "다크 모드로 전환"
  );
}

function updateProgress() {
  const total = goals.length;
  const done = goals.filter((g) => g.done).length;
  const percent = total === 0 ? 0 : Math.round((done / total) * 100);

  const rest = goals
    .filter((g) => !g.done)
    .reduce((acc, g) => {
      acc[g.category] = (acc[g.category] || 0) + 1;
      return acc;
    }, {});

  fillEl.style.width = percent + "%";
  textEl.textContent = `전체 ${total}개 중 ${done}개 완료 (${percent}%)`;
  restEl.textContent = `
  남은 HTML 목록: ${rest.HTML == undefined ? 0 : rest.HTML} /
  남은 JS 목록: ${rest.JS == undefined ? 0 : rest.JS} /
  남은 CSS 목록: ${rest.CSS == undefined ? 0 : rest.CSS}
  `;
}

function createGoalItem(goal) {
  const li = document.createElement("li");
  li.className = goal.done ? "item is-done" : "item";
  li.dataset.id = goal.id;

  li.innerHTML = `
    <input type="checkbox" class="item-check" ${goal.done ? "checked" : ""} />
    <span class="item-text">${escapeHtml(goal.title)}</span>
    <div class="item-tags">
      <span class="badge">${goal.category}</span>
      <span class="d-day">${getDDay(goal.due)}</span>
      <span class="item-date">${goal.due}</span>
    </div>
    <button type="button" class="item-del">x</button>
  `;

  return li;
}

function removeGoalItem(li) {
  const rect = li.getBoundingClientRect();
  const clone = li.cloneNode(true);

  Object.assign(clone.style, {
    position: "fixed",
    top: `${rect.top}px`,
    left: `${rect.left}px`,
    width: `${rect.width}px`,
    height: `${rect.height}px`,
    margin: "0",
    zIndex: "100",
    pointerEvents: "none",
    background: "#fff",
  });

  clone.classList.add("item--leaving");
  document.body.appendChild(clone);

  li.remove();

  clone.addEventListener("animationend", () => clone.remove(), { once: true });
}

function render(items = visible(), {addedId, removedId} = {}) {
  const currentItems = new Map(
    [...listEl.children].map((li) => [Number(li.dataset.id), li])
  );
  const visibleIds = new Set(items.map((goal) => goal.id));

  // 현재 화면에서 사라져야 하는 항목만 제거
  currentItems.forEach((li, id) => {
    if (visibleIds.has(id)) return;

    if (id === removedId) {
      li.classList.add("item--leaving");
      li.addEventListener("animationend", () => li.remove(), { once: true });
    } else {
      li.remove(); // 필터, 검색 전환은 즉시 처리
    }
  });

  // 기존 DOM은 재사용, 새 항목만 생성
  items.forEach((goal) => {
    let li = currentItems.get(goal.id);

    if (!li) {
      li = createGoalItem(goal);

      if (goal.id === addedId) {
        li.classList.add("item--entering");
      }
    } else {
      li.classList.toggle("is-done", goal.done);
      li.querySelector(".item-check").checked = goal.done;
    }

    // 새 요소만 삽입된다.
    listEl.appendChild(li);
  });

  emptyEl.hidden = items.length > 0;
  updateProgress();
}

async function loadTip() {
  const tipEl = document.getElementById("tip");
  try {
    const res = await fetch("data/tips.json");
    if (!res.ok) throw new Error("HTTP " + res.status);
    const tips = await res.json();
    const today = new Date().getDate() % tips.length;
    tipEl.textContent = tips[today];
    return true;
  } catch (error) {
    tipEl.textContent = "팁을 불러오지 못했습니다.";
  }
}

// Event Listener
form.addEventListener("submit", (event) => {
  event.preventDefault();
  const title = input.value.trim();
  const dday = dueday.value;
  if (title === "") {
    errorEl.textContent = "목표를 한 글자 이상 입력해 주세요.";
    errorEl.hidden = false;
    input.focus();
    return;
  }
  if (!dday) {
    errorEl.textContent = "목표일을 설정해주세요.";
    errorEl.hidden = false;
    dueday.focus();
    return;
  }
  errorEl.hidden = true;
  
  const newGoal = {
    id: Date.now(),
    title: title,
    category: category.value,
    done: false,
    due: dueday.value,
  };

  goals.push(newGoal);
  input.value = "";
  save();
  render(visible(), { addedId: newGoal.id });
});

listEl.addEventListener("click", (event) => {
  const li = event.target.closest(".item");
  if (!li) return;
  const id = Number(li.dataset.id);
  if (event.target.matches(".item-check")) {
    const goal = goals.find((g) => g.id === id);
    goal.done = event.target.checked;
    save();
    render();
  }
  if (event.target.matches(".item-del")) {
    removeGoalItem(li);

    goals = goals.filter((g) => g.id !== id);
    save();
    render();
  }
});

input.addEventListener("keydown", (event) => {
  if (event.key == "Escape") input.value = "";
});

tabsEl.addEventListener("click", (e) => {
  const tab = e.target.closest(".tab");
  if (!tab) return;
  filter = tab.dataset.filter;

  document.querySelectorAll(".tab").forEach((t) => {
    t.classList.toggle("is-active", t === tab);
  });
  render();
});

searchInput.addEventListener("input", (e) => {
  searchFor(e.target.value);
});

searchInput.addEventListener("keydown", (event) => {
  if (event.key == "Escape") {
    searchInput.value = "";
    render();
  }
});

themeToggle.addEventListener("click", () => {
  const nextTheme = document.body.classList.contains("dark")
    ? "light"
    : "dark";

  localStorage.setItem(THEME_KEY, nextTheme);
  applyTheme(nextTheme);
});

// Page load.
document.addEventListener("DOMContentLoaded", () => {
  applyTheme(savedTheme ?? (systemPrefersDark ? "dark" : "light"));
  goals = load();
  render();

  const todayEl = document.getElementById("today");
  if (todayEl) todayEl.textContent = GetCurrentDate();

  loadTip();
});
