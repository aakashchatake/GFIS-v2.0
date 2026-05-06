async function loadManifest() {
  const table = document.querySelector("#libraryRows");
  const docList = document.querySelector("#docList");
  if (!table) return;

  try {
    const response = await fetch("data/portal_manifest.json");
    const manifest = await response.json();

    table.innerHTML = "";
    if (docList) docList.innerHTML = "";
    manifest.library.forEach((item) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${item.href ? `<a href="${item.href}" target="_blank" rel="noopener">${item.title}</a>` : item.title}</td>
        <td>${item.type}</td>
        <td>${item.status}</td>
      `;
      table.appendChild(row);

      if (docList && item.href && item.href.endsWith(".pdf")) {
        const button = document.createElement("button");
        button.type = "button";
        button.textContent = item.title;
        button.addEventListener("click", () => {
          document.querySelector("#docFrame").src = item.href;
        });
        docList.appendChild(button);
      }
    });
  } catch (error) {
    table.innerHTML = "<tr><td colspan=\"3\">Manifest loads when served through a local or production web server.</td></tr>";
  }
}

loadManifest();

const DEFAULT_USERS = [
  {
    displayName: "GreenWorks Admin",
    emailHash: "2d2d0b76116dfad6e266d6c961a8da62d1a7de16f14380ce7de4b0cc5ddd9b8f",
    passwordHash: "fcda0c33ae7ebfed39c826ac8eec59342a94b4c06a3d72abba875cc69e6a89ac",
    role: "admin"
  },
  {
    displayName: "GFIS Team User",
    emailHash: "1032fdee6eabbff3c6bcf93465d1f541b56fc50b666106ce7efe47d230f3796b",
    passwordHash: "fcda0c33ae7ebfed39c826ac8eec59342a94b4c06a3d72abba875cc69e6a89ac",
    role: "user"
  }
];

const state = {
  user: JSON.parse(localStorage.getItem("gfis_l2_session") || "null")
};

function readJson(key, fallback) {
  try {
    return JSON.parse(localStorage.getItem(key)) || fallback;
  } catch {
    return fallback;
  }
}

function writeJson(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

function users() {
  const existing = readJson("gfis_l2_users", null);
  if (existing && !existing.some((user) => user.password || user.email)) return existing;
  writeJson("gfis_l2_users", DEFAULT_USERS);
  return DEFAULT_USERS;
}

async function hashText(value) {
  const bytes = new TextEncoder().encode(value);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
}

function records(key) {
  return readJson(key, []);
}

function download(filename, content, type = "text/plain") {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

function renderAuth() {
  const loginPanel = document.querySelector("#loginPanel");
  const workbenchPanel = document.querySelector("#workbenchPanel");
  const adminPanel = document.querySelector("#adminPanel");
  if (!loginPanel || !workbenchPanel) return;

  const loggedIn = Boolean(state.user);
  loginPanel.classList.toggle("hidden", loggedIn);
  workbenchPanel.classList.toggle("hidden", !loggedIn);
  adminPanel?.classList.toggle("hidden", !loggedIn || state.user?.role !== "admin");

  if (loggedIn) {
    document.querySelector("#profileName").textContent = state.user.displayName;
    document.querySelector("#profileRole").textContent = `Role: ${state.user.role}`;
    renderNotes();
    renderDiary();
    renderUsers();
  }
}

function renderNotes() {
  const list = document.querySelector("#notesList");
  if (!list) return;
  const noteRows = records("gfis_l2_notes");
  list.innerHTML = noteRows.slice().reverse().map((note) => `
    <div class="record-item">
      <strong>${note.title}</strong>
      <span>${note.createdBy || "GFIS Team"} / ${note.createdAt}</span>
      <span>${note.body.slice(0, 180)}</span>
    </div>
  `).join("") || "<div class=\"record-item\"><strong>No notes yet.</strong><span>Write the first one above.</span></div>";
}

function renderDiary() {
  const list = document.querySelector("#diaryList");
  if (!list) return;
  const diaryRows = records("gfis_l2_diary");
  list.innerHTML = diaryRows.slice().reverse().map((entry) => `
    <div class="record-item">
      <strong>${entry.date}</strong>
      <span>${entry.createdBy || "GFIS Team"}</span>
      <span>${entry.body.slice(0, 180)}</span>
    </div>
  `).join("") || "<div class=\"record-item\"><strong>No diary entries yet.</strong><span>Start today’s log above.</span></div>";
}

function renderUsers() {
  const list = document.querySelector("#userList");
  if (!list) return;
  list.innerHTML = users().map((user) => `
    <div class="record-item">
      <strong>${user.displayName || "GFIS Team Member"}</strong>
      <span>Role: ${user.role}</span>
      <div class="record-actions">
        <button type="button" data-remove-user="${user.emailHash}">Remove</button>
      </div>
    </div>
  `).join("");
}

document.querySelector("#loginForm")?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const email = document.querySelector("#loginUser").value.trim().toLowerCase();
  const password = document.querySelector("#loginPass").value;
  const emailHash = await hashText(email);
  const passwordHash = await hashText(password);
  const found = users().find((user) => user.emailHash === emailHash && user.passwordHash === passwordHash);
  const message = document.querySelector("#loginMessage");
  if (!found) {
    message.textContent = "Invalid GFIS login.";
    return;
  }
  state.user = { displayName: found.displayName || "GFIS Team Member", emailHash: found.emailHash, role: found.role };
  localStorage.setItem("gfis_l2_session", JSON.stringify(state.user));
  message.textContent = "";
  document.querySelector("#loginPass").value = "";
  renderAuth();
});

document.querySelector("#logoutButton")?.addEventListener("click", () => {
  state.user = null;
  localStorage.removeItem("gfis_l2_session");
  renderAuth();
});

document.querySelector("#saveNote")?.addEventListener("click", () => {
  const title = document.querySelector("#noteTitle").value.trim() || "GFIS Note";
  const body = document.querySelector("#noteBody").value.trim();
  if (!body) return;
  const noteRows = records("gfis_l2_notes");
  noteRows.push({ title, body, createdBy: state.user.displayName, createdAt: new Date().toISOString() });
  writeJson("gfis_l2_notes", noteRows);
  document.querySelector("#noteBody").value = "";
  renderNotes();
});

document.querySelector("#saveDiary")?.addEventListener("click", () => {
  const date = document.querySelector("#diaryDate").value || new Date().toISOString().slice(0, 10);
  const body = document.querySelector("#diaryBody").value.trim();
  if (!body) return;
  const diaryRows = records("gfis_l2_diary");
  diaryRows.push({ date, body, createdBy: state.user.displayName, createdAt: new Date().toISOString() });
  writeJson("gfis_l2_diary", diaryRows);
  document.querySelector("#diaryBody").value = "";
  renderDiary();
});

document.querySelector("#exportNotes")?.addEventListener("click", () => {
  const noteRows = records("gfis_l2_notes");
  const content = noteRows.map((note) => `# ${note.title}\n\n${note.createdAt} / ${note.createdBy}\n\n${note.body}\n`).join("\n---\n\n");
  download("gfis_notes.md", content);
});

document.querySelector("#exportDiary")?.addEventListener("click", () => {
  const diaryRows = records("gfis_l2_diary");
  const content = diaryRows.map((entry) => `# ${entry.date}\n\n${entry.createdBy}\n\n${entry.body}\n`).join("\n---\n\n");
  download("gfis_diary.md", content);
});

document.querySelector("#downloadDoc")?.addEventListener("click", () => {
  const title = document.querySelector("#docTitle").value.trim() || "GFIS Draft";
  const body = document.querySelector("#docBody").value.trim().replace(/\n/g, "<br>");
  const html = `<!doctype html><html><head><meta charset="utf-8"><title>${title}</title></head><body><h1>${title}</h1><p>${body}</p></body></html>`;
  download(`${title.replace(/[^a-z0-9]+/gi, "_")}.doc`, html, "application/msword");
});

document.querySelector("#clearDoc")?.addEventListener("click", () => {
  document.querySelector("#docTitle").value = "";
  document.querySelector("#docBody").value = "";
});

document.querySelector("#downloadCsv")?.addEventListener("click", () => {
  download("gfis_readings.csv", document.querySelector("#sheetBody").value, "text/csv");
});

document.querySelector("#addSampleRow")?.addEventListener("click", () => {
  const now = new Date().toISOString().slice(0, 10);
  document.querySelector("#sheetBody").value += `\n${now},36.7,7.12,3.1,24,73,0.43,Stable`;
});

document.querySelector("#createUserForm")?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const email = document.querySelector("#newUserEmail").value.trim().toLowerCase();
  const password = document.querySelector("#newUserPassword").value.trim();
  const role = document.querySelector("#newUserRole").value;
  if (!email || !password) return;
  const emailHash = await hashText(email);
  const passwordHash = await hashText(password);
  const rows = users().filter((user) => user.emailHash !== emailHash);
  rows.push({ displayName: email, emailHash, passwordHash, role });
  writeJson("gfis_l2_users", rows);
  event.target.reset();
  renderUsers();
});

document.querySelector("#userList")?.addEventListener("click", (event) => {
  const emailHash = event.target.dataset.removeUser;
  if (!emailHash || emailHash === state.user?.emailHash) return;
  writeJson("gfis_l2_users", users().filter((user) => user.emailHash !== emailHash));
  renderUsers();
});

document.querySelector("#diaryDate") && (document.querySelector("#diaryDate").value = new Date().toISOString().slice(0, 10));
renderAuth();
