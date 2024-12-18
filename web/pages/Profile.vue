<template>
  <div class="profile">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="profile-card">
      <h1>{{ user.username }}</h1>
      <p><strong>Name:</strong> {{ user.firstname }} {{ user.lastname }}</p>
      <p><strong>Email:</strong> {{ user.email }}</p>
      <p><strong>Role:</strong> {{ user.role }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Profile",
  data() {
    return {
      user: null,
      loading: true,
      error: null,
    };
  },
  methods: {
    async fetchUserProfile() {
      try {
        const response = await axios.get("http://localhost:8000/api/v1/users/me", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        this.user = response.data;
      } catch (err) {
        this.error = "Failed to load profile information. Please try again.";
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
  },
  mounted() {
    this.fetchUserProfile();
  },
};
</script>

<style scoped>
.profile {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.loading,
.error {
  font-size: 18px;
  color: #666;
}

.profile-card {
  padding: 20px;
}

h1 {
  font-size: 24px;
  margin: 10px 0;
}

p {
  font-size: 16px;
  color: #555;
}
</style>
