<template>
  <div id = "Tip">
    <div class="panel-header">EpochView</div>
    <div class="panel-header-end"></div>
    <svg id = "Epoch"  class="epoch" style = 'width:435px; height:330px'>
    </svg>
    <div class="tooltip"></div>
    <div class="tooltip2"></div>
    <button id = 'ghost' @click = 'GHOST(), showNote(),drawDelay()'>GHOST Vote</button>
    <button id = 'casper' @click = 'Casper(), showNote(),drawDelay()'>Casper Vote</button>
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
      height: 285,
      margin:{
        top:40,
        right:50,
        bottom:10,
        left:89
      },
      r:15,
      c:15,
      flag:"",
      timer:"",
      timer2:"",
      timer3:"",
      current_justified_epoch: 0,
      current_finalized_epoch: 0,
      total_reorgs: 0,
      record_reorgs:0,
      last_reorgs:'',
      current_slot: 0
    };
  },
  mounted(){
    this.Scale();
    this.timer = setInterval(this.getEpoch, 80000);
    this.timer2 = setInterval(this.getTotalReorgs,40000);
    this.timer3 = setInterval(this.getCurrentSlot,40000);
  },
  computed:{
    reorg(){
      return this.total_reorgs;
    },
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
      const path = 'http://10.192.9.11:5000/EpochView/' + eval(this.day);
      axios
        .get(path)
        .then(res => {
          this.epochs = res.data;
        })
        .catch(error => {
          console.error(error);
        });
      console.log("getEpoch")
     },
    getCurrentJustifiedEpoch(){
      const path_justified_epoch = 'http://localhost:9093/api/v1/query?query=beacon_current_justified_epoch';
      axios
        .get(path_justified_epoch)
        .then(results => {
          this.current_justified_epoch = results.data.data.result[0].value[1];
        })
        .catch(error => {
          console.error(error);
        });
    },
    getCurrentFinalizedEpoch(){
      const path_finalized_epoch = 'http://localhost:9093/api/v1/query?query=beacon_finalized_epoch';
      axios
        .get(path_finalized_epoch)
        .then(results => {
          this.current_finalized_epoch = results.data.data.result[0].value[1];
        })
        .catch(error => {
          console.error(error);
        });
    },
    getTotalReorgs(){
      const path_total_reorgs = 'http://10.192.9.11:9093/api/v1/query?query=beacon_reorgs_total';
      axios
        .get(path_total_reorgs)
        .then(results => {
          this.total_reorgs = results.data.data.result[0].value[1];
        })
        .catch(error => {
          console.error(error);
        });
    },
    getCurrentSlot(){
      const path_total_reorgs = 'http://10.192.9.11:9093/api/v1/query?query=beacon_slot';
      axios
        .get(path_total_reorgs)
        .then(results => {
          this.current_slot = results.data.data.result[0].value[1];
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
                      .tickPadding(5);
      const xaxis = d3.axisBottom(xscale)
                      .ticks(this.c)
                      .tickSize(-5)
                      .tickPadding(-15);
        g.append('g').call(yaxis)
         .attr('id' ,'yaxis');
        g.append('g').call(xaxis)
         .attr('id', 'xaxis');
    },

    drawDelay(){
      let that = this;
      d3.select('#epochview').selectAll('#delay').remove()
      const xscale = d3.scaleLinear()
                       .domain([0,this.c])
                       .range([0, this.innerWidth]);
      const yscale = d3.scaleLinear()
                       .domain([0,this.r])
                       .range([0, this.innerHeight]);

      var [h,q] = d3.extent(d3.filter(that.epochs,x=>x['delay']>1),function(d){return d['delay']})
      const z = d3.scaleLinear()
                  .domain([h,q])
                  .range([1,d3.min([that.innerWidth,that.innerHeight])/15-10]);

      d3.select('#epochview').append('g').attr('id','delay')
        .selectAll("circle")
        .data(that.epochs)
        .enter()
        .append("circle")
        .attr("cx", function (d,i) {return xscale(Math.ceil((i)%that.c + 1));} )
        .attr("cy", function (d,i) {return yscale(Math.floor((i)/that.c) + 1)-2;})
        .attr("r", function (d) { return d['delay']==1?0:z(d['delay']); } )
        .style("fill", "#014040")
        .style("opacity", 0.6 );
    },
  
  showNote(){
    let that = this;
    d3.select('#epochview')
      .selectAll('rect')
      .on("click", function(){               
        var temp = d3.select(this).data();
        that.$emit('details',temp[0].epoch);
            d3.selectAll('.tooltip2')
              .html("Current Epoch: " + temp[0].epoch + "<br>Total Reorgs in Unfinalized Epochs: " + that.total_reorgs + "<br>Last Reorg: Num:" + that.last_reorgs + " slot:" + that.current_slot)
              .style("opacity",1.0)
      })
  },

  GHOST(){
    let that = this;
    that.flag="GHOST";
    d3.select('#epochview').selectAll('rect').remove()
    d3.select('#Epoch').selectAll('#legend').remove()
    const c = this.c;
    var [a,b] = d3.extent(this.epochs, function(d){return d['active_balance_g'] - d['head_correct_balance'];})

    const xscale = d3.scaleLinear()
                       .domain([0,this.c])
                       .range([0, this.innerWidth]);
    const yscale = d3.scaleLinear()
          .domain([0,this.r])
          .range([0, this.innerHeight]);

    d3.select('#epochview')
      .selectAll('rect').data(this.epochs).enter()
      .append('rect')
      .attr('fill', function(d){return d3.interpolateBlues((d['active_balance_g'] - d['head_correct_balance']-a)/(b-a) )})
      .attr('width', this.innerWidth/15-5)
      .attr('height', this.innerHeight/15-5)
      .attr('stroke',function(d){
        if ((d['active_balance_g'] - d['head_correct_balance']) > d['active_balance_g'] * 0.67){
            console.log(d['head_correct_balance'])
            return '#E53935 '
        }else{
          if((d['active_balance_g'] - d['head_correct_balance']) > d['active_balance_g'] * 0.33){
            return '#FBC02D'
          }else{
           return ''
          }
        }
      })
      .attr('stroke-width',function(d){
        if ((d['active_balance_g'] - d['head_correct_balance']) > d['active_balance_g'] * 0.67){
            console.log(d['head_correct_balance'])
            return '1.5px'
        }else{
          if((d['active_balance_g'] - d['head_correct_balance']) > d['active_balance_g'] * 0.33){
            return '1px'
          }else{
              return ''
          }
        }
      })
      .attr("transform", function(d, i) {
        return `translate(${xscale(Math.ceil((i)%c))+that.innerWidth/30+2.5},${yscale(Math.floor((i)/c))+that.innerHeight/30+1})`;
      })
      .on("mouseover",function(){
        let d =d3.select(this).data();
        var str =" Head_error_balance/active_balance: " + (100*(1 - d[0]['head_correct_balance']/d[0]['active_balance_g'])).toFixed(2) + "% " +"<br>Epoch:"+d[0]['epoch'];
        var t = yscale(Math.floor((d[0].epoch%225)/c))
        if (d[0]['delay'] > 1){
          str += '<br>Justification Delay: ' + d[0]['delay']
          t -= 10;
        }      
        
        d3.selectAll('.tooltip')
          .html(str)
          .style("left", (810+xscale(Math.ceil((d[0].epoch%225)%c)))+"px")
          .style("top", (t)+"px")
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
      .call(that.colorbox,[10,150],d3.scaleDiverging([a, med, b], function (t){return d3.interpolateBlues(t);}))
      .attr("transform",`translate(${20+that.width - that.margin.right},${25})`)

    d3.select("#legend")
       .append("g")
       .call(d3.axisRight(d3.scaleLinear().domain([b/1000000000000,a/1000000000000]).range([150,0])).ticks(5))
       .attr("transform","translate(10,0)")
    d3.select("#legend") 
      .append("text")
      .text("Effective Balance(gwei)")
      .attr("transform","translate(-6,-8)")
      .attr("font-size","10px")

    d3.select("#legend")
      .append("g")
      .append("circle")
      .attr('r',that.innerWidth/50)
      .attr('transform', `translate(${5},${180})`)
      .attr('fill','#014040')
      .attr("opacity", 0.6 );
    d3.select("#legend") 
      .append("text")
      .text("Inclusion Delay")
      .attr("transform",`translate(${that.innerWidth/50+10},${183})`)
      .attr("font-size","10px")

  },

  Casper(){
    let that = this;
    that.flag="Casper";
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
                  .attr('fill', function(d){return d3.interpolatePurples((d['active_balance'] - d['target_correct_balance']-a)/(b-a) )})
                  .attr('width', this.innerWidth/15-5)
                  .attr('height', this.innerHeight/15-5)
                  .attr('stroke',function(d){
                    if ((d['active_balance'] - d['target_correct_balance']) > d['active_balance'] * 0.5){
                        console.log(d['target_correct_balance'])
                        return '#E53935'
                    }else{
                      if((d['active_balance'] - d['target_correct_balance']) > d['active_balance'] * 0.25){
                        return '#FBC02D'
                      }else{
                          return ''
                      }
                    }
                  })
                  .attr('stroke-width',function(d){
                    if ((d['active_balance'] - d['target_correct_balance']) > d['active_balance'] * 0.5){
                        console.log(d['target_correct_balance'])
                        return '1.5px'
                    }else{
                      if((d['active_balance'] - d['target_correct_balance']) > d['active_balance'] * 0.25){
                        return '1px'
                      }else{
                          return ''
                      }
                    }
                  })
                  .attr("transform", function(d, i) {
            return `translate(${xscale(Math.ceil((i)%c))+that.innerWidth/30+2.5},${yscale(Math.floor((i)/c))+that.innerHeight/30+1})`;
                  })
                  .on("mouseover",function(){
                    let d =d3.select(this).data();

                    var str =" Target_error_balance/active_balance: " + (100*(1 - d[0]['target_correct_balance']/d[0]['active_balance'])).toFixed(2) + "% "+"<br>Epoch:"+d[0]['epoch'];
                    
                    var t = -10+yscale(Math.floor((d[0].epoch%225)/c))
                    if (d[0]['delay'] > 1){
                      str += '<br>Justification Delay: ' + d[0]['delay']
                      t -= 10;
                    }      

                    d3.selectAll('.tooltip')
                      .html(str)
                      .style("left", (810+xscale(Math.ceil((d[0].epoch%225)%c)))+"px")
                      .style("top", (t)+"px")
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
      .call(that.colorbox,[10,150],d3.scaleDiverging([a, med, b], function (t){return d3.interpolatePurples(t);}))
      .attr("transform",`translate(${20+that.width - that.margin.right},${25})`)

    d3.select("#legend")
       .append("g")
       .call(d3.axisRight(d3.scaleLinear().domain([b/1000000000000,a/1000000000000]).range([150,0])).ticks(5))
       .attr("transform","translate(10,0)")
    d3.select("#legend") 
      .append("text")
      .text("Effective Balance(gwei)")
      .attr("transform","translate(-6,-8)")
      .attr("font-size","10px")

    d3.select("#legend")
      .append("g")
      .append("circle")
      .attr('r',that.innerWidth/50)
      .attr('transform', `translate(${5},${180})`)
      .attr('fill','#014040')
      .attr("opacity", 0.6 );
    d3.select("#legend") 
      .append("text")
      .text("Inclusion Delay")
      .attr("transform",`translate(${that.innerWidth/50+10},${183})`)
      .attr("font-size","10px")
  }, // Casper

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
    reorg_cal(){
      this.last_reorgs = this.record_reorgs;
      this.record_reorgs = this.total_reorgs;
    }
  },
  created(){
    this.getEpoch();
    this.getTotalReorgs();
    this.getCurrentSlot();
  },
  beforeUnmount() {
    clearInterval(this.timer);
    clearInterval(this.timer2);
    clearInterval(this.timer3);
  },
  watch:{
    epoch(){

      this.GHOST();
      this.showNote();
      this.drawDelay();

    },
    index(){
      this.getEpoch();
      //console.log("day changed")
      //console.log(this.epochs)
    },
    reorg(){
      if(this.record_reorgs == 0){
        this.showNote();
        this.reorg_cal();
      }else{
        this.reorg_cal();
        this.showNote();
      }
    }
  }
};
</script>

<style scoped>
#ghost {
    appearance: none;
    background-color: #39c561;
    border: 1px solid rgba(27, 31, 35, .15);
    border-radius: 5px;
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
    top:240px;
    left:1150px;
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
    background-color: #39c561;
    border: 1px solid rgba(27, 31, 35, .15);
    border-radius: 5px;
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
    top:265px;
    left:1150px;
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
    font-size: 8px;
    text-align: center;
    opacity:0;
    z-index:999;
		}

.tooltip2{
  position:absolute;
  left:920px;
  top:640px;
  width:auto;
  height:auto;
  border:2px solid lightcoral;
  border-radius:5px;
  padding-left:1px;
  padding-right:1px;
  padding-top:1px;
  padding:1px;
  background-color: white;
  font-size: 1px;
  text-align: center;
  opacity:0;
  z-index:99;
}
.panel-header {
  position: absolute;
  left:817px;
  top:0px;
  padding: -10px 20px;
  width: 53px;
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
  top: 0px;
  left: 886px;
  border-top: 18px solid #455a64;
  border-right: 18px solid #ffffff;
  border-bottom: 0px solid #ffffff;
  z-index:98;
}
</style>
