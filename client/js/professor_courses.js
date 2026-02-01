document.addEventListener("DOMContentLoaded", function () {
  const coursesTbody = document.getElementById("coursesTbody");
  const studentsTbody = document.getElementById("studentsTbody");
  const studentsSection = document.getElementById("studentsSection");

  const STORAGE_KEY = "professor_courses";

    //  SEED DATA 

  const DEFAULT_DATA = [
    {
      id: 1,
      title: "Database Systems",
      code: "CS301",
      units: 3,
      students: [
        { id: 11, first_name: "Ali", last_name: "Ahmadi", student_id: "401001" },
        { id: 12, first_name: "Sara", last_name: "Hosseini", student_id: "401002" }
      ]
    },
    {
      id: 2,
      title: "Operating Systems",
      code: "CS302",
      units: 4,
      students: [
        { id: 13, first_name: "Mina", last_name: "Abbasi", student_id: "401003" }
      ]
    }
  ];

  if (!localStorage.getItem(STORAGE_KEY)) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(DEFAULT_DATA));
  }

 
   //  API FUNCTIONS 

  async function apiGetProfessorCourses() {
    return {
      success: true,
      data: JSON.parse(localStorage.getItem(STORAGE_KEY))
    };
  }

  async function apiRemoveStudent(courseId, studentId) {
    const courses = JSON.parse(localStorage.getItem(STORAGE_KEY));
    const course = courses.find(c => c.id === courseId);

    if (!course) {
      return { success: false, message: "Course not found" };
    }

    course.students = course.students.filter(s => s.id !== studentId);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(courses));

    return { success: true };
  }

  
   //  UI LOGIC
  

  let courses = [];
  let activeCourseId = null;

  async function loadCourses() {
    const res = await apiGetProfessorCourses();
    if (!res.success) return;

    courses = res.data;
    renderCourses();
  }

  function renderCourses() {
    coursesTbody.innerHTML = "";

    courses.forEach(c => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${c.title}</td>
        <td>${c.code}</td>
        <td>${c.units}</td>
        <td class="actions-cell">
          <button class="action-btn" data-course="${c.id}">
            View Students
          </button>
        </td>
      `;
      coursesTbody.appendChild(tr);
    });
  }

  function renderStudents(courseId) {
    activeCourseId = courseId;
    studentsSection.style.display = "block";
    studentsTbody.innerHTML = "";

    const course = courses.find(c => c.id === courseId);
    if (!course) return;

    const sortedStudents = [...course.students].sort((a, b) =>
      a.last_name.localeCompare(b.last_name)
    );

    sortedStudents.forEach(s => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${s.first_name}</td>
        <td>${s.last_name}</td>
        <td>${s.student_id}</td>
        <td class="actions-cell">
          <button
            class="action-btn btn-delete remove-student-btn"
            data-student="${s.id}">
            Remove
          </button>
        </td>
      `;
      studentsTbody.appendChild(tr);
    });
  }

  //   EVENTS


  document.addEventListener("click", async (e) => {
    const viewBtn = e.target.closest("[data-course]");
    if (viewBtn) {
      renderStudents(Number(viewBtn.dataset.course));
    }

    const removeBtn = e.target.closest(".remove-student-btn");
    if (removeBtn) {
      if (!confirm("Remove this student from the course?")) return;

      const studentId = Number(removeBtn.dataset.student);
      const res = await apiRemoveStudent(activeCourseId, studentId);
      if (!res.success) return;

      await loadCourses();
      renderStudents(activeCourseId);
    }
  });


//     INIT


  loadCourses();
});
