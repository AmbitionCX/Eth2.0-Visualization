<template>
  <div class="dynamic-visualization">
    <div class="container">
      <div class="narrow">
        <div>You have selected {{ dotNum }} points.</div>
        <br />
        <div class="distribution-container">
          <svg id="x-slice"></svg>
        </div>
        <div class="distribution-container">
          <svg id="y-slice"></svg>
        </div>
      </div>
      <div class="wide">
        <div id="dynamic-vis-container">
          <svg id="dynamic-scatter"></svg>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="js">
import * as d3 from "d3"
import { drawScatter, search } from "@/assets/js/quadtree.js"
import { drawHist } from "@/assets/js/histogram.js"
import { mapGetters } from 'vuex'

export default {
    name: "Dynamic-Visualization",
    components: {

    },
    data() {
        return {
          dotNum: 0
        }
    },
    computed: {
        ...mapGetters([
            'dataset', // map global dataset into local data
            'bell'
            // ...
        ]),
        svg() {
            return d3.select('#dynamic-scatter')
        }
    },
    created() {
        // when the page is created, request global data
        this.$store.dispatch('getScatterDataset')
    },
    mounted() {
        let bbox = d3.select('#dynamic-vis-container').node().getBoundingClientRect()
        this.svg.attr('height', bbox.height).attr('width', bbox.width).attr('viewBox', `0 0 800 800`)
        let smBbox = d3.select('.distribution-container').node().getBoundingClientRect()
        d3.selectAll('.distribution-container').select('svg').attr('width', smBbox.width).attr('height', smBbox.height)
    },
    watch: {
        // watch changes on the dataset
        dataset(newDataset, oldDataset) {
            let self = this
            if(newDataset.length == 0) return
            console.log('Dataset Changed!', newDataset.length, oldDataset.length)
            let { point, quadtree } = drawScatter(this.svg, newDataset)
            let brush = d3.brush().on("brush end", (event) => self.brushed(event, point, quadtree));
            this.svg.append("g")
            .attr("class", "brush")
            .call(brush)
            .call(brush.move, [[100, 100], [200, 200]]);
        },
        bell(nv) {
          let focus = this.$store.getters.focus
          if(nv === 0) return
          this.dotNum = focus.length
          drawHist(d3.select('#x-slice'), focus.map(v => v[0]), 'X')
          drawHist(d3.select('#y-slice'), focus.map(v => v[1]), 'Y')
        }
    },
    methods: {
        brushed({ selection: extent }, point, quadtree) {
            point.each(d => (d.scanned = d.selected = d.grandfathered = false))
            if (extent)
            search(quadtree, extent[0][0], extent[0][1], extent[1][0], extent[1][1])
            point.classed("point--scanned", d => d.scanned)
            point.classed("point--selected", d => d.selected)
            point.classed("point--grandfathered", d => d.grandfathered)
            this.$store.dispatch('notify')  // tell others to update view
        }
    }

}
</script>

<style lang="scss">
.dynamic-visualization {
  .container {
    width: 100%;
    display: flex;
    .narrow {
      width: 40%;
      padding: 10px;
    }
    .wide {
      width: 60%;
      padding: 10px;
    }
  }
  .distribution-container {
    height: 40vh;
    width: 100%;
  }
  #dynamic-vis-container {
    height: 80vh;
    width: 100%;
  }
  .point {
    fill: #000;
    fill-opacity: 0.4;
  }

  .point--scanned {
    fill: orange;
    fill-opacity: 1;
    stroke: red;
    stroke-width: 3px;
  }

  .point--selected {
    fill: blue;
    fill-opacity: 1;
    stroke: blue;
    stroke-width: 5px;
  }

  .point--grandfathered {
    fill: steelblue;
    fill-opacity: 1;
    stroke: steelblue;
    stroke-width: 1px;
  }

  .node {
    fill: none;
    stroke: #ccc;
    shape-rendering: crispEdges;
  }
}
</style>
