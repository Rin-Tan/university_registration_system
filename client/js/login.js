const form = document.getElementById("loginForm");
const errorBox = document.getElementById("errorBox");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();
  const captchaResponse = grecaptcha.getResponse();
if (!captchaResponse) {
  errorBox.textContent = "Please check the captcha.";
  return;
}
  // Validate empty fields
  if (!username || !password) {
    errorBox.textContent = "Please enter both username and password.";
    return;
  }


  try {
    // Send login request to Django API
    const response = await fetch("/api/sessions/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        password: password,
        "g-recaptcha-response": captchaResponse  
      })
    });
    
    // Parse response JSON (contains access + refresh tokens)
    const data = await response.json();

    // If login failed (401)
    if (!response.ok) {
  errorBox.style.color = "red";
  

    //invalid-captcha
  if (data.error === "invalid-captcha") {
    errorBox.textContent = "Captcha validation failed. Please try again.";
    grecaptcha.reset(); 
  } else {
    errorBox.textContent = "Incorrect username or password.";
  }

  return;
   }




    // Store JWT tokens in localStorage
localStorage.setItem("access_token", data.access);
localStorage.setItem("refresh_token", data.refresh);
document.cookie = `access_token=${data.access}; path=/`;
alert(document.cookie);




    // Redirect after success
    errorBox.style.color = "blue";
    errorBox.textContent = "Login successful! Redirecting...";
    setTimeout(() => {
     window.location.href = "/dashboard/";
    }, 700);

  } catch (error) {
    // If API server is unreachable
    errorBox.style.color = "red";
    errorBox.textContent = "Could not connect to server.";
    console.error("Login error:", error);
  }
});
