<template>
  <div>
    <svg id = "Slot" style = 'width:1200px; height:860px'></svg>
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
        top:160,
        right:40,
        bottom:500,
        left:5
      },
      c:32,
      extent_m:0,
      extent_M:0
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
    },
    epochs(){
      let e = [this.msg - 1, this.msg + 1]
      return e
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
      let that = this;
      const g = d3.select('#Slot').append('g').attr('id', 'slotview')
                   .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
      const xscale = d3.scaleLinear()
                       .domain([-1,this.c])
                       .range([0, this.innerWidth]);

      const xaxis = d3.axisBottom(xscale)
                      .ticks(34)
                      .tickSize(-10)
                      .tickPadding(20)
                      .tickFormat(function(d,i){console.log(i==0?0:1)
                      return (i < 33 && i > 0) ? (i-1): "";});
        
       g.append('g').call(xaxis)
        .attr('id', 'xaxis')
        .selectAll('text')
        .attr('transform',`translate(${this.innerWidth/68},${0})`)
        .attr('font-size', '11px');
      
      g.append('circle')
        .attr('cx',xscale(-1)+that.innerWidth/68)
        .attr('cy',0)
        .attr('r',8)
        .attr('fill','#B768FF')

      // g.append('circle')
      //   .attr('cx',xscale(32)+that.innerWidth/68)
      //   .attr('cy',0)
      //   .attr('r',8)
      //   .attr('fill','#6BFF88')

     },

     Color(num){
      let that = this;
      var [m_temp,n] = d3.extent(d3.filter(that.slots, x=>x.block_header !=0), function(d){return d.block_header})
      var prev = m_temp == 0? m_temp : n;
      var m = 0;
      for(let j = 0; j < that.slots.length; j++){
          m = d3.min(that.slots[j]['ex_blocks'])
          if(m < prev){
            prev = m;
          }
         }

      that.extent_m = prev;
      that.extent_M = n
      const color =d3.scaleDivergingSymlog([prev,0.8*prev+0.2*n,n], function(t){return d3.interpolateBlues(t);})
      return color(num)
    },

     drawBlockheader(){
      let that = this;
      console.log(that.Color(20))
      const xscale = d3.scaleLinear()
                       .domain([-1,this.c])
                       .range([0, this.innerWidth]);
      var [a,b] = d3.extent(that.slots, function(d){return d.at_number;})
      console.log([a,b]);
      var distribute = d3.scaleLinear().domain([a,b]).range([10, this.innerWidth/34]);

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
        .attr('fill', function(d){return that.Color(d.block_header);})
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
          // var [u,v] = d3.extent(that.slots[j]['ex_blocks'])
          // var dis = d3.scaleLinear().domain([u,v]).range([0.1, 1]);
          d3.select('#slotview').append('g').attr('id','ex_block'+j).selectAll('rect')
          .data(that.slots[j]['ex_blocks']).enter()
              .append('rect')
          .attr('transform',function(d,i){
              return `translate(${xscale(j)+that.innerWidth/68-ex_block/2},${-i*(ex_block+10)-that.innerWidth/34-20})`;
              })
          .attr('width', ex_block)
          .attr('height', ex_block)
          .attr('fill',function(d){return that.Color(d);})
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
      console.log(that.links)
      var [e,f] = d3.extent(that.links, function(d){return d.value;})
      console.log([e,f]);
      var thickness = d3.scaleLinear().domain([e,f]).range([1, 10]);

      d3.select('#slotview').append('g').attr('id','inclusion_delay').attr('fill','none')
          .selectAll("path")
          .data(that.links).enter()
          .append("path").attr("d",that.arc).attr("stroke-width",function(d){return thickness(d.value);})
          .attr("stroke", function(d){return d.correct ? "#88EB52":"#DB366A";})

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
      },

     Legend(){
       let that = this;
       var lg = d3.select('#Slot').append('g').attr('id','legend')
                  .attr('transform', `translate(${10},${0})`)
       lg.append('rect')
         .attr('width',that.innerWidth/50)
         .attr('height', that.innerWidth/100)
         .attr('transform', `translate(${10},${0})`)
         .attr('fill','#2665A5')

       lg.append('rect')
         .attr('width',that.innerWidth/50)
         .attr('height', that.innerWidth/100)
         .attr('transform', `translate(${10},${that.innerWidth/100})`)
         .attr('fill','lightgrey')

       lg.append('text')
         .text('—Effective balance of GHOST selection')
         .attr('transform', `translate(${16+that.innerWidth/50},${8})`)
         .attr('font-size','10px')

       lg.append('text')
         .text('—Effective balance of Casper voting')
         .attr('transform', `translate(${16+that.innerWidth/50},${9+that.innerWidth/100})`)
         .attr('font-size','10px')
       
       lg.append('text')
         .text('Block size: number of attestations inside')
         .attr('transform', `translate(${16+that.innerWidth/50},${20+that.innerWidth/100})`)
         .attr('font-size','10px')

       lg.append('rect')
         .attr('width',that.innerWidth/50)
         .attr('height', that.innerWidth/50)
         .attr('transform', `translate(${250},${0})`)
         .attr('fill','lightblue')

       lg.append('text')
         .text('—Competing block in the slot')
         .attr('transform', `translate(${260+that.innerWidth/50},${3+that.innerWidth/100})`)
         .attr('font-size','10px')

       lg.append('circle')
         .attr('r', 8)
         .attr('fill', '#B768FF')
         .attr('transform',`translate(${460+that.innerWidth/50},${11})`)

       lg.append('text')
         .text('Previous Epoch')
         .attr('transform', `translate(${470+that.innerWidth/50},${3+that.innerWidth/100})`)
         .attr('font-size','10px')

      //  lg.append('circle')
      //    .attr('r', 8)
      //    .attr('fill', '#6BFF88')
      //    .attr('transform',`translate(${610+that.innerWidth/50},${11})`)

      //  lg.append('text')
      //    .text('Next Epoch')
      //    .attr('transform', `translate(${620+that.innerWidth/50},${3+that.innerWidth/100})`)
      //    .attr('font-size','10px')

       lg.append('circle')
         .attr('r', 10)
         .attr('fill', 'white')
         .attr('stroke','#DB366A')
         .attr('transform',`translate(${620+that.innerWidth/50},${6})`)

       lg.append('rect')
         .attr('width',20)
         .attr('height', 10)
         .attr('transform', `translate(${610+that.innerWidth/50},${-4})`)
         .attr('fill','white')
       
       lg.append('text')
         .text('Target wrong attestations')
         .attr('transform', `translate(${640+that.innerWidth/50},${3+that.innerWidth/100})`)
         .attr('font-size','10px')

       lg.append('circle')
         .attr('r', 10)
         .attr('fill', 'white')
         .attr('stroke','#88EB52')
         .attr('transform',`translate(${810+that.innerWidth/50},${6})`)

       lg.append('rect')
         .attr('width',20)
         .attr('height', 10)
         .attr('transform', `translate(${800+that.innerWidth/50},${-4})`)
         .attr('fill','white')
       
       lg.append('text')
         .text('Target correct attestations')
         .attr('transform', `translate(${830+that.innerWidth/50},${3+that.innerWidth/100})`)
         .attr('font-size','10px')

       lg.append("g").attr("id","legend_blocks")
         .call(that.colorbox,[10,100],d3.scaleDivergingSymlog([that.extent_m,0.7*that.extent_m+0.3*that.extent_M,that.extent_M], function(t){return d3.interpolateBlues(t);}))
         .attr("transform",`translate(${1170},${30})`)

        d3.select("#legend_blocks")
          .append("g")
          .call(d3.axisLeft(d3.scaleLinear().domain([that.extent_M/1000000000000,that.extent_m/10000000000]).range([100,0])).ticks(5))
          .attr("transform","translate(0,0)")
        d3.select("#legend_blocks") 
          .append("text")
          .text("Obtained Effective")
          .attr("transform","translate(-70,-20)")
          .attr("font-size","10px")
        d3.select("#legend_blocks") 
          .append("text")
          .text("Balance/*10e12")
          .attr("transform","translate(-60,-10)")
          .attr("font-size","10px")
     
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
        this.Legend();
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
