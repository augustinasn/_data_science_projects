<template>
  <div id="app">
    <transition name="router-anim" enter-active-class="animated fadeIn faster">
      <router-view :key="$route.fullPath"></router-view>
    </transition>
  </div>
</template>

<script>

export default {
  name: 'app',
  data () {
    return {
    }
  },
  methods: {
    goToMain() {
      this.$router.push('/')
    },
    goToData() {
      this.$router.push('/data')
    },
    goToContribute() {
      this.$router.push('/contribute')
    }
  },
  mounted() {
  },
  computed: {
  },
  filters: {
  } 
}

</script>

<style>

#navbar {
  position: absolute;
  right: 0;
  text-decoration: none;
  margin-right: 1rem;
}

#links li {
  display: inline-block;
  margin: 0 .5rem;
  text-decoration: none;
  transition: color .2s;
  cursor: pointer;
}

#links li:hover {
  color: #cc0000;
  transition: color .2s;
}

.red-text {
  color: #ff0000;
  text-decoration: none;
}

.black-text {
  color: #133337;
  text-decoration: none;
}

</style>
