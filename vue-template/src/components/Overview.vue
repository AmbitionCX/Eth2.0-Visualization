<template>
  <div class="overview">
    <button @click='Draw(dayData)'>Hi</button>
    <svg id = "mainsvg" style = 'width:4200px; height:3600px'>
 
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
      width: 2000,
      height: 1750,
      margin:{
        top:100,
        right:90,
        bottom:60,
        left:90
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
    innerWidth(){
      return this.width - this.margin.left - this.margin.right
    },
    innerHeight(){
      return this.height - this.margin.top - this.margin.bottom
    },
    dayData(){
      let day = this.all
      day.forEach(d =>{
        d["date"] = new Date(d['day']).getDate();
        d["month"] = new Date(d['day']).getMonth();
        d["year"] = new Date(d['day']).getFullYear();
    })
    return day
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
     show(data){
       console.log(data);
     },
 
  Color(num){
    let that = this;
    const color = d3.scaleLinear()
                    .domain([d3.min(that.dayData,function(d){return d["canonical"]}),
                             d3.max(that.dayData,function(d){return d["canonical"]})])
                    .range([0, 1]);
    return color(num)
  },
  Draw(){
    
for (let i =0; i < this.dayData.length; i++){
    this.dayData[i]['color'] = this.Color(this.dayData[i]["canonical"])}


var dayDatas=[[],[],[]]
dayDatas[0] = this.dayData.filter(d =>{
        return d["year"]==2020;
})
dayDatas[1] = this.dayData.filter(d =>{
        return d["year"]==2021;
})
dayDatas[2] = this.dayData.filter(d =>{
        return d["year"]==2022;
})
console.log(dayDatas[0])
console.log(dayDatas[1])
console.log(dayDatas[2])
 

for (let k=0; k<3;k++){

var rawdeposits = [];

var allmonths = Array.from(new Set(dayDatas[k].map(d => {
        return d["month"];
      })));
        
allmonths.forEach(function(){
        let b = [];
        for(let i =0; i<31;i++){ b.push([]);}
        rawdeposits.push(b);
        })
var deposits = rawdeposits

dayDatas[k].forEach(d => {
        for (let i=0;i<d["deposits"].length;i++){
        deposits[allmonths.indexOf(d['month'])][d["date"]-1].push(d["deposits"][i]);
}})

console.log(deposits)
let that = this;
const width = 1400//(+svg.attr('width');
const height = 45*allmonths.length//(+svg.attr('height');
const margin = { top: 30, right: 60, bottom: 30, left: 55 };
const innerWidth = width - margin.left - margin.right;
const innerHeight = height - margin.top - margin.bottom;
const g = d3.select('#mainsvg').append('g').attr('id', 'maingroup')
              .attr('transform', `translate(${margin.left},${margin.top+height*k})`);

              const xscale = d3.scaleLinear()
.domain([0,31])
.range([0, innerWidth]);

const yscale = d3.scaleBand().
        domain(allmonths.map(d => that.MONTHS[d])).
        range([0, innerHeight]);


const yaxis = d3.axisLeft(yscale)
        .tickSize(5)
        .tickPadding(20);
const xaxis = d3.axisBottom(xscale)
        .ticks(31)
        .tickSize(-5)
        .tickPadding(-20);

g.append('g').call(yaxis).attr('id' ,'yaxis');

g.append('g').call(xaxis).attr('id', 'xaxis');

console.log(dayDatas[k])

g.selectAll('.datarect').data(dayDatas[k]).enter().append('rect')
.attr('class', 'datarect')
.attr('width', 25)
.attr('height', 25)
.attr('y', d => (yscale(that.MONTHS[d['month']]))+12.5)
.attr('x', d => (xscale(d['date'])) -12.5)
.attr('fill', d => d3.interpolateYlOrRd((d['color']))).
attr('opacity', 0.9)

for (let i = 0; i < deposits.length; i++) {
    for (let j = 0; j < deposits[i].length; j++) {
                const xscale2 = d3.scaleLinear()
                .domain([0,254])
                .range([0, 25]);

                const yscale2 = d3.scaleLinear().
                domain([d3.max(deposits[i][j],function(d){
                        return d}),d3.min(deposits[i][j],function(d){return d})])
                        .range([0, 25]);

                const line = d3.line()
                .x(function (d, i) {return xscale2(i);})
                .y(function (d) {return yscale2(d);});

                d3.select('g')
                .append('g')
                .attr('transform', function () {
                return `translate(${xscale(j+1) -12.5},${yscale(that.MONTHS[allmonths[i]]) +12.5+height*k})`;
                })
                .append('path')
                .datum(deposits[i][j])
                .attr('class', 'linestyle')
                .attr("fill", "none")
                .attr("stroke", "brown")
                .attr("stroke-width", 0.3)
                .attr("d", line)
        }
      }}
      

  }

  },
  created(){
    this.getAll();
  },
  watch:{

  }
};
</script>

<style>
.overview {
  position: sticky;
  top: 100px;
  background: #ffffff;
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
