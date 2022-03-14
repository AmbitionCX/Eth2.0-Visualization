<template>
  <div>
    <svg id = "Epoch"  class="epoch" style = 'width:400px; height:350px'> 
    </svg>
    <button id = 'ghost' @click = 'GHOST()'>Head</button>
    <button id = 'casper' @click = 'Casper()'>Checkpoint</button>
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
      width: 400,
      height: 350,
      margin:{
        top:30,
        right:10,
        bottom:10,
        left:30
      },
      r:15,
      c:15,
      msg:0
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
       const path = 'http://127.0.0.1:5000/EpochView';
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
      const g = d3.select('#Epoch').append('g').attr('id', 'epochview')
                  .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
      const xscale = d3.scaleLinear()
                       .domain([0,this.c])
                       .range([0, this.innerWidth]);
      const yscale = d3.scaleLinear()
          .domain([0,this.r])
          .range([0, this.innerHeight]);

      const yaxis = d3.axisLeft(yscale)
          .ticks(this.r)
          .tickSize(5)
          .tickPadding(10);
      const xaxis = d3.axisBottom(xscale)
          .ticks(this.c)
          .tickSize(-5)
          .tickPadding(-20);
          g.append('g').call(yaxis)
    .attr('id' ,'yaxis');
  g.append('g').call(xaxis)
    .attr('id', 'xaxis');
  },

  GHOST(){
    d3.select('#epochview').selectAll('rect').remove()
    const c = this.c;
    var [a,b] = d3.extent(this.epochs, function(d){return d['active_balance'] - d['head_correct_balance'];})
    const xscale = d3.scaleLinear()
                       .domain([0,this.c])
                       .range([0, this.innerWidth]);
    const yscale = d3.scaleLinear()
          .domain([0,this.r])
          .range([0, this.innerHeight]);
    d3.select('#epochview').selectAll('rect').data(this.epochs).enter()
                  .append('rect')
                  .attr('fill', function(d){return d3.interpolateReds((d['active_balance'] - d['head_correct_balance']-a)/(b-a) )})
                  .attr('width', this.innerWidth/15-5)
                  .attr('height', this.innerHeight/15-5)
                  .attr("transform", function(d, i) {
            return `translate(${xscale(Math.floor((i)%c))+2.5},${yscale(Math.floor((i)/c))+2.5})`;
                  })
  },


  Casper(){
    let that = this;
    d3.select('#epochview').selectAll('rect').remove()
    const c = this.c;
    var [a,b] = d3.extent(this.epochs, function(d){return d['active_balance'] - d['target_correct_balance'];})
    const xscale = d3.scaleLinear()
                       .domain([0,this.c])
                       .range([0, this.innerWidth]);
    const yscale = d3.scaleLinear()
          .domain([0,this.r])
          .range([0, this.innerHeight]);
    d3.select('#epochview').selectAll('rect').data(this.epochs).enter()
                  .append('rect')
                  .attr('fill', function(d){return d3.interpolateReds((d['active_balance'] - d['target_correct_balance']-a)/(b-a) )})
                  .attr('width', this.innerWidth/15-5)
                  .attr('height', this.innerHeight/15-5)
                  .attr("transform", function(d, i) {
                  console.log(c)
            return `translate(${xscale(Math.floor((i)%c))+2.5},${yscale(Math.floor((i)/c))+2.5})`;
                  })
                  .on("click", function(){                   
                    var temp = d3.select(this).data();
                    that.$emit('details',temp[0].epoch);
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
#ghost {
    appearance: none;
    background-color: #2ea44f;
    border: 1px solid rgba(27, 31, 35, .15);
    border-radius: 1px;
    box-shadow: rgba(27, 31, 35, .1) 0 1px 0;
    box-sizing: border-box;
    color: #fff;
    cursor: pointer;
    display: inline-block;
    font-family: -apple-system,system-ui,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji";
    font-size: 10px;
    font-weight: 1200;
    line-height: 10px;
    padding: 5px 5px;
    position: absolute;
    top:0;
    left:285px;
    text-align: center;
    text-decoration: none;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
    vertical-align: middle;
    white-space: nowrap;
}
#casper{
    appearance: none;
    background-color: #2ea44f;
    border: 1px solid rgba(27, 31, 35, .15);
    border-radius: 1px;
    box-shadow: rgba(27, 31, 35, .1) 0 1px 0;
    box-sizing: border-box;
    color: #fff;
    cursor: pointer;
    display: inline-block;
    font-family: -apple-system,system-ui,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji";
    font-size: 10px;
    font-weight: 1200;
    line-height: 10px;
    padding: 5px 5px;
    position: absolute;
    top:0;
    left:330px;
    text-align: center;
    text-decoration: none;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
    vertical-align: middle;
    white-space: nowrap;
}
</style>
