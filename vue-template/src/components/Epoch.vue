  <template>
<div>
  <svg id = "mainsvg" style = 'width:4200px; height:3600px'>

  </svg>
      <button id = 'ghost' style = 'appearance: none;
    background-color: #2ea44f;
    border: 1px solid rgba(27, 31, 35, .15);
    border-radius: 6px;
    box-shadow: rgba(27, 31, 35, .1) 0 1px 0;
    box-sizing: border-box;
    color: #fff;
    cursor: pointer;
    display: inline-block;
    font-family: -apple-system,system-ui,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji";
    font-size: 56px;
    font-weight: 1200;
    line-height: 80px;
    padding: 24px 64px;
    position: relative;
    text-align: center;
    text-decoration: none;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
    vertical-align: middle;
    white-space: nowrap'
    @click = 'Casper()'>Head</button>
</div>

</template>

<script>
import axios from 'axios'
import * as d3 from 'd3'

export default {
  name:'Epoch',
  data(){

    return {
      epochs:[],
      width: 2000,
      height: 1750,
      margin:{
        top:100,
        right:90,
        bottom:60,
        left:90
      },
      r:15,
      c:15
    };
  },
  mounted(){
    this.Scale();
  },
  computed:{
    innerWidth(){
      return this.width - this.margin.left - this.margin.right
    },
    innerHeight(){
      return this.height - this.margin.top - this.margin.bottom
    }
  },
  methods:{
     getEpoch(){
       const path = 'http://127.0.0.1:5000/overview';
       axios
         .get(path)
         .then(res => {
           this.epochs=res.data;
         })
         .catch(error => {
           console.error(error);
         });
     },
     Scale(){
      const g = d3.select('svg').append('g').attr('id', 'maingroup')
                   .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
      const xscale = d3.scaleLinear()
                       .domain([0,this.c])
                       .range([0, this.innerWidth]);
      const yscale = d3.scaleLinear()
          .domain([0,this.r])
          .range([0, this.innerHeight]);

      const yaxis = d3.axisLeft(yscale)
          .ticks(this.r)
          .tickSize(10)
          .tickPadding(10);
      const xaxis = d3.axisBottom(xscale)
          .ticks(this.c)
          .tickSize(-10)
          .tickPadding(-50);
          g.append('g').call(yaxis)
    .attr('id' ,'yaxis');
  g.append('g').call(xaxis)
    .attr('id', 'xaxis');
  },
  Casper(){
    const c = this.c;
    var [a,b] = d3.extent(this.epochs, function(d){return d['attesting_balance'] - d['target_correct_balance'];})
    const xscale = d3.scaleLinear()
                       .domain([0,this.c])
                       .range([0, this.innerWidth]);
    const yscale = d3.scaleLinear()
          .domain([0,this.r])
          .range([0, this.innerHeight]);
    d3.select('g').selectAll('rect').data(this.epochs).enter()
                  .append('rect')
                  .attr('fill', function(d){return d3.interpolateReds((d['attesting_balance'] - d['target_correct_balance']-a)/(b-a) )})
                  .attr('width', this.innerWidth/15-20)
                  .attr('height', this.innerHeight/15-20)
                  .attr("transform", function(d, i) { // bug: d and i lack number 0 and 1 in pies_data
                  console.log(c)
            return `translate(${xscale(Math.floor((i)%c))+10},${yscale(Math.floor((i)/c))+10})`;
                  })
  }
  },
  created(){
    this.getEpoch();
  },
  watch:{

  }
};
</script>

<style scoped>
.panel-header {
  position: relative;
  padding: 0 8px;
  width: 250px;
  height: 40px;
  line-height: 40px;
  font-size: 24px;
  background: #455a64;
  color: #fcfcfc;
  display: flex;
  font-weight: bold;
  border-radius: 2px;
  box-shadow: 0 1px 2px rgba(26 26 26 0.2);
}

.panel-header-end {
  position: absolute;
  top: 0px;
  left: 250px;
  border-top: 40px solid #455a64;
  border-right: 45px solid #ffffff;
  border-bottom: 3px solid #ffffff;
}

.ant-table-selected :deep(.table-selected) td {
  background-color: #fafafa;
}
</style>
