<template>
  <div>
    <svg id = "Slot" style = 'width:2000px; height:3600px'></svg>
    <text>"This is the slot view"</text>
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
      width: 2000,
      height: 1750,
      margin:{
        top:100,
        right:10,
        bottom:60,
        left:10
      },
      c:32
    };
  },
  mounted(){
    this.xScale();
  },
  beforeUpdate(){
    this.drawSlots();
    this.drawBlocks();
  },
  computed:{
    message(){
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

       const path = 'http://127.0.0.1:5000/slot/'+eval(this.msg);
       console.log(path);
       axios
         .get(path)
         .then(res => {
           this.slots=res.data;
         })
         .catch(error => {
           console.error(error);
         });
     },

     xScale(){
      const g = d3.select('#Slot').append('g').attr('id', 'slotview')
                   .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
      const xscale = d3.scaleLinear()
                       .domain([0,this.c])
                       .range([0, this.innerWidth]);

      const xaxis = d3.axisBottom(xscale)
        .ticks(32)
        .tickSize(-10)
        .tickPadding(45)
        .tickFormat(function(d,i){return i < 32 ? ("slot " + i):"";});
        
       g.append('g').call(xaxis)
        .attr('id', 'xaxis')
        .selectAll('text')
        .attr('transform',`translate(${this.innerWidth/64},${0})`)
        .attr('font-size', '14px');
     },

     drawSlots(){
       console.log("drawSlots")
      let that = this;
      const xscale = d3.scaleLinear()
                       .domain([0,this.c])
                       .range([0, this.innerWidth]);
      var [a,b] = d3.extent(that.slots, function(d){return d.at_number;})
      console.log([a,b]);
      var distribute = d3.scaleLinear().domain([a,b]).range([10, this.innerWidth/32]);

      d3.select('#slotview').append('g').attr('id','headers')
        .selectAll('rect').data(this.slots).enter()
        .append('rect')
        .attr('transform',function(d,i){
        return `translate(${xscale(i)+that.innerWidth/64-distribute(d.at_number)/2}, ${-distribute(d.at_number)/2})`;
        })
        .attr('width', function(d){return distribute(d.at_number);} )//长宽待定
        .attr('height', function(d){return distribute(d.at_number);})
        .attr('fill', 'grey')
        .attr('opacity', 0.9)
     },

     drawBlocks(){
       console.log("drawBlocks");
      var ex_block = this.innerWidth/50;  
      const xscale = d3.scaleLinear()
                  .domain([0,this.c])
                  .range([0, this.innerWidth]);
      let that = this;
      for(let j = 0; j < that.slots.length; j++){
        for(let k=1; k <= that.slots[j]['block_number']; k++){
          d3.select('#slotview').append('g').attr('id','ex_blocks')
              .attr('transform',function(){
              return `translate(${xscale(j)+that.innerWidth/64-ex_block/2},${k*(ex_block+10)+30})`;
              })
              .append('rect')
          .attr('width', ex_block)
          .attr('height', ex_block)
          .attr('fill',"lightblue")
          .attr('opacity',0.9)
        }
}
     }
  },

  created(){
    this.getSlot();
    this.drawSlots();
    this.drawBlocks();
  },
  watch:{
    message(){
      d3.select('#headers').remove();
        console.log("draw")
        this.getSlot();
        this.drawSlots();
        this.drawBlocks();
    }

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
