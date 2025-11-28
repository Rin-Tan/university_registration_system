const coursesTbody = document.getElementById('coursesTbody');
const emptyState = document.getElementById('emptyState');
const openAddBtn = document.getElementById('openAddBtn');
const modalOverlay = document.getElementById('modalOverlay');
const closeModal = document.getElementById('closeModal');
const cancelCourseBtn = document.getElementById('cancelCourseBtn');
const courseForm = document.getElementById('courseForm');
const searchInput = document.getElementById('searchInput');

let courses = [];
let editId = null; 

const API_URL = "http://localhost:8000/courses/";

// Open Modal
openAddBtn.addEventListener('click', () => {
  modalOverlay.classList.remove('hidden');
  courseForm.reset();
  editId = null;
});

// Close Modal
closeModal.addEventListener('click', () => modalOverlay.classList.add('hidden'));
cancelCourseBtn.addEventListener('click', () => modalOverlay.classList.add('hidden'));

// Load Courses from API
async function loadCourses() {
  try {
    const res = await fetch(API_URL);
    courses = await res.json();
    renderCourses();
  } catch (err) {
    console.error("Error loading courses:", err);
  }
}

// Save/Edit Course
courseForm.addEventListener('submit', async e => {
  e.preventDefault();

  const courseData = {
    title: document.getElementById('courseName').value,
    course_code: document.getElementById('courseCode').value,
    capacity: Number(document.getElementById('courseCapacity').value),
    professor: document.getElementById('courseProfessor').value,
    day_of_week: document.getElementById('courseTime').value,
    location: document.getElementById('courseLocation').value,
    start_time: document.getElementById('courseStartTime')?.value || "00:00:00",
    end_time: document.getElementById('courseEndTime')?.value || "00:00:00",
    exam: document.getElementById('courseExamTime').value,
    prerequisites: []
  };

  try {
    let res;
    if (editId) {
      res = await fetch(`${API_URL}${editId}/`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(courseData)
      });
    } else {
      res = await fetch(API_URL, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(courseData)
      });
    }
    await res.json();
    modalOverlay.classList.add('hidden');
    loadCourses();
  } catch (err) {
    console.error("Error saving course:", err);
  }
});

// Render Courses
function renderCourses(filter='') {
  coursesTbody.innerHTML = '';
  const filtered = courses.filter(c => c.title.toLowerCase().includes(filter.toLowerCase()) || c.course_code.toLowerCase().includes(filter.toLowerCase()));

  if(filtered.length === 0){
    emptyState.style.display = 'block';
  } else {
    emptyState.style.display = 'none';
    filtered.forEach(c => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${c.title}</td>
        <td>${c.course_code}</td>
        <td>${c.capacity}</td>
        <td>${c.professor || ''}</td>
        <td>${c.day_of_week} / ${c.location}</td>
        <td>${c.exam || ''}</td>
        <td class="actions-cell">
          <button class="btn-edit action-btn">Edit</button>
          <button class="btn-delete action-btn">Delete</button>
        </td>
      `;

      // Edit
      tr.querySelector('.btn-edit').addEventListener('click', () => {
        document.getElementById('courseName').value = c.title;
        document.getElementById('courseCode').value = c.course_code;
        document.getElementById('courseCapacity').value = c.capacity;
        document.getElementById('courseProfessor').value = c.professor || '';
        document.getElementById('courseTime').value = c.day_of_week;
        document.getElementById('courseLocation').value = c.location;
        document.getElementById('courseExamTime').value = c.exam || '';
        editId = c.id;
        modalOverlay.classList.remove('hidden');
      });

      // Delete
      tr.querySelector('.btn-delete').addEventListener('click', async () => {
        if(confirm(`Delete ${c.title}?`)){
          try {
            await fetch(`${API_URL}${c.id}/`, { method: 'DELETE' });
            loadCourses();
          } catch(err) {
            console.error("Error deleting course:", err);
          }
        }
      });

      coursesTbody.appendChild(tr);
    });
  }
}

// Search
searchInput.addEventListener('input', () => renderCourses(searchInput.value));

// Initial load
loadCourses();
