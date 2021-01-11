<template>
  <div id="Data">
    
    <nav id="navbar">
      <ul id="links">
        <li  class="black-text"@click="goToMain">MAIN</li> |
        <li class="red-text" @click="goToData">DATA</li> |
        <li class="black-text" @click="goToContribute">CONTRIBUTE</li>
      </ul>
    </nav>
    
    <header id="header">
      <h1>VILNIUS "HEARTBEAT"</h1>
      <h3>Interactive traffic map</h3>
    </header>

    <div id="data-source-div">
      <h3>Data <span class="red-text">source</span>:</h3>
      <div id="data-source-contents">
        <a href="https://api.vilnius.lt/" target="_blank"><img src="./assets/vilnius2in.png" alt="Vilnius2IN logo"></a>
        <p>This is an independant and voluntary project that was made possible by the <a class="red-text" href="https://api.vilnius.lt">Vilnius2IN</a> (Intelligent and Integrated) initiative, purpose of which is to integrate Vilnius City projects with each other and create greater benefits for the City of Vilnius and its inhabitants. <a style="red-text" href="https://github.com/vilnius/traffic" target="_blank">Here's</a> is a link to the repository of the dataset for Vilnius traffic data from 2018.</p>
      </div>
    </div>

    <div id="inspiration-div">
      <h3><span class="black-text">Inspiration</span>:</h3>
      <div id="inspiration-contents">
        <p>Project was inspired by <a href="https://www.facebook.com/events/a-go%C5%A1tauto-gatv%C4%97-12a-lt-01108-vilnius-lietuva/future-pros-challenge-data-science/368742297182231/" target="_blank" class="red-text">Data Science Challenge 2019</a> event, organized by <a href="https://danskebank.lt/" target="_blank" class="red-text">Danske Bank Lithuania</a> as a part of the <a href="https://danskebank.lt/en/career/future-pros/future-pros" target="_blank" class="red-text">Future Pros</a> initiative, a program that successfully combines two hard-to-combine subjects - study and work - into one new combination. It is designed for students who want a perfect balance between professional and academic life, not formally, but in reality.</p>
        <a href="https://danskebank.lt/" target="_blank"><img src="./assets/danske.png" alt="Danske bank logo"></a>
      </div>
    </div>

    <h3 id="thank-you">Big thank you to everyone involved!</h3>

  </div>
</template>

<script>

export default {
  name: 'Data',
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

#data-source-div {
  background: #133337;
  color: #f0f8ff;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 2rem;
}

#inspiration-div {
  background: #e6e6fa;
  color: #133337;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

#data-source-contents, #inspiration-contents {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 50%;
  margin-bottom: 2rem;
}

#data-source-contents img,  #inspiration-contents img {
  flex: 1;
  width: 10rem;
}

#data-source-contents p {
  text-align: justify;
  padding-left: 5rem;
}

#inspiration-contents p {
  text-align: justify;
  padding-right: 5rem;
}

#data-source-contents p a {
  color: #ff0000;
  text-decoration: none;
}

#thank-you {
  margin-top: 5rem;
  text-align: center;
  color: #ff0000;
}


</style>