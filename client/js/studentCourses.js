const coursesTbody = document.getElementById("coursesTbody");
const emptyState = document.getElementById("emptyState");
const searchInput = document.getElementById("searchInput");

let courses = [];

const API_URL = "http://localhost:8000/courses/api/v1/courses/";

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

function getPrerequisiteTitles(prereqIds = []) {
  if (!prereqIds.length) return "-";

  return prereqIds
    .map(id => {
      const course = allCourses.find(c => c.id === id);
      return course
        ? `${course.title} [${course.course_code}]`
        : `#${id}`;
    })
    .join(" , ");
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

       const times = c.time_slots_details?.length
      ? c.time_slots_details
          .map(
            t =>
              `${t.day_display} ${t.start_time.slice(0,5)}-${t.end_time.slice(0,5)}`
          )
          .join("<br>")
      : "-";

    tr.innerHTML = `
      <td>${c.title}</td>
      <td>${c.course_code}</td>
      <td>${c.capacity}</td>
      <td>${c.units}</td>
      <td>${times}</td>
      <td>${c.location || "-"}</td>
      <td>${c.prerequisites?.join(", ")}</td>
      <td data-label="Actions" class="actions-cell">
      <button
      class="action-btn icon-btn add-lesson-btn"
      data-course-id="${c.id}"
      title="Add Lesson">
      <img src="/static/images/icon-plus.svg" alt="Add Lesson" />
      </button>
      </td>
    `;

    coursesTbody.appendChild(tr);
  });
}
document.addEventListener("click", (e) => {
  if (e.target.classList.contains("add-lesson-btn")) {
    const courseId = e.target.dataset.courseId;

    console.log("Add lesson to course:", courseId);
  }
});


// Search
searchInput.addEventListener("input", () => renderCourses(searchInput.value));

// Initial load
loadCourses();
