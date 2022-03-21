<template>
  <div id = "Tip">
    <svg id = "Epoch"  class="epoch" style = 'width:360px; height:300px'>
    </svg>
    <div class="tooltip"></div>
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
      width: 360,
      height: 300,
      margin:{
        top:30,
        right:80,
        bottom:10,
        left:30
      },
      r:15,
      c:15,
      flag:0,
      information:{}
    };
  },
  mounted(){

  },
  computed:{
    showTip(){
      return this.flag;
    },
    index(){
      console.log(this.day);
      return this.day;
    },
    epoch(){
      console.log(this.epochs)
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
    d3.select('#Epoch').selectAll('#legend').remove()
    const c = this.c;
    var [a,b] = d3.extent(this.epochs, function(d){return d['active_balance'] - d['head_correct_balance'];})

    const xscale = d3.scaleLinear()
                       .domain([0,this.c])
                       .range([0, this.innerWidth]);
    const yscale = d3.scaleLinear()
          .domain([0,this.r])
          .range([0, this.innerHeight]);

    

    d3.select('#epochview')
      .selectAll('rect').data(this.epochs).enter()
      .append('rect')
      .attr('fill', function(d){return d3.interpolateReds((d['active_balance'] - d['head_correct_balance']-a)/(b-a) )})
      .attr('width', this.innerWidth/15-5)
      .attr('height', this.innerHeight/15-5)
      .attr('stroke',function(d){
        if ((d['active_balance'] - d['head_correct_balance']) > d['active_balance'] * 0.67){
            console.log(d['head_correct_balance'])
            return '#7E00C4'
        }else{
          if((d['active_balance'] - d['head_correct_balance']) > d['active_balance'] * 0.33){
            return '#7510EB'
          }else{
           return ''
          }
        }
      })
      .attr('stroke-width',function(d){
        if ((d['active_balance'] - d['head_correct_balance']) > d['active_balance'] * 0.67){
            console.log(d['head_correct_balance'])
            return '2.5px'
        }else{
          if((d['active_balance'] - d['head_correct_balance']) > d['active_balance'] * 0.33){
            return '2px'
          }else{
              return ''
          }
        }
      })
      .attr("transform", function(d, i) {
        return `translate(${xscale(Math.floor((i)%c))+2.5},${yscale(Math.floor((i)/c))+2.5})`;
      })
      .on("click", function(){                   
        var temp = d3.select(this).data();
        that.$emit('details',temp[0].epoch);
      })
      .on("mouseover",function(){
        let d =d3.select(this).data();

        var str =" head_error_balance/active_balance: " + (100*(1 - d[0]['head_correct_balance']/d[0]['active_balance'])).toFixed(2) + "% ";
      
        
        d3.selectAll('.tooltip')
          .html(str)
               .style("left", (820+xscale(Math.ceil((d[0].epoch%225)%c)))+"px")
               .style("top", (25+yscale(Math.floor((d[0].epoch%225)/c)))+"px")
               .style("opacity",1.0);
    })
      .on("mouseleave",function(){
            d3.select('#Tip')
              .selectAll('.tooltip')
              .style("opacity",0.0);
          })
    
    var med = d3.median([a,b]);
    d3.select("#Epoch")
      .append("g").attr("id","legend")
      .call(that.colorbox,[10,150],d3.scaleDiverging([a, med, b], function (t){return d3.interpolateReds(t);}))
      .attr("transform",`translate(${10+that.width - that.margin.right},${25})`)

    d3.select("#legend")
       .append("g")
       .call(d3.axisRight(d3.scaleLinear().domain([b/1000000000000,a/1000000000000]).range([150,0])).ticks(5))
       .attr("transform","translate(10,0)")
    d3.select("#legend") 
      .append("text")
      .text("/x10e12")
      .attr("transform","translate(20,0)")
      .attr("font-size","10px")
  },


  Casper(){
    let that = this;
    d3.select('#epochview').selectAll('rect').remove()
    d3.select('#Epoch').selectAll('#legend').remove()
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
                  .attr('stroke',function(d){
                    if ((d['active_balance'] - d['head_correct_balance']) > d['active_balance'] * 0.5){
                        console.log(d['head_correct_balance'])
                        return '#7E00C4'
                    }else{
                      if((d['active_balance'] - d['head_correct_balance']) > d['active_balance'] * 0.25){
                        return '#7510EB'
                      }else{
                          return ''
                      }
                    }
                  })
                  .attr('stroke-width',function(d){
                    if ((d['active_balance'] - d['head_correct_balance']) > d['active_balance'] * 0.5){
                        console.log(d['head_correct_balance'])
                        return '2.5px'
                    }else{
                      if((d['active_balance'] - d['head_correct_balance']) > d['active_balance'] * 0.25){
                        return '2px'
                      }else{
                          return ''
                      }
                    }
                  })
                  .attr("transform", function(d, i) {
            return `translate(${xscale(Math.floor((i)%c))+2.5},${yscale(Math.floor((i)/c))+2.5})`;
                  })
                  .on("click", function(){                   
                    var temp = d3.select(this).data();
                    that.$emit('details',temp[0].epoch);
                  })

    var med = d3.median([a,b]);
    d3.select("#Epoch")
      .append("g").attr("id","legend")
      .call(that.colorbox,[10,150],d3.scaleDiverging([a, med, b], function (t){return d3.interpolateReds(t);}))
      .attr("transform",`translate(${10+that.width - that.margin.right},${20})`)

    d3.select("#legend")
       .append("g")
       .call(d3.axisRight(d3.scaleLinear().domain([b/1000000000000,a/1000000000000]).range([150,0])).ticks(5))
       .attr("transform","translate(10,0)")
    d3.select("#legend") 
      .append("text")
      .text("/x10e12")
      .attr("transform","translate(20,0)")
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
    top:0px;
    left:1085px;
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
    top:0px;
    left:1130px;
    text-align: center;
    text-decoration: none;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
    vertical-align: middle;
    white-space: nowrap;
}

.tooltip{
    position: absolute;
    padding-left:5px;
    padding-right:5px;
    width:auto;
    height:auto;
    border:1px solid #2ea44f;
    border-radius:5px;
    background-color: white;
    font-size: 14px;
    text-align: center;
		}

</style>
