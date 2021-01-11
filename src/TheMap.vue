<template>
  <div id="TheMap">

    <div id="nav">
      <div id="navbar-contents">
        <div id="header-div">
          <h1>VILNIUS HEARTBEAT</h1>
          <h3>Dynamic Traffic Map</h3>
        </div>
      </div>
    </div>


    <div id="map-div">
      <div id="map"></div>
    </div>

    <div id="controls-div">
      <div id="controls-content">
        <div id="select-data-div">
          <div id="select-metric-div">
            <label for="metric-selection">Metric:</label>
            <select id="metric-selection" name="metric-selection">
              <option value="vol">Traffic volume (auto/h)</option>
              <option value="occ">Detector occupancy (% of measuring interval)</option>
              <option value="speed">Average speed (km/h)</option>
            </select>
          </div>
          <div id="select-subset-div">
            <label for="subset-selection">Filter:</label>
            <select id="subset-selection" name="subset-selection">
              <option value="averageWorkdayAutumn">Avg. workday (Sep-Apr)</option>
              <option value="averageWorkdaySummer">Avg. workday (Jun-Aug)</option>
              <option value="averageWorkdayStud">Avg. workday during school holidays</option>
              <option value="averageBankHoliday">Avg. workday during bank holidays</option>
              <option value="averageWeekendAutumn">Avg. weekend (Sep-Apr)</option>
            </select>
          </div>
        </div>

        <div id="clock-div">
          <div id="hour-div">
            <a href="#" id="minusOne" class="control-btn" v-bind:style="[running ? {opacity: 0} : {opacity:1}]">&larr;</a>
            <h2>{{ hours }}</h2>
            <a href="#" id="plusOne" class="control-btn" v-bind:style="[running ? {opacity: 0} : {opacity:1}]">&rarr;</a>
          </div>
          <a href="#" id="play-pause-button">Pause</a>
        </div>

        <div id="details-div">
          <p v-if="running">Press "Pause" to enter detailed view.</p>
          <div v-else>
            <ul v-if="currVol">
              <li>Intersection: <span class="strong">{{ currInter }}</span>.</li>
              <li>Volume: <span class="strong">{{ currVol | round }} cars per hour</span></li>
              <li>Occupancy: <span class="strong">{{ currOcc | round }}% </span></li>
              <li>Average speed: <span class="strong">{{ currSpeed | round }} km/h</span></li>
            </ul>
            <p v-else>Hover on an intersection for more details, use arrow keys (&larr; or &rarr;) for time shifting, press "Resume" to leave detailed view.</p>
          </div>
        </div>
      </div>
    </div>
    <div id="footer">
      <p>All Rights Reserved | <a href="https://www.linkedin.com/in/augustinasn/" class="strong" target="_blank">Augustinas Naina</a> | 2020</p>
    </div>
  </div>
</template>

<script>
import coordinates from './data/coords.json'

