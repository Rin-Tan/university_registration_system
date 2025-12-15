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
let coursesLoaded = true;
const TIME_API_URL = "http://localhost:8000/courses/api/v1/timeslots/";
const API_URL = "http://localhost:8000/courses/api/v1/courses/";

async function loadTimeSlots() {
  try {
    const res = await fetch(TIME_API_URL);

    if (!res.ok) throw new Error("TimeSlot fetch failed");

    const slots = await res.json();
    const select = document.getElementById("timeSlots");

    if (!select) {
      console.error("timeSlots select not found in DOM");
      return;
    }

    select.innerHTML = "";

    if (slots.length === 0) {
      const opt = document.createElement("option");
      opt.textContent = "No time slots available";
      opt.disabled = true;
      select.appendChild(opt);
      return;
    }

    slots.forEach(slot => {
      const opt = document.createElement("option");
      opt.value = slot.id;
      opt.textContent =
        `${slot.day_display} | ${slot.start_time.slice(0,5)} - ${slot.end_time.slice(0,5)}`;
      select.appendChild(opt);
    });

  } catch (err) {
    console.error(err);
    notify("Failed to load time slots", "error");
  }
}


function notify(message, type = "success") {
  const box = document.getElementById("notification");

  box.textContent = message;
  box.className = "notification " + type;
  box.classList.remove("hidden");

  setTimeout(() => {
    box.classList.add("hidden");
  }, 3000);
}

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
  
   loadTimeSlots();
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
  location: document.getElementById("location").value,
  prerequisites: Array.from(
    document.getElementById("prerequisites").selectedOptions
  ).map(o => Number(o.value)),
  time_slots: Array.from(
    document.getElementById("timeSlots").selectedOptions
  ).map(o => Number(o.value))
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

    if (!res.ok) throw new Error();
    notify(
  editId ? "Course updated successfully" : "Course added successfully",
  "success"
  );


    modalOverlay.classList.add("hidden");
    loadCourses();

  } catch (err) {
    notify("Operation failed", "error");

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
    const times = c.time_slots_details?.length
  ? c.time_slots_details
      .map(t => `${t.day_display} ${t.start_time.slice(0,5)}-${t.end_time.slice(0,5)}`)
      .join("<br>")
  : "-";


    tr.innerHTML = `
      <td>${c.title}</td>
      <td>${c.course_code}</td>
      <td>${c.capacity}</td>
      <td>${c.units}</td>
      <td>${times}</td>
      <td>${c.location}</td>
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
      const selectedIds = c.time_slots_details
      ? c.time_slots_details.map(t => t.id)
      : [];
      Array.from(document.getElementById("timeSlots").options).forEach(opt => {
          opt.selected = selectedIds.includes(Number(opt.value));
        });
        notify("Course loaded for editing", "info");


      document.getElementById("location").value = c.location;

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
            notify("Course deleted successfully", "success");
          loadCourses();
        } catch (err) {
          notify("Delete failed", "error");
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
loadTimeSlots();
loadCourses();
