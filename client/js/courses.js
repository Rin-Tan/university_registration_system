const coursesTbody = document.getElementById("coursesTbody");
const emptyState = document.getElementById("emptyState");
const openAddBtn = document.getElementById("openAddBtn");
const modalOverlay = document.getElementById("modalOverlay");
const closeModal = document.getElementById("closeModal");
const cancelCourseBtn = document.getElementById("cancelCourseBtn");
const courseForm = document.getElementById("courseForm");
const searchInput = document.getElementById("searchInput");

let courses = [];
let editId = null;
let allCourses = [];
coursesLoaded = true;

const API_URL = "http://localhost:8000/courses/api/V1/courses/";

// Open modal
openAddBtn.addEventListener("click", () => {
  if (!coursesLoaded) {
    alert("Courses are still loading, please wait...");
    return;
  }

  modalOverlay.classList.remove("hidden");
  courseForm.reset();
  editId = null;

  fillPrerequisites(null);  
  document.getElementById("prereqSearch").value = "";
});


// Close modal
closeModal.addEventListener("click", () => modalOverlay.classList.add("hidden"));
cancelCourseBtn.addEventListener("click", () => modalOverlay.classList.add("hidden"));


// Load all courses
async function loadCourses() {
  try {
    const res = await fetch(API_URL);
    courses = await res.json();
    allCourses = courses; 
    coursesLoaded = true;
    renderCourses();
  } catch (err) {
    console.error("Load failed:", err);
  }
}
console.log("ALL COURSES:", allCourses);


function fillPrerequisites(excludeId = null) {
  console.log("FILLING PREREQUISITES", allCourses.length);

  const select = document.getElementById("prerequisites");
  select.innerHTML = "";

  allCourses.forEach(course => {
    if (course.id === excludeId) return;

    const opt = document.createElement("option");
    opt.value = course.id;
    opt.textContent = `${course.title} (${course.course_code})`;
    select.appendChild(opt);
  });
}

function filterPrerequisites() {
  const q = document.getElementById("prereqSearch").value.toLowerCase();
  const options = document.getElementById("prerequisites").options;

  Array.from(options).forEach(opt => {
    opt.style.display = opt.textContent.toLowerCase().includes(q)
      ? "block"
      : "none";
  });
}

// Submit (Add / Edit)
courseForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    title: document.getElementById("title").value,
    course_code: document.getElementById("course_code").value,
    capacity: Number(document.getElementById("capacity").value),
    units: Number(document.getElementById("units").value),
    day_of_week: document.getElementById("day_of_week").value,
    location: document.getElementById("location").value,
    start_time: document.getElementById("start_time").value,
    end_time: document.getElementById("end_time").value,
    prerequisites: Array.from(document.getElementById("prerequisites").selectedOptions).map(o => Number(o.value)),
  };

  try {
    let res;

    if (editId) {
      res = await fetch(API_URL + editId + "/", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
    } else {
      res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
    }

    if (!res.ok) throw new Error("Saving failed");

    modalOverlay.classList.add("hidden");
    loadCourses();

  } catch (err) {
    console.error("Error saving course:", err);
  }
});

function getPrerequisiteTitles(prereqIds = []) {
  if (!prereqIds.length) return "-";

  return prereqIds
    .map(id => {
      const course = allCourses.find(c => c.id === id);
      return course ? `${course.title}[${course.course_code}]` : `#${id}`;
    })
    .join(" - ");
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
      <td>${getPrerequisiteTitles(c.prerequisites)}</td>
      <td class="actions-cell">
        <button class="btn-edit action-btn">Edit</button>
        <button class="btn-delete action-btn">Delete</button>
      </td>
    `;

    // Edit
    tr.querySelector(".btn-edit").addEventListener("click", () => {
      editId = c.id;

      document.getElementById("title").value = c.title;
      document.getElementById("course_code").value = c.course_code;
      document.getElementById("capacity").value = c.capacity;
      document.getElementById("units").value = c.units;
      document.getElementById("day_of_week").value = c.day_of_week;
      document.getElementById("location").value = c.location;
      document.getElementById("start_time").value = c.start_time;
      document.getElementById("end_time").value = c.end_time;
      fillPrerequisites(c.id);

const prereqIds = c.prerequisites || [];
Array.from(document.getElementById("prerequisites").options).forEach(opt => {
  opt.selected = prereqIds.includes(Number(opt.value));
});

document.getElementById("prereqSearch").value = "";

      //document.getElementById("courseExamTime").value = c.exam || "";

      modalOverlay.classList.remove("hidden");
    });

    // Delete
    tr.querySelector(".btn-delete").addEventListener("click", async () => {
      if (confirm(`Delete ${c.title}?`)) {
        try {
          await fetch(API_URL + c.id + "/", { method: "DELETE" });
          loadCourses();
        } catch (err) {
          console.error("Delete failed:", err);
        }
      }
    });

    coursesTbody.appendChild(tr);
  });
}


// Search
searchInput.addEventListener("input", () => renderCourses(searchInput.value));


// Initial load
loadCourses();
