<template>
  <div>
    <div class="panel-header">SlotView</div>
    <div class="panel-header-end"></div>
    <svg id = "Slot" style = 'width:1250px; height:420px'></svg>
    <div class="tooltip_delay"></div>
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
      delays:[],
      width: 950,
      height: 850,
      margin:{
        top:72,
        right:85,
        bottom:0,
        left:25
      },
      c:32,
      extent_m:0,
      extent_M:0,
      h:0,
      q:0,
      timer:""
    };
  },
  mounted(){
      this.timer = setInterval(this.getSlot,10000);
  },
  computed:{
    slot(){
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
      const path = 'http://10.192.9.11:5000/slot/' + eval(this.msg);
      axios
        .get(path)
        .then(res => {
          this.slots=res.data[0];
          this.links = res.data[1];
          this.delays = res.data[2];
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
                      .tickSize(-5)
                      .tickPadding(10)
                      .tickFormat(function(d,i){console.log(i==0?0:1)
                      return (i < 33 && i > 0) ? (i-1): "";});
        
       g.append('g').call(xaxis)
        .attr('id', 'xaxis')
        .selectAll('text')
        .attr('transform',`translate(${this.innerWidth/68},${0})`)
        .attr('font-size', '10px');
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

    ColorCasper(num){
      let that = this;
      var [h,q] = d3.extent(d3.filter(that.slots, x=>x.block_header !=0), function(d){return d.casper_balance;})
      const color =d3.scaleDivergingSymlog([h/1.2,0.2*h+0.8*q,q], function(t){return t;})
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
      that.h = h;
      that.q = q;

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
        .attr('fill', "#6B3593")
        .attr('opacity', function(d){return that.ColorCasper(d.casper_balance);})
     },
     
    drawDelay(){
      console.log("drawBlocks");
      var ex_block = this.innerWidth/40;  
      const xscale = d3.scaleLinear()
                  .domain([-1,this.c])
                  .range([0, this.innerWidth]);
      let that = this;
      var [a,b] = d3.extent(that.delays, function(d){return d.count;})
      console.log([a,b]);
      var distribute = d3.scaleLinear().domain([a,b]).range([5, this.innerWidth/80]);

      d3.select('#slotview').append('g').attr('id','delays')
        .selectAll('circle')
        .data(that.delays).enter()
        .append('circle')
        .attr('cx',xscale(-1)+that.innerWidth/68)
        .attr('cy',function(d,i){return -i*(ex_block+2);})
        .attr('r',function(d){
          return distribute(d.count);
        })
        .attr('fill',"#F48FB1")
        .on("mouseover",function(){
        let d =d3.select(this).data();
        var str ="Delay length:" + d[0]['gap'] + "<br>Number of Attestation:"+d[0]['count'];
      
        console.log(d3.select(this));
        d3.selectAll('.tooltip_delay')
          .html(str)
               .style("left", (xscale(-1))+"px")
               .style("top", (300-d[0]['gap']*(ex_block+8))+"px")
               .style("opacity",1.0);
    })
      .on("mouseleave",function(){
            d3.selectAll('.tooltip_delay')
              .style("opacity",0.0);
          })
     },

     drawExBlocks(){
      console.log("drawBlocks");
      var ex_block = this.innerWidth/50;  
      const xscale = d3.scaleLinear()
                  .domain([-1,this.c])
                  .range([0, this.innerWidth]);
      let that = this;

      for(let j = 0; j < that.slots.length; j++){
          d3.select('#slotview').append('g').attr('id','ex_block'+j).selectAll('rect')
          .data(that.slots[j]['ex_blocks']).enter()
              .append('rect')
          .attr('transform',function(d,i){
              return `translate(${xscale(j)+that.innerWidth/68-ex_block/2},${-i*(ex_block+2)-that.innerWidth/34-4})`;
              })
          .attr('width', ex_block)
          .attr('height', ex_block)
          .attr('fill',function(d){return that.Color(d);})
          .attr('stroke',"#F8BBD0")
          .attr('opacity',1)
          }


     },
     arc(lines){
        const xscale = d3.scaleLinear()
                       .domain([-1,this.c])
                       .range([0, this.innerWidth]);

        const x1 = xscale(lines.source)+this.innerWidth/68;
        const x2 = xscale(lines.target)+this.innerWidth/68;
        const r = Math.abs(x2 - x1) / 2 ;
      return `m${x1},${this.innerWidth/30+3}A${r},${r/1.17} 0,0,0 ${x2},${this.innerWidth/30+3}`;
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
          .attr("stroke", function(d){return d.correct ? "#55A674":"#C64D6B";})

     },
     colorbox(sel, size, colors){
    var [x0,x1] = d3.extent( colors.domain());
    var bars = d3.range( x0, x1, (x1-x0)/size[0]);
    var sc = d3.scaleLinear()
        .domain([x0,x1]).range([0, size[0]]);
    sel.selectAll("line").data(bars).enter().append("line")
      .attr("x1", sc).attr("x2",sc)
      .attr("y1", 0).attr("y2",size[1])
      .attr("stroke",colors);
    
    sel.append("rect")
        .attr("width",size[0]).attr("height",size[1])
        .attr("fill","none").attr("stroke","black")
      },

     Legend(){
       let that = this;
       var lg = d3.select('#Slot').append('g').attr('id','legend')
                  .attr('transform', `translate(${600},${30})`)
       lg.append('rect')
         .attr('width',that.innerWidth/35)
         .attr('height', that.innerWidth/70)
         .attr('transform', `translate(${355},${35})`)
         .attr('fill','#2665A5')

       lg.append('rect')
         .attr('width',that.innerWidth/35)
         .attr('height', that.innerWidth/70)
         .attr('transform', `translate(${355},${35+that.innerWidth/70})`)
         .attr('fill','#AF7AC5')

       lg.append('text')
         .text(' — GHOST balance')
         .attr('transform', `translate(${377},${41})`)
         .attr('font-size','9px')

       lg.append('text')
         .text(' — Casper balance')
         .attr('transform', `translate(${377},${44+that.innerWidth/50})`)
         .attr('font-size','9px')

       lg.append('text')
         .text('Block size: number of attestations inside')
         .attr('transform', `translate(${325},${60+that.innerWidth/70})`)
         .attr('font-size','9px')

       lg.append('rect')
         .attr('width',that.innerWidth/50)
         .attr('height', that.innerWidth/50)
         .attr('transform', `translate(${360},${18})`)
         .attr('fill','lightblue')

       lg.append('text')
         .text(' — Competing blocks')
         .attr('transform', `translate(${377},${18+that.innerWidth/100})`)
         .attr('font-size','9px')

       lg.append('circle')
         .attr('r', 5)
         .attr('fill', '#F48FB1')
         .attr('transform',`translate(${365},${140+that.innerWidth/50})`)

       lg.append('text')
         .text('Finalization Delay')
         .attr('transform', `translate(${377},${144+that.innerWidth/50})`)
         .attr('font-size','9px')

       lg.append('circle')
         .attr('r', 10)
         .attr('fill', 'white')
         .attr('stroke',"#C64D6B")
         .attr('transform',`translate(${360},${180+that.innerWidth/50})`)

       lg.append('rect')
         .attr('width',22)
         .attr('height', 12)
         .attr('transform', `translate(${349},${168+that.innerWidth/50})`)
         .attr('fill','white')

       lg.append('text')
         .text('Target wrong attestations')
         .attr('transform', `translate(${375},${190+that.innerWidth/50})`)
         .attr('font-size','9px')

       lg.append('circle')
         .attr('r', 10)
         .attr('fill', 'white')
         .attr('stroke',"#55A674")
         .attr('transform',`translate(${360},${210+that.innerWidth/50})`)

       lg.append('rect')
         .attr('width',22)
         .attr('height', 12)
         .attr('transform', `translate(${349},${198+that.innerWidth/50})`)
         .attr('fill','white')

       lg.append('text')
         .text('Target correct attestations')
         .attr('transform', `translate(${375},${220+that.innerWidth/50})`)
         .attr('font-size','9px')

       lg.append("g").attr("id","legend_blocks")
         .call(that.colorbox,[150,8],d3.scaleDivergingSymlog([that.extent_m,0.7*that.extent_m+0.3*that.extent_M,that.extent_M], function(t){return d3.interpolateBlues(t);}))
         .attr("transform",`translate(${335},${-10})`)

        d3.select("#legend_blocks")
          .append("g")
          .call(d3.axisBottom(d3.scaleLinear().domain([that.extent_M/1000000000000,that.extent_m/10000000000]).range([150,0])).ticks(5).tickSize(3))
          .attr("transform","translate(0,8)")


        d3.select("#legend_blocks")
          .append("text")
          .text("Effective Balance(gwei)")
          .attr("transform","translate(60,-5)")
          .attr("font-size","9px")

       lg.append("g").attr("id","legend_casper")
         .call(that.colorbox,[150,8],d3.scaleDiverging([that.h,0.5*that.h+0.5*that.q,that.q], function(t){return d3.interpolatePurples(t);}))
         .attr("transform",`translate(${335},${100})`)

        d3.select("#legend_casper")
          .append("g")
          .call(d3.axisTop(d3.scaleLinear().domain([that.extent_M/1000000000000,that.extent_m/10000000000]).range([150,0])).ticks(5).tickSize(3))
          .attr("transform","translate(0,0)")


        d3.select("#legend_casper")
          .append("text")
          .text("Effective Balance(gwei)")
          .attr("transform","translate(60,20)")
          .attr("font-size","9px")
     
     }
  },

  created(){
  },
  beforeUnmount() {
      clearInterval(this.timer);
    },
  watch:{
    slot(){
      d3.select('#Slot').selectAll('g').remove()
        this.xScale();
        this.drawArc();
        this.drawBlockheader();
        this.drawCasper();
        this.drawExBlocks();
        this.drawDelay();
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
.tooltip_delay{
    position: absolute;
    padding-left:5px;
    padding-right:5px;
    width:auto;
    height:auto;
    border:1px solid #2ea44f;
    border-radius:5px;
    background-color: white;
    font-size: 8px;
    text-align: center;
    opacity:0;
    z-index:999;
		}

.panel-header {
  position: absolute;
  left:0px;
  top:335px;
  padding: -10px 20px;
  width: 45px;
  height: 18px;
  line-height: 18px;
  font-size: 8px;
  text-align: left;
  background: #415c68;
  color: #fcfcfc;
  display: flex;
  font-weight: bold;
  border-radius: 1px;
  box-shadow: 0 1px 2px rgba(26 26 26 0.2);
  z-index:99;

}

.panel-header-end {
  position: absolute;
  top: 335px;
  left: 61px;
  border-top: 18px solid #455a64;
  border-right: 18px solid #ffffff;
  border-bottom: 0px solid #ffffff;
  z-index:98;
}

</style>
