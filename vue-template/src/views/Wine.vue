<template>
  <div class="wine">
    <div class="container">
      <div class="narrow">
      <p>
      A simple scatter plot with quadtree search for brush.
      </p>
      </div>
      <div class="wide">
      <div id="heatmap">
            </div>
      </div>
    </div>
  </div>
</template>

<script lang="js">
import * as d3 from "d3"
import { drawMatrix } from "@/assets/js/heatmap.js"
// import { mapGetters } from 'vuex'

export default {
    name: "Wine",
    components: {

    },   
    data() {
        return {
        }
    },
    computed: {
    },
    created() {
    },
    mounted() {
       d3.csv('./dataset/wine_matrix.csv').then(function(data) {
           drawMatrix(data)
       })

    },
    watch: {
    },
    methods: {
       
    }

}
</script>

<style lang="scss">
.wine {
    .container {
    width: 100%;
    display: flex;
    }
    .narrow {
        width: 40%;
        padding: 10px;
    }
    .wide {
        width: 60%;
        padding:10px;
    }

    #heatmap {
        width: 100%;
        height: 80vh;
    }
    svg {
        font: 12px sans-serif;
        text-anchor: middle;
    }
    rect {
        stroke: lightgray;
        stoke-width: 3 px;
        fill: none;
    }
    
    .y.axis path{
        fill: none;
        stroke: none;
    }

    text.active{
        fill: "red";
    }
}
</style>
