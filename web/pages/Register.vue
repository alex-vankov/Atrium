<template>
  <div class='register'>
    <h2>Register</h2>
    <form @submit.prevent="register">
      <div class="form-group">
        <label for="firstname">First Name</label>
        <input
          v-model="firstname"
          type="text"
          id="firstname"
          placeholder="Enter your first name"
          required
        />
      </div>
      <div class="form-group">
        <label for="lastname">Last Name</label>
        <input
          v-model="lastname"
          type="text"
          id="lastname"
          placeholder="Enter your last name"
          required
        />
      </div>
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
        <label for="email">Email</label>
        <input
          v-model="email"
          type="email"
          id="email"
          placeholder="Enter your email"
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
      <button type="submit" :disabled="loading">{{ loading ? 'Registering...' : 'Register' }}</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
    <div>
      <router-link to="/login">Already have an account? Login</router-link>
    </div>
  </div>

</template>

<script>
import axios from "axios";

export default {
  name: "Register",
  data() {
    return {
      firstname: "",
      lastname: "",
      username: "",
      email: "",
      password: "",
      error: "",
      loading: false,
    };
  },
  methods: {
    async register() {
      // Clear previous error
      this.error = "";
      this.loading = true;

      // Check if the form is filled out properly (basic validation)
      if (!this.firstname || !this.lastname || !this.username || !this.email || !this.password) {
        this.error = "Please fill in all fields.";
        this.loading = false;
        return;
      }

      try {
        // Create the payload object
        const payload = {
          firstname: this.firstname,
          lastname: this.lastname,
          username: this.username,
          email: this.email,
          password: this.password,
        };

        // Send register request with JSON body
        const response = await axios.post("http://localhost:8000/api/v1/users/", payload, {
          headers: { "Content-Type": "application/json" },
        });

        // Check if the user was created successfully
        if (response.data && response.data.username) {
          // Redirect to the login page
          this.$router.push("/login");
        } else {
          this.error = "Failed to create a new user. Please try again.";
        }
      } catch (err) {
        console.error("Error during registration:", err);
        if (err.response && err.response.data) {
          this.error = err.response.data.detail || "An unexpected error occurred.";
        } else {
          this.error = "Failed to create a new user. Please try again.";
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>

.register {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 15px;
  margin-bottom: 15px;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #0056b3;
}

.error {
  color: red;
}
</style>
