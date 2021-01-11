<template>
  <div id="Contribute">
    
    <nav id="navbar">
      <ul id="links">
        <li class="black-text" @click="goToMain">MAIN</li> |
        <li class="black-text" @click="goToData">DATA</li> |
        <li class="red-text" @click="goToContribute">CONTRIBUTE</li>
      </ul>
    </nav>
    
    <header id="header">
      <h1>VILNIUS "HEARTBEAT"</h1>
      <h3>Interactive traffic map</h3>
    </header>

    <div id="contribute-div">

      <div id="contribute-contents">
        <h4>For comments and suggestions contact me at:</h4>
        <div id="contact-card">
            <img src="./assets/an.png" alt="Augustinas Naina photo">
            <div id="contact-info">
              <p>Augustinas Naina</p>
              <br>
              <a href="mailto:augustinasnaina@gmail.com" target="_blank"><p>AugustinasNaina@gmail.com</p></a>
              <a href="https://www.linkedin.com/in/augustinasn/" target="_blank"><p>LinkedIn</p></a>
            </div>
        </div>
        
        <h4>To support this and future projects, visit my patreon page:</h4>
        <a id="patreon-logo" href="https://www.patreon.com/user?u=30039071" target="_blank"><img src="./assets/patreon.png" alt="Patreon Logo"></a>
      </div>
    </div>

  </div>
</template>

<script>

export default {
  name: 'Contribute',
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

@import url('https://fonts.googleapis.com/css?family=Montserrat&display=swap');
@import url('https://fonts.googleapis.com/css?family=Orbitron&display=swap');

@media screen and (max-width: 768px) {
  #contact-card {
    flex-direction: column !important;
  }
}

body {
  background: #f0f8ff;
  font-family: 'Montserrat', sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  color: #133337;
}

#header {
  margin: 0 auto;
  height: 10vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

#header h1, #header h2, #header h3 {
  margin: 0;
  text-align: center;
}

#header h1 {
  color: 	#ff0000;
  font-weight: 600;
}

#contribute-contents {
  display:flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 5rem;
}

#contact-card {
  margin-top: 1rem;
  display: flex;
  margin-bottom: 3rem;
}

#contact-card img {
  height: 10rem;
  width: 10rem;
  border-radius: 50%;
}

#contact-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-left: 2rem;
}

#contact-info p {
  margin: .1rem 0;
  padding: 0;
}

#contact-info a {
  color: #ff0000;
  text-decoration: none;
}

#patreon-logo img {
  width: 8rem;
}

</style>
