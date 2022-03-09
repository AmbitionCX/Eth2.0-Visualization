<template>
  <div class="static-visualization">
    <h2>A simple scatter plot with quadtree search for brush.</h2>
    <div id="vis-container">
      <svg id="scatter"></svg>
    </div>
  </div>
</template>

<script lang="js">
import * as d3 from "d3"
import { drawScatter, search } from "@/assets/js/quadtree.js"

export default {
    name: "Static-Visualization",
    components: {

    },
    data() {
        return {

        }
    },
    mounted() {
        let bbox = d3.select('#vis-container').node().getBoundingClientRect()
        let svg = d3.select('#scatter').attr('height', bbox.height).attr('width', bbox.width)
        let self = this
        d3.json('./dataset/dot_data.json').then(function(dotData){
            let { point, quadtree } = drawScatter(svg, dotData)
            let brush = d3.brush().on("brush end", (event) => self.brushed(event, point, quadtree));
            svg.append("g")
            .attr("class", "brush")
            .call(brush)
            .call(brush.move, [[100, 100], [200, 200]]);
        })

    },
    methods: {
        brushed({ selection: extent }, point, quadtree) {
            console.log({selection: extent})
            point.each(d => (d.scanned = d.selected = d.grandfathered = false));
            if (extent)
            search(quadtree, extent[0][0], extent[0][1], extent[1][0], extent[1][1]);
            point.classed("point--scanned", d => d.scanned);
            point.classed("point--selected", d => d.selected);
            point.classed("point--grandfathered", d => d.grandfathered);
        }
    }

}
</script>

<style lang="scss">
.static-visualization {
  text-align: middle;
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
#vis-container {
  height: 80vh;
  width: 99vw;
  text-align: middle;
}
</style>