export default {
  name: 'TheMap',
  data () {
    return {
      index: 0,
      currInter: '-',
      currVol: 0,
      currOcc: 0,
      currSpeed: 0,
      running: true,
      subset: 'averageWorkdayAutumn',
      metric: 'vol',
      interval: {}
    }
  },
  methods: {
    goToMain() {
      clearInterval(this.interval)
      this.$router.push('/')
    },

    goToData() {
      clearInterval(this.interval)
      this.$router.push('/data')
    },

    goToContribute() {
      clearInterval(this.interval)
      this.$router.push('/contribute')
    },

    plot() {
      let currHour;
      let currCode;

      let currLat;
      let currLong;
      let currStreet;
      
      let parsedData = {};

      // let interval;
      let button;
      let dataSampled = {};

      let columnMatrix = {
        'averageWorkdayAutumn': {
          'vol': 'vol_wd_autumn',
          'occ': 'occ_wd_autumn',
          'speed': 'speed_wd_autumn'
        },
        'averageWorkdaySummer': {
          'vol': 'vol_wd_summer',
          'occ': 'occ_wd_summer',
          'speed': 'speed_wd_summer'
        },
        'averageWorkdayStud': {
          'vol': 'vol_stud_autumn',
          'occ': 'occ_stud_autumn',
          'speed': 'speed_stud_autumn'
        },
        'averageBankHoliday': {
          'vol': 'vol_holi',
          'occ': 'occ_holi',
          'speed': 'speed_holi'
        },
        'averageWeekendAutumn': {
          'vol': 'vol_wkd_autumn',
          'occ': 'occ_wkd_autumn',
          'speed': 'speed_wkd_autumn'
        },
      }

      let metricParsed = columnMatrix[this.subset][this.metric]

      // CANVAS:
      var map = L
        .map('map')
        .setView([54.70, 25.26], 14);

      L.tileLayer(
        'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '<a href="https://api.vilnius.lt/">Vilnius API</a>',
        minZoom: 14,
        maxZoom: 14
      }).addTo(map);

      L.svg()
        .addTo(map)

      const g = d3.select("#map")
                  .select("svg")

      g.attr("style", "pointer-events: auto;")

      map.panTo(new L.LatLng(54.70, 25.26));


      // SCALES:    
      const colorScale = d3.scaleOrdinal()
        .domain(['vol', 'occ', 'speed'])
        .range(['purple', 'blue', 'red']);

      // RUNTIME:
      const update = data => {
        dataSampled = data[this.index]
        metricParsed = columnMatrix[this.subset][this.metric]

        // TRANSITION:
        let t = d3.transition()
          .duration(150);

        // SCALES:
        const rScale = d3.scaleLinear()
          .range([5, 30])
          
        if (this.metric == 'vol') {
          rScale
            .domain([0, 600])
        } else if (this.metric == 'occ') {
          rScale
            .domain([0, 25])
        } else {
          rScale
            .domain([0, 50]) // Else - Speed
        };
      
        // JOIN:
        const dots = d3.select("#map")
          .select("svg")
          .selectAll("circle")
          .data(dataSampled)

        // EXIT:
        dots.exit().remove()

        // UPDATE
        dots
          .attr("cx", d => (typeof d !== 'undefined' ? map.latLngToLayerPoint([d[0]['lat'], d[0]['long']]).x : 0))
          .attr("cy", d => (typeof d !== 'undefined' ? map.latLngToLayerPoint([d[0]['lat'], d[0]['long']]).y : 0))
          .attr("r", d => (typeof d !== 'undefined' ? rScale(d[0][metricParsed]) : 5) )
          .style("fill", colorScale(this.metric))
          .style('cursor', 'pointer')
          .attr("fill-opacity", .5)
          .on('mouseover', printData)
          .on('mouseout', clearData)

        // ENTER:
            
        dots.enter()
          .append('circle')
            .style("fill", colorScale(this.metric))
            .style('cursor', 'pointer')
            .attr("fill-opacity", .5)
            .on('mouseover', printData )
            .on('mouseout', clearData)
            .attr("cx", d => (typeof d !== 'undefined' ? map.latLngToLayerPoint([d[0]['lat'], d[0]['long']]).x : 0))
            .attr("cy", d => (typeof d !== 'undefined' ? map.latLngToLayerPoint([d[0]['lat'], d[0]['long']]).y : 0))
            .transition(t)
              .attr("r", d => (typeof d !== 'undefined' ? rScale(d[0][metricParsed]) : 1) )
      }

      const printData = d => {
        this.currInter = d[0]['street']
        this.currVol = d[0][columnMatrix[this.subset]['vol']]
        this.currOcc = d[0][columnMatrix[this.subset]['occ']]
        this.currSpeed = d[0][columnMatrix[this.subset]['speed']]
      }

      const clearData = () => {
        this.currInter = '-'
        this.currVol = 0
        this.currOcc = 0
        this.currSpeed = 0
      } 

      // IMPORT DATA:
      d3.csv('./src/data/traffic_comb.csv').then(data => {
          data.forEach(row => {
            currHour = +row['Hour'];
            currCode = +row['Code'];

            if (currHour in parsedData) {
              if (currCode in parsedData[currHour]) {
              } else {
                parsedData[currHour][currCode] = [];
              }
            } else {
              parsedData[currHour] = [];
            }
          })

          data.forEach(row => {
              currHour = +row['Hour'];
              currCode = +row['Code'];
          
              if (row['Code'] in coordinates) {
                currLat = coordinates[row['Code']]['lat'].replace(',', '.');
                currLong = coordinates[row['Code']]['long'].replace(',', '.');
                currStreet = coordinates[row['Code']]['street'];
              } else {
                currLat = '0';
                currLong = '0';
                currStreet = 'N/A';
              }

              if (currCode in parsedData[currHour]) {
                parsedData[currHour][currCode].push({
                  "vol_wd_autumn": +row['vol_wd_autumn'],
                  "occ_wd_autumn": +row['occ_wd_autumn'],
                  "speed_wd_autumn": +row['speed_wd_autumn'],
                  "vol_wd_summer": +row['vol_wd_summer'],
                  "occ_wd_summer": +row['occ_wd_summer'],
                  "speed_wd_summer": +row['speed_wd_summer'],
                  "vol_stud_autumn": +row['vol_stud_autumn'],
                  "occ_stud_autumn": +row['occ_stud_autumn'],
                  "speed_stud_autumn": +row['speed_stud_autumn'],
                  "vol_holi": +row['vol_holi'],
                  "occ_holi": +row['occ_holi'],
                  "speed_holi": +row['speed_holi'],
                  "vol_wkd_autumn": +row['vol_wkd_autumn'],
                  "occ_wkd_autumn": +row['occ_wkd_autumn'],
                  "speed_wkd_autumn": +row['speed_wkd_autumn'],
                  "lat": currLat,
                  "long": currLong,
                  "street": currStreet
                })
              }
          })

          const step = x => {
            if (this.index == 23) {
              this.index = 0
            } else {
              this.index++;
            }

            update(parsedData)
            printData(parsedData)
          }

          const stepBack = x => {
            if (this.index == 0) {
              this.index = 23
            } else {
              this.index--;
            }
            
            update(parsedData)
            printData(parsedData)
          }

          const justUpdate = x => {
            update(parsedData)
          }

          this.interval = setInterval(step, 130);

          $('#minusOne')
            .on('click', x => {
              event.preventDefault();
              stepBack()
            })

          $('#plusOne')
            .on('click', x => {
              event.preventDefault();
              step()
            })

          $('#play-pause-button')
            .on('click', x => {
              event.preventDefault();
              button = $('#play-pause-button');

              if (this.running) {
                clearInterval(this.interval);
                button.text('Resume');
                this.running = false;

                // d3.select("#map")
                //   .select("svg")
                //     .attr("style", "pointer-events: auto;")
                // map.panTo(new L.LatLng(54.70, 25.26));

              } else {
                this.interval = setInterval(step, 130);
                button.text('Pause');
                this.running = true;

                // d3.select("#map")
                //   .select("svg")
                //     .attr("style", "pointer-events: none;")
                // map.panTo(new L.LatLng(54.70, 25.26));

              };
            });



          $('#metric-selection')
            .on('change', x => {
              this.metric = $('#metric-selection').val()
              if (!this.running) {
                justUpdate()
              }
            }
          );

          $('#subset-selection')
            .on('change', x => {
              this.subset = $('#subset-selection').val()
              if (!this.running) {
                justUpdate()
              }
            }
          );

          // $(document).keydown(e => {
          //   if (!this.running && e.which == 37) {
          //     document.getElementById('minusOne').click()
          //   } else if (!this.running && e.which == 39) {
          //     document.getElementById('plusOne').click()
          //   } 
          // });

          $(document).keydown(e => {
            if (e.which == 32) {
              document.getElementById('play-pause-button').click()
            } 
          })

    
      })
    }
  },
  mounted() {
    clearInterval(this.interval)
    this.plot()
  },
  computed: {
    hours() {
      if (this.index < 10) {
        return '0' + this.index + ':00'
      } else {
        return this.index + ':00'
      }
    }
  },
  filters: {
    round(val) {
      return Math.round(val)
    }
  } 
}
</script>

