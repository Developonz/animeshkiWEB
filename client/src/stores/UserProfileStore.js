import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserProfileStore = defineStore('userProfile', {
  state: () => ({
    is_auth: false,
    username: '',
    is_superuser: false
  }),

  actions: {
    async fetchUserProfile() {
      try {
        const response = await axios.get('/api/user/info/')
        if (response.data) {
          this.is_auth = response.data.is_authenticated || false
          this.username = response.data.name || ''
          this.is_superuser = response.data.is_superuser || false
        }
      } catch (error) {
        console.log('Пользователь не аутентифицирован')
        this.is_auth = false
        this.username = ''
        this.is_superuser = false
      }
    }
  }
})
