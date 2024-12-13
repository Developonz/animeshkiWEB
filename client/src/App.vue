<script setup>

</script>

<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Navbar</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link to="/" class="nav-link" aria-current="page">Аниме</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/directors" class="nav-link">Режиссеры</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/studios" class="nav-link">Студии</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/genres" class="nav-link">Жанры</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/countries" class="nav-link">Страны студий</router-link>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Пользователь
              </a>
              <ul class="dropdown-menu">
                <li>
                  <a href="/admin" class="dropdown-item">Админка</a>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container">
      <router-view />
    </div>
  </div>
</template>



<style scoped>
  .nav-link.active {
    color: #ff0000 !important;
    background-color: #e0e0e0;
    border-radius: 10px; 
  }

  .nav-link {
    padding-bottom: 2px;
    border-bottom: 2px solid transparent;
  }

  .nav-link:not(.active):hover {
    border-bottom: 2px solid #0d6efd;
  }
</style>