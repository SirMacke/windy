// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      
    }
  },
  vite: {
    css: {
      preprocessorOptions: {
        sass: {
          additionalData: '@use "~/assets/sass/variables.sass" as *\n'
        },
      },
    },
  },
  compatibilityDate: '2024-11-01'
})
