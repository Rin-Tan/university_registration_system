const coursesTbody = document.getElementById("coursesTbody");
const emptyState = document.getElementById("emptyState");
const searchInput = document.getElementById("searchInput");

let courses = [];

const API_URL = "http://localhost:8000/courses/api/V1/courses/";

// Load all courses
async function loadCourses() {
  try {
    const res = await fetch(API_URL);
    courses = await res.json();
    renderCourses();
  } catch (err) {
    console.error("Load failed:", err);
  }
}

// Render table
function renderCourses(filter = "") {
  coursesTbody.innerHTML = "";

  const filtered = courses.filter(
    c =>
      c.title.toLowerCase().includes(filter.toLowerCase()) ||
      c.course_code.toLowerCase().includes(filter.toLowerCase())
  );

  if (filtered.length === 0) {
    emptyState.style.display = "block";
    return;
  }

  emptyState.style.display = "none";

  filtered.forEach(c => {
    const tr = document.createElement("tr");

    tr.innerHTML = `
      <td>${c.title}</td>
      <td>${c.course_code}</td>
      <td>${c.capacity}</td>
      <td>${c.units}</td>
      <td>${c.day_of_week}</td>
      <td>${c.location}</td>
      <td>${c.start_time}</td>
      <td>${c.end_time}</td>
      <td>${c.prerequisites?.join(", ")}</td>
    `;

    coursesTbody.appendChild(tr);
  });
}

// Search
searchInput.addEventListener("input", () => renderCourses(searchInput.value));

// Initial load
loadCourses();
