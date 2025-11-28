const form = document.getElementById("loginForm");
const errorBox = document.getElementById("errorBox");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  // Validate empty fields
  if (!username || !password) {
    errorBox.textContent = "Please enter both username and password.";
    return;
  }

  try {
    // Send login request to Django API
    const response = await fetch("http://localhost:8000/api/sessions/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    // If login failed (401)
    if (!response.ok) {
      errorBox.style.color = "red";
      errorBox.textContent = "Incorrect username or password.";
      return;
    }

    // Parse response JSON (contains access + refresh tokens)
    const data = await response.json();

    // Store JWT tokens in localStorage
    localStorage.setItem("access", data.access);
    localStorage.setItem("refresh", data.refresh);

    // Redirect after success
    errorBox.style.color = "blue";
    errorBox.textContent = "Login successful! Redirecting...";
    setTimeout(() => {
      window.location.href = "dashboard.html";
    }, 700);

  } catch (error) {
    // If API server is unreachable
    errorBox.style.color = "red";
    errorBox.textContent = "Could not connect to server.";
    console.error("Login error:", error);
  }
});