<style>

  @import url('https://fonts.googleapis.com/css?family=Montserrat&display=swap');
  @import url('https://fonts.googleapis.com/css?family=Orbitron&display=swap');

  /* @media screen and (max-width: 1600px) {
    #controls-div {
      flex-direction: column;
      height: 50vh !important;
      width: 100%;
    }

    #details-div {
      justify-content: center !important;
    }
  } */

  body {
    background: #f0f8ff;
    font-family: 'Montserrat', sans-serif;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    color: #133337;
  }

  #nav {
    height: 5vh;
    width: 100%;
    color: #f0f8ff;
    background: #133337;
  }

  #navbar-contents {
    display: flex;
    width: 100%;
    height: 100%;
    padding: 0 2rem;
    max-width: 1600px;
    margin: 0 auto;
    align-items: center;
    justify-content: space-between;
  }

  #navbar-contents #header-div {
    color: #ff0000;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  #navbar-contents #header-div h1, #navbar-contents #header-div h3 {
    margin: 0;
    padding: 0;
  }

  #navbar-contents #header-div h1 {
    font-size: 1.25rem;
  }

  #navbar-contents #header-div h3 {
    font-size: .75rem;
    color: #f0f8ff;
  }

  #map-div {
    height: 70vh;
    width: 100%;
    position: relative;
  }

  #map-div #map {
    height: 100%;
  }

  #controls-div {
    height: 20vh;
    background: #eeeeee;
    margin: 0;
  }

  #controls-content {
    display: flex;
    justify-content: space-around;
    align-items: center;
    color: #133337;
    width: 100%;
    height: 100%;
    max-width: 1600px;
    margin: 0 auto;
    padding: 0 2rem;
  }

  #select-data-div {
    flex: 2;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }


  #select-metric-div, #select-subset-div {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  #select-metric-div label, #select-metric-div select, #select-subset-div label, #select-subset-div select {
    margin-bottom: 0.5rem;
  }

  #select-metric-div select, #select-subset-div select {
    width: 17rem;
    font-family: 'Montserrat', sans-serif;
  }

  #clock-div {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-family: 'Orbitron', sans-serif;
    color: #ff0000;
  }

  #hour-div {
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 3rem;
  }

  #hour-div h2 {
    padding: 0 1rem;
    margin: 0
  }

  #play-pause-button {
    font-family: 'Montserrat', sans-serif;
    display: block;
    color:#f0f8ff;
    background: #ff0000;
    border-radius: .25rem;
    text-align: center;
    padding: .25rem;
    width: 5rem;
    text-decoration: none;
    transition: background .2s;
  }

  #play-pause-button:hover {
    transition: background .2s;
    background: #cc0000
  }

  #details-div {
    flex: 2;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  #details-div p {
    text-align: center;
  }

  #details-div ul {
    list-style-type: none;
    padding-right: 1rem;
  }

  .strong {
    color:#ff0000;
    text-decoration: none;
  }

  .control-btn {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 1.3rem;
    display: block;
    width: 2rem;
    height: 2rem;
    line-height: 2rem;
    border-radius: .5rem;
    background: #ff0000;
    color: #f0f8ff;
    text-align: center;
    transition: background .2s;
    cursor: pointer;
    text-decoration: none;
    -webkit-user-select: none;    
    -moz-user-select: none; 
    -ms-user-select: none; 
  }

  .control-btn:hover {
    background: #cc0000;
    transition: background .2s;
  }

  #footer {
    background: #133337;
    width: 100%;
    height: 5vh;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  #footer p {
    margin: 0;
    color: #f0f8ff;
  }

</style>
