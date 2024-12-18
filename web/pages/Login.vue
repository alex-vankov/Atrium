<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="username">Username</label>
        <input
          v-model="username"
          type="text"
          id="username"
          placeholder="Enter your username"
          required
        />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input
          v-model="password"
          type="password"
          id="password"
          placeholder="Enter your password"
          required
        />
      </div>
      <button type="submit">Login</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginPage",
  data() {
    return {
      username: "",
      password: "",
      error: "",
    };
  },
  methods: {
    async login() {
      try {
        const formData = new URLSearchParams();
        formData.append("username", this.username);
        formData.append("password", this.password);

        // Send login request to get the token
        const response = await axios.post("http://localhost:8000/api/v1/token/", formData, {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        });

        // Check if access_token exists
        if (response.data && response.data.access_token) {
          // Store the token in localStorage
          localStorage.setItem("token", response.data.access_token);

          // Optionally, you can fetch the username using a separate API endpoint.
          // For now, just use the username entered during login for the greeting later.
          localStorage.setItem("username", this.username);

          // Redirect to the home page or dashboard
          this.$router.push("/");
        } else {
          this.error = "Login failed. No token received.";
        }
      } catch (err) {
        console.error("Login error:", err.response || err);  // Log detailed error response
        if (err.response && err.response.status === 401) {
          this.error = "Invalid username or password.";
        } else {
          this.error = "An unexpected error occurred. Please try again.";
        }
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  width: 300px;
  margin: 100px auto;
  text-align: center;
}
.form-group {
  margin-bottom: 15px;
}
input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}
button {
  padding: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}
button:hover {
  background-color: #369870;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>
