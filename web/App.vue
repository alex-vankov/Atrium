<template>
  <div id="app">
    <nav>
      <ul class="nav-left">
        <li><router-link to="/">Home</router-link></li>
        <li v-if="isLoggedIn"><a href="#" @click="logout">Logout</a></li>
      </ul>
      <div class="nav-right" v-if="isLoggedIn">
        <router-link to="/profile">
        <p>{{ username }}</p>
        </router-link>
      </div>
      <ul class="nav-right" v-if="!isLoggedIn">
        <li><router-link to="/login">Login</router-link></li>
        <li><router-link to="/register">Register</router-link></li>
      </ul>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      isLoggedIn: false, // Tracks login state
      username: "", // Stores the username
    };
  },
  methods: {
    checkLoginStatus() {
      // Check if a token exists in localStorage
      this.isLoggedIn = !!localStorage.getItem("token");

      // Retrieve username from localStorage
      if (this.isLoggedIn) {
        this.username = localStorage.getItem("username") || "User";
      } else {
        this.username = "";
      }
    },
    logout() {
      // Remove token and username from localStorage
      localStorage.removeItem("token");
      localStorage.removeItem("username");

      // Update state
      this.isLoggedIn = false;
      this.username = "";

      // Redirect to the login page
      this.$router.push("/login");
    },
  },
  created() {
    // Check login status when the app is created
    this.checkLoginStatus();
  },
  watch: {
    // Watch for route changes to re-check login status
    $route() {
      this.checkLoginStatus();
    },
  },
};
</script>

<style>
body {
  background-size: contain; /* Scale to cover the viewport */
  background-repeat: no-repeat; /* Prevent tiling */
  background-color: papayawhip;
  background-attachment: fixed; /* Keeps the background in place */
  margin: 0; /* Remove default margins */
  font-family: Arial, sans-serif; /* Optional: Customize font */
}

nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: darkolivegreen;
}

.nav-left {
  list-style-type: none;
  display: flex;
  gap: 10px;
  margin: 0;
  padding: 0;
}

.nav-left a {
  font-size: 16px;
  text-decoration: none;
  color: papayawhip;
}

.nav-right {
  list-style-type: none;
  display: flex;
  gap: 10px;
  margin: 0;
  padding: 0;
}

.nav-right p, .nav-right a {
  font-size: 16px;
  color: papayawhip;
  text-decoration: none;
}
</style>
