<template>
  <div>
    <svg id = "Epoch"  class="epoch" style = 'width:400px; height:340px'> 
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
  props:["day"],
  data(){
    return {
      epochs:[],
      width: 400,
      height: 340,
      margin:{
        top:30,
        right:10,
        bottom:0,
        left:30
      },
      r:15,
      c:15
    };
  },
  mounted(){

  },
  computed:{
    index(){
      console.log(this.day);
      return this.day;
    },
    epoch(){
      return this.epochs;
    },
    innerWidth(){
      return this.width - this.margin.left - this.margin.right
    },
    innerHeight(){
      return this.height - this.margin.top - this.margin.bottom
    }
  },
  methods:{
     getEpoch(){
       const path = 'http://127.0.0.1:5000/EpochView/' + eval(this.day);
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
    let that = this;
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
                  .on("click", function(){                   
                    var temp = d3.select(this).data();
                    that.$emit('details',temp[0].epoch);
                  })     
		 
     //var [a,b] = d3.extent(record, function(d){return d.minTemp;});//max时choice=MaxTemp
		 
		 function color() {
			 return d3.scaleLinear([a, b], function (t){return d3.interpolateReds(t);}); 
		 } 
    d3.select("#legend")
		   .append("g").attr("id","legend")
       .call(that.colorbox,[450,20],d3.scaleLinear([a, b], function (t){return d3.interpolateReds(t);}))
		   .attr("transform","translate(5,0)")
		 //创建图例
		 
		 d3.select("#legend")
		   .append("g")
		   .call(d3.axisBottom(d3.scaleLinear().domain([b,a]).range([450,0])).ticks(5))
		   .attr("transform","translate(5,20)")
		 d3.select("#legend") 
		   .append("text")
		   .text("/%C").attr("transform","translate(450,35) scale(0.5)")
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
   },

  colorbox(sel, size, colors){
    var [x0,x1] = d3.extent( colors.domain());
    var bars = d3.range( x0, x1, (x1-x0)/size[0]);
    var sc = d3.scaleLinear()
        .domain([x0,x1]).range( [0, size[0]]);
    sel.selectAll("line").data(bars).enter().append("line")
      .attr( "x1", sc).attr( "x2",sc)
      .attr( "y1", 0).attr("y2",size[1])
      .attr("stroke",colors);
    
    sel.append("rect")
        .attr("width",size[0]).attr("height",size[1])
        .attr("fill","none").attr("stroke","black")
		 },

  Legend(){
    var [a,b] = d3.extent(record, function(d){return d.minTemp;});//max时choice=MaxTemp
		 
		function color() {
		    var med = d3.median([a,b]);
			 return d3.scaleDiverging([a, med, b], function (t){return d3.interpolatePuBu(t);}); 
		}
    d3.select("#legend")
		   .append("g").attr("id","legend")
       .call( colorbox,[450,20],colorM())
		   .attr("transform","translate(5,0)")
		 //创建图例
		 
		 d3.select("#legend")
		   .append("g")
		   .call(d3.axisBottom(d3.scaleLinear().domain([b,a]).range([450,0])).ticks(5))
		   .attr("transform","translate(5,20)")
		 d3.select("#legend") 
		   .append("text")
		   .text("/%C").attr("transform","translate(450,35) scale(0.5)")
   }
  },
  created(){
    this.getEpoch();
  },
  watch:{
    epoch(){
      this.Scale();
      this.GHOST();
    },
    index(){
      this.getEpoch();
      console.log("day changed")
      console.log(this.epochs)
      this.Scale();
      this.GHOST();
    }
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
    top:600px;
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
    top:600px;
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
