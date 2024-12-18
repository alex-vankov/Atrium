<template>
  <div id="app">
    <nav>
      <ul>
        <li><router-link to="/">Home</router-link></li>
      </ul>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>

export default {
  name: 'App',
};

</script>

<style>

body {
  background-size: contain; /* Scale to cover the viewport */
  background-repeat: no-repeat; /* Prevent tiling */
  background-attachment: fixed; /* Keeps the background in place */
  margin: 0; /* Remove default margins */
  font-family: Arial, sans-serif; /* Optional: Customize font */
}

nav ul {
  list-style-type: none;
  display: flex;
  gap: 10px;
}

router-link {
  text-decoration: none;
  color: blue;
}

</style>
