import { createRouter, createWebHistory } from 'vue-router'
import AnimeView from '../views/Anime.vue'
import DirectorsView from '../views/Director.vue'
import StudiosView from '../views/Studio.vue'
import GenresView from '../views/Genre.vue'
import CountriesView from '../views/Country.vue'
import AnimeDetail from '../views/AnimeDetail.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', 
      name: 'Anime',
      component: AnimeView
     },
     {
      path: '/anime/:id',
      name: 'AnimeDetail',
      component: AnimeDetail,
      props: true
     },
     {
      path: '/directors',
      name: 'Directors',
      component: DirectorsView
     },
     {
      path: '/studios',
      name: 'Studios',
      component: StudiosView
     },
     {
      path: '/genres',
      name: 'Genres',
      component: GenresView
     },
     {
      path: '/countries',
      name: 'Countries',
      component: CountriesView
     }
  ],
  linkActiveClass: 'active',
})

export default router
