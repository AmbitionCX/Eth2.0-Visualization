<template>
  <div>
    <svg id = "Slot" style = 'width:1200px; height:850px'></svg>
  </div>
</template>

<script>
import axios from 'axios'
import * as d3 from 'd3'

export default {
  name:'Slot',
  props:["msg"],
  data(){

    return {
      slots:[],
      links:[],
      width: 1200,
      height: 850,
      margin:{
        top:150,
        right:10,
        bottom:500,
        left:10
      },
      c:33
    };
  },
  mounted(){
    this.xScale();
  },
  computed:{
    slot(){
      console.log(this.slots);
      return this.slots
    },
    message(){
      console.log(this.msg)
      return this.msg
    },
    innerWidth(){
      return this.width - this.margin.left - this.margin.right
    },
    innerHeight(){
      return this.height - this.margin.top - this.margin.bottom
    }
  },
  methods:{
     getSlot(){
       const path = 'http://127.0.0.1:5000/slot/' + eval(this.msg);
       console.log(path);
       axios
         .get(path)
         .then(res => {
           console.log(res);
           this.slots=res.data[0];
           this.links = res.data[1]
         })
         .catch(error => {
           console.error(error);
         });
     },

     xScale(){
      const g = d3.select('#Slot').append('g').attr('id', 'slotview')
                   .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
      const xscale = d3.scaleLinear()
                       .domain([-1,this.c])
                       .range([0, this.innerWidth]);

      const xaxis = d3.axisBottom(xscale)
        .ticks(34)
        .tickSize(-10)
        .tickPadding(20)
        .tickFormat(function(d,i){return (i < 33 && i > 0) ? (i-1):"";});
        
       g.append('g').call(xaxis)
        .attr('id', 'xaxis')
        .selectAll('text')
        .attr('transform',`translate(${this.innerWidth/68},${0})`)
        .attr('font-size', '14px');
     },

     drawBlockheader(){
       console.log("drawSlots")
      let that = this;
      const xscale = d3.scaleLinear()
                       .domain([-1,this.c])
                       .range([0, this.innerWidth]);
      var [a,b] = d3.extent(that.slots, function(d){return d.at_number;})
      console.log([a,b]);
      var distribute = d3.scaleLinear().domain([a,b]).range([10, this.innerWidth/34]);

      var [m,n] = d3.extent(d3.filter(that.slots, x=>x.block_header !=0), function(d){return d.block_header})
      var opaci = d3.scaleLinear().domain([m,n]).range([0.1, 1]);

     d3.select('#slotview').append('g').attr('id','block_header')
        .selectAll('rect').data(that.slots).enter()
        .append('rect')
        .attr('transform',function(d,i){
        return `translate(${xscale(i)+that.innerWidth/68-distribute(d.at_number)/2}, ${-distribute(d.at_number)/2})`;
        })
        .attr('width', function(d){
          return d.at_number == 0? 0 : distribute(d.at_number);} )//长宽待定
        .attr('height', function(d){
          let hei = d.at_number == 0? 0 : distribute(d.at_number)
          return hei/2;})
        .attr('fill', function(d){return d3.interpolateGreys(opaci(d.block_header))})
        .attr('opacity', 0.9)
     },

     drawCasper(){
      let that=this;
      const xscale = d3.scaleLinear()
                       .domain([-1,this.c])
                       .range([0, this.innerWidth]);
      var [a,b] = d3.extent(that.slots, function(d){return d.at_number;})
      console.log([a,b]);
      var distribute = d3.scaleLinear().domain([a,b]).range([10, this.innerWidth/34]);
      var [h,q] = d3.extent(d3.filter(that.slots, x=>x.block_header !=0), function(d){return d.casper_balance;})
      var cas_opa = d3.scaleLinear().domain([h,q]).range([0.2, 1]);

      d3.select('#slotview').append('g').attr('id','casper_balance')
        .selectAll('rect').data(that.slots).enter()
        .append('rect')
        .attr('transform',function(d,i){
        return `translate(${xscale(i)+that.innerWidth/68-distribute(d.at_number)/2}, ${0})`;
        })
        .attr('width', function(d){
          return d.at_number == 0? 0 : distribute(d.at_number);} )//长宽待定
        .attr('height', function(d){
          let hei = d.at_number == 0? 0 : distribute(d.at_number)
          return hei/2;})
        .attr('fill', function(d){return d3.interpolateGreys(d.block_header == 0? 0.1:cas_opa(d.casper_balance))})
        .attr('opacity', 0.9)
     },

     drawExBlocks(){
      console.log("drawBlocks");
      var ex_block = this.innerWidth/50;  
      const xscale = d3.scaleLinear()
                  .domain([-1,this.c])
                  .range([0, this.innerWidth]);
      let that = this;

      for(let j = 0; j < that.slots.length; j++){
          var [u,v] = d3.extent(that.slots[j]['ex_blocks'])
          var dis = d3.scaleLinear().domain([u,v]).range([0.1, 1]);
          d3.select('#slotview').append('g').attr('id','ex_block'+j).selectAll('rect')
          .data(that.slots[j]['ex_blocks']).enter()
              .append('rect')
          .attr('transform',function(d,i){
              return `translate(${xscale(j)+that.innerWidth/68-ex_block/2},${-i*(ex_block+10)-that.innerWidth/34-20})`;
              })
          .attr('width', ex_block)
          .attr('height', ex_block)
          .attr('fill',function(d){return d3.interpolateBlues(dis(d));})
          .attr('opacity',0.9)
          }
     },
     arc(lines){
        const xscale = d3.scaleLinear()
                       .domain([-1,this.c])
                       .range([0, this.innerWidth]);

        const x1 = xscale(lines.source)+this.innerWidth/68;
        const x2 = xscale(lines.target)+this.innerWidth/68;
        const r = Math.abs(x2 - x1) / 2;
      return `m${x1},${this.innerWidth/34}A${r},${r} 0,1,0 ${x2},${this.innerWidth/34}`;
     },

     drawArc(){
      let that = this;
      var [e,f] = d3.extent(that.links, function(d){return d.value;})
      console.log([e,f]);
      var thickness = d3.scaleLinear().domain([e,f]).range([1, 20]);

      d3.select('#slotview').append('g').attr('id','inclusion_delay').attr('fill','none')
          .selectAll("path")
          .data(that.links).enter()
          .append("path").attr("d",that.arc).attr("stroke-width", function(d){return thickness(d.value);})
          .attr("stroke", "blue")

     }
  },

  created(){
    this.getSlot();
  },
  watch:{
    slot(){
      console.log('slot changed')
        this.xScale();
        this.drawArc();
        this.drawBlockheader();
        this.drawCasper();
        this.drawExBlocks();
    },
    message(){
        this.getSlot();
        d3.select('#Slot').selectAll('g').remove()
        console.log("draw");
      }
    }

}
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
