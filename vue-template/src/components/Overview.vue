<template>
  <div class="overview">
   
    <svg id = "Overview" style = 'width:800px; height:400px'>
 
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
      width: 800,//1220,
      height: [22],
      margin:{
        top:0,
        right:80,
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
    const [a,b] = d3.extent(that.day, function(d){return d['canonical'];})
    const color =d3.scaleDivergingSymlog([a,0.8*a+0.2*b,b], function(t){return d3.interpolateYlOrRd(t);})
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

    //that.height.push(25 * allmonths.length)
    that.height.push(23 * allmonths.length)

    const yscale = d3.scaleBand()
                     .domain(allmonths.map(d => that.MONTHS[d]))
                     .range([0, that.innerHeight])

    const yaxis = d3.axisLeft(yscale)

    const xaxis = d3.axisTop(xscale)
            .ticks(31)
            .tickPadding(5);

    g.append('g').call(yaxis).attr('id' ,'yaxis');

    g.append('g').call(xaxis).attr('id', 'xaxis');

   // let rectwid = 20
    let rectwid = 16
    g.selectAll('.datarect'+ k).data(that.dayData[k]).enter().append('rect')
     .attr('class', 'datarect'+k)
     .attr('width', rectwid)
     .attr('height', rectwid)
     .attr('y', function(d){return yscale.step()*(allmonths.indexOf(d['month'])+0.5) - rectwid/2 }) 
     .attr('x', d => (xscale(d['date'])-rectwid/2))
     .attr('fill', d => that.Color(d["canonical"]))
     .attr('opacity', 0.9)
     .on("click", function(){
          var temp = d3.select(this).data();
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
    },
    
  Legend(){
    let that = this;
    var [a,b] = d3.extent(that.day, function(d){return d['canonical'];})

    d3.select("#Overview")
      .append("g").attr("id","legend_overview")
      .call(that.colorbox,[10,150],d3.scaleDivergingSymlog([a,0.8*a+0.2*b,b], function(t){return d3.interpolateYlOrRd(t);}))
      .attr("transform",`translate(${22+that.width - that.margin.right},${30})`)

    d3.select("#legend_overview")
       .append("g")
       .call(d3.axisRight(d3.scaleLinear().domain([b,a]).range([150,0])).ticks(5))
       .attr("transform","translate(10,0)")
    d3.select("#legend_overview") 
      .append("text")
      .text("Missing Blocks")
      .attr("transform","translate(-12,-10)")
      .attr("font-size","10px")
  },
  colorbox(sel, size, colors){
    var [x0,x1] = d3.extent( colors.domain());
    var bars = d3.range( x0, x1, (x1-x0)/size[1]);
    var sc = d3.scaleLinear()
        .domain([x0,x1]).range([0, size[1]]);
    sel.selectAll("line").data(bars).enter().append("line")
      .attr("x1", 0).attr("x2",size[0])
      .attr("y1", sc).attr("y2",sc)
      .attr("stroke",colors);
    
    sel.append("rect")
        .attr("width",size[0]).attr("height",size[1])
        .attr("fill","none").attr("stroke","black")
      }
  },
  created(){
    this.getAll();
},
  watch:{
    all_data(){
      for(let i=0; i < this.dayData.length-1; i++){
        this.Draw(i);
      }
      this.Legend();
    }
  }
};
</script>

<style>
</style>
