<template>
  <div class="overview">
   
    <svg id = "Overview" style = 'width:1200px; height:600px'>
 
    </svg>
    
  </div>
</template>

<script>
import axios from 'axios'
import * as d3 from 'd3'

export default {
  name:'Overview',
  data(){

    return {
      all:[],
      width: 1200,
      height: [22],
      margin:{
        top:0,
        right:60,
        bottom:0,
        left:60
      },
      r:15,
      c:15,
      MONTHS:['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November','December']

    };
  },
  mounted(){
    //this.Scale();
  },
  computed:{
    all_data(){
      return this.all
    },
    innerWidth(){
      return this.width - this.margin.left - this.margin.right
    },
    innerHeight(){
      return this.height[this.height.length-1] - this.margin.top - this.margin.bottom
    },
    day(){
      let day = this.all
      day.forEach(d =>{
        d["date"] = new Date(d['day']).getDate();
        d["month"] = new Date(d['day']).getMonth();
        d["year"] = new Date(d['day']).getFullYear();
    })
    return day
    },
    dayData(){
        let dayDatas=[[],[],[]]
        dayDatas[0] = this.day.filter(d =>{
                return d["year"]==2020;
        })
        dayDatas[1] = this.day.filter(d =>{
                return d["year"]==2021;
        })
        dayDatas[2] = this.day.filter(d =>{
                return d["year"]==2022;
        })
      return dayDatas;
    }
  },
  methods:{
     getAll(){
       const path = 'http://127.0.0.1:5000/Overview';
       axios
         .get(path)
         .then(res => {
           this.all=res.data;
         })
         .catch(error => {
           console.error(error);
         });
     },
 
  Color(num){
    let that = this;
    const color = d3.scaleSymlog()
                    .domain([d3.min(that.day,function(d){return d["canonical"]}),d3.max(that.day,function(d){return d["canonical"]})])
                    .range([0, 1]);
    return color(num)
  },
  Draw(k){
    let that = this;

   
    var rawdeposits = [];

    var allmonths = Array.from(new Set(that.dayData[k].map(d => {
            return d["month"];
          })));
            
    allmonths.forEach(function() {
            let b = [];
            for(let i =0; i<31;i++){ b.push([]);}
            rawdeposits.push(b);
            })
    var deposits = rawdeposits

    that.dayData[k].forEach(d => {
            for (let i = 0;i < d["deposits"].length; i++){
            deposits[allmonths.indexOf(d['month'])][d["date"]-1].push(d["deposits"][i]);
    }})

    var svg = d3.select('#Overview');
    const g = svg.append('g').attr("id","overview" + k)
                 .attr('transform', `translate(${that.margin.left},${d3.sum(that.height)+22*k})`);

    const xscale = d3.scaleLinear()
    .domain([0,31])
    .range([0, that.innerWidth]);

    that.height.push(25 * allmonths.length)


    const yscale = d3.scaleBand()
                     .domain(allmonths.map(d => that.MONTHS[d]))
                     .range([0, that.innerHeight])

    const yaxis = d3.axisLeft(yscale)
            // .ticks(allmonths.length)
            // .tickPadding(-45);
    const xaxis = d3.axisTop(xscale)
            .ticks(31)
            .tickPadding(5);

    g.append('g').call(yaxis).attr('id' ,'yaxis');

    g.append('g').call(xaxis).attr('id', 'xaxis');
    
    let rectwid = 20
    g.selectAll('.datarect'+ k).data(that.dayData[k]).enter().append('rect')
     .attr('class', 'datarect'+k)
     .attr('width', rectwid)
     .attr('height', rectwid)
     .attr('y', function(d){return yscale.step()*(allmonths.indexOf(d['month'])+0.5) - rectwid/2 }) 
     .attr('x', d => (xscale(d['date'])-rectwid/2))
     .attr('fill', d => d3.interpolateYlOrRd((that.Color(d["canonical"]))))
     .attr('opacity', 0.9)
     .on("click", function(){
          var temp = d3.select(this).data();
          console.log(temp)
          let a = temp[0]['day'];
          let b = "2020-12-01";
          that.$emit('day_detail',225*(new Date(a) - new Date(b))/(1*24*60*60*1000));
          })     

    for (let i = 0; i < deposits.length; i++) {
      for (let j = 0; j < deposits[i].length; j++) {
        const xscale20 = d3.scaleLinear()
                           .domain([0,254])
                           .range([0, rectwid]);

        const yscale20 = d3.scaleLinear()
                           .domain([d3.max(deposits[i][j],function(d){return d}),d3.min(deposits[i][j],function(d){return d})])
                           .range([0, rectwid]);

        const line0 = d3.line()
                        .x(function (d,i) {return xscale20(i);})
                        .y(function (d) {return yscale20(d);});

        d3.select('#overview'+k).append('g')
          .attr('transform', function () {
          return `translate(${xscale(j+1)-rectwid/2},${yscale.step()*(i+0.5) - rectwid/2})`;
          })
          .append('path')
          .datum(deposits[i][j])
          .attr('class', 'linestyle')
          .attr("fill", "none")
          .attr("stroke", "brown")
          .attr("stroke-width", 0.5)
          .attr("d", line0)
        }
      }
    }

  },
  created(){
    this.getAll();
},
  watch:{
    all_data(){
      for(let i=0; i < this.dayData.length; i++){
        this.Draw(i);
      }
    }
  }
};
</script>

<style>
</style>
