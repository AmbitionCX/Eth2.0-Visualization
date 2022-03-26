<template>
  <div>
    <div class="panel-header_val">ValidatorView</div>
    <div class="panel-header-end_val"></div>
    <svg id = "Validator" style = 'width:435px; height:315px'>
    </svg>
    <div class="tooltip3"></div>
  </div>
</template>

<script>
import axios from 'axios'
import * as d3 from 'd3'

export default {
  name:'Validator',
  props:["msg"],
  data(){
    return {
      val:[],
      proposer:[],
      width: 435,
      height: 321,
      margin:{
        top:5,
        right:0,
        bottom:45,
        left:0
        
      }
    
    };
  },
  mounted(){

  },
  computed:{
    message(){
      console.log(this.msg);
      return this.msg;
    },
    vali(){
      return this.val;
    },
    innerWidth(){
      return this.width - this.margin.left - this.margin.right
    },
    innerHeight(){
      return this.height - this.margin.top - this.margin.bottom
    }
  },
  methods:{
    getValidator(){
      const path = 'http://127.0.0.1:5000/validator/' + eval(this.msg);
      console.log(path);
      axios
        .get(path)
        .then(res => {
          console.log(res);
          this.val=res.data[0];
          this.proposer = res.data[1]
        })
        .catch(error => {
          console.error(error);
        });

    },

    data_processing(){
   const     slashed_slot=[6668,22373,40771,138163,138730,140312,140558,140810,140844,140894,141173,248185,343132,476903,1510278
  ,1856962,3339590,17090,17090,17090,17091,17091,17092,17090,17091,17091,17091,43917,102388,118135,138163,138163,138163,138730,
  140894,140894,138163,138730,456995,457540,231180,256809,296752,357059,421394,456865,456873,456869,456875,456930,456931,456929,
  456928,457443,457540,457537,457537,457538,457541,457542,457541,457537,457540,457537,457536,457539,457540,457536,457539,457541,
  457536,457537,457542,457541,457536,457536,457536,457541,457536,457539,457536,457539,457536,475779,457537,457538,457537,457537,
  457540,2755552,457538,457539,457541,457538,457540,2812800,2813960,457536,457536,457542,457539,457540,457537,457539,457537,457540,
  457536,457542,457536,457539,457536,457540,457541,457541,457537,457538,457542,457536,457542,457536,457541,457542,475780,475778,475777,
  475776,475780,475779,475776,475776,475780,475780,475776,475779,475776,475777,475778,475776,906880,1003553,1130720,1224987,1232591,1322720,
  1322969,1348326,1376000,1376000,1379970,1381593,1899680,1956769,1956779,1978690,2008347,2029832,2043488,2176001,2176737,2176801,2332096,
  2535250,2624390,2638205,2724283,2814144,2814432,2834208,2872459,3065149,3360800];
  const  slashed_V=[20075,18177,25645,38069,38089,38130,38129,38065,38128,38117,38114,45871,40892,63338,169440,21613,19299,21574,4259,
    4100,4390,4086,4102,4110,13869,18249,4451,7635,1644,23241,38105,38061,38061,38091,38148,38106,38058,38116,14415,71603,43843,52866,
    57976,38038,9143,8320,8275,8250,8239,16509,16491,16523,16479,17377,71676,71654,69812,71401,69884,71665,68648,69358,69895,71614,75715,
    71690,75162,69391,69817,69716,71664,69732,71671,69772,69841,71673,71708,69866,71699,71663,69809,69388,69756,17189,71593,71646,69786,
    68593,72074,203983,72499,69717,70044,71672,71709,88656,88655,71718,72084,71714,71734,71744,72081,72082,72421,72491,72493,72496,72503,
    72508,72511,72674,72807,75045,75172,75204,75212,75711,75723,71743,75699,69873,17395,18989,19001,24696,26278,26201,17164,17228,17304,
    17140,24703,23179,17291,24528,19017,17232,73292,66420,8776,3206,100190,67319,119315,26447,25895,25894,25893,12981,78678,161751,161752,
    9230,27442,45276,26945,26988,26989,26987,42708,261,1859,12697,12954,88632,88657,39710,62830,270651,66065];
    const g = d3.select("#Validator").append('g')
      .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
      
      


let that = this;

// console.log("WZH",that.val[0]);

for(let j=that.val[that.val.length-1].validator.length-1;j>0&&that.val[that.val.length-1].validator[j].vote==-2;j--)

for(let i=0;i<that.val.length;i++){
    that.val[i].validator.splice(j,1);
}

that.val.reverse();
that.proposer.reverse();


 const SUM=that.val[0].validator.length;
console.log(SUM);


 var graph = [];
 var v_line = [];
 for(let i=0; i < SUM; i++)
   v_line.push({index:that.val[0].validator[i].validator_index,node:[]});
 for(let i=0;i<that.val.length;i++){
    graph.push([]);
    for(let j=0;j<2;j++){
        graph[i].push(0);
    }
 }
//处理 被slashed的数据
var slashed=[];

for(let i=0;i<slashed_slot.length;i++){
  slashed.push({slot:slashed_slot[i],V_index:slashed_V[i]});
}
slashed.sort((x,y)=>{
  return x.V_index-y.V_index;
})
// console.log(slashed);
 //graph保留数量信息
var k = []
for(let i = 0;i < that.proposer.length; i++)
 k.push(0);
for(let j = 0; j < SUM; j++){
  for(let i = 0; i < that.val.length; i++){
   while(k[i] < that.proposer[i].length && that.val[i].validator[j].validator_index>that.proposer[i][k[i]])
        k[i]++;
    var Y=that.val[i].validator[j].vote+1;
    // if(Y==-1)
    //    console.log(i,j);
    if(Y<2){
    if(Y<0)
        Y=0;
    var X= ++graph[i][Y];
    v_line[j].node.push( {dy:X,y:Y,ispro:0,isslashed:0});
    }
    else{
     v_line[j].node.push( {dy:0,y:2,ispro:0,isslashed:0})
    }
    if(k[i]<that.proposer[i].length&&that.val[i].validator[j].validator_index==that.proposer[i][k[i]])
    v_line[j].node[i].ispro=1;
   }
}
console.log(v_line);

for(let i=0,j=0;i<slashed.length&&j<v_line.length;){
     if(slashed[i].V_index<v_line[i].index){
       i++;
     }
     else if(slashed[i].V_index>v_line[i].index){
       j++;
     }
     else{
         let epoch=Math.floor(slashed[i].slot/32);
         if(epoch>=epoch_0&&epoch<epoch_0+that.val.length){
               v_line[j].node[epoch-epoch_0].isslashed=1;
         }
     }
}
// console.log(proposer);
// console.log(graph);
// console.log(v_line);

    var data_rect=[];
   for(let i=0;i<graph.length;i++){
       for(let j=0;j<graph[i].length;j++){
        data_rect.push({i:i,j:j,size:graph[i][j]})
       }
   }

 //设置矩阵的行列
var c=that.val.length;
var epoch_0=that.val[0].epoch;
const yValue=['Unvoted validator','Wrong voted validator','Wrong voted proposer','Continuous irregular','Slashed validator'];
const xValue=[];
for(let i=0;i<c;i++){
    xValue.push(i == 0?'epoch:'+ that.val[i].epoch:that.val[i].epoch);
}


var legend = g.selectAll(".legend")
        .data(yValue)
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function (d, i) { return "translate(" + (4+i *95) + "," +(that.margin.top+that.innerHeight+20) + ")"; });
      legend.append("rect")
        .data(yValue)
        .attr("x", function(d,i){return i?-20:0})
        .attr("y", d=>d=='Continuous irregular'?5:3)
        .attr("width", 10)
        .attr("height", d=>d=='Continuous irregular'?1:4)
        .style("fill",function(d){
            switch (d){
                case 'Wrong voted validator':return 'red';
                case 'Unvoted validator':return 'grey';
                case 'Wrong voted proposer':return '#6E00F5';
                case 'Continuous irregular':return '#BFC9CA';
                case 'Slashed validator':return 'black';
            }
        })
        .attr('opacity',d=>d=='Continuous irregular'?0.7:0.8);

      legend.append("text")
        .data(yValue)
        .attr('class', 'legend_text')
        .attr("x", function(d,i){return i?-8:12})
        .attr("y", d=>d=='Continuous irregular'?-2:3)
        .attr("dy", ".5em")
        .attr("fill", 'black')
        .style("text-anchor", "start")
        .text(d => d )
         .attr('font-size','6px');
        
      g.append('text')
        .text('voting')
        .attr('transform', `translate(${300},${308})`)
        .attr('font-size','6px')

//设置坐标轴
const xscale = d3.scaleBand()
        .domain(xValue)
        .range([0, that.innerWidth]);

 const xscale2 = d3.scaleLinear()
        .domain([0,c])
        .range([0, that.innerWidth]);

const yscale2 = d3.scaleLinear() 
        .domain([0,1])
        .range([0,that.innerHeight])
// const yaxis = d3.axisLeft(yscale)
//         .ticks(r)
//         .tickSize(10)
//         .tickPadding(10)
const xaxis = d3.axisTop(xscale)
        .ticks(c)
        .tickSize(-3)
        .tickPadding(-15);
// g.append('g').call(yaxis)
//         .attr('id' ,'yaxis') 
//         .style("font-size","24px");
 
g.append('g').call(xaxis)
        .attr('id', 'xaxis')
        .attr('transform', `translate(0, ${that.innerHeight})`)
        .style("font-size","10px");
//添加矩阵

const  rect_width=that.innerWidth/(5*c);
const  sub_width=that.innerWidth/c-rect_width;
const   rect_height_I=that.innerHeight/SUM;

var x1=[];
var x2=[];
for(let j=0;j<that.val.length-1;j++){
       x1.push((j+1)*rect_width+j*sub_width+sub_width/2);
       x2.push((j+1)*rect_width+(j+1)*sub_width+sub_width/2);
  }


  function  make_line(i){
      var Y=[];
      var y1=[];
      var y2=[];
      for(let j=0;j<that.val.length;j++){
        var h;
        rect_height_I*v_line[i].node[j].dy+yscale2(v_line[i].node[j].y);
        if(v_line[i].node[j].y==2)
            h=0;
        else if(v_line[i].node[j].y==0)
            h=rect_height_I*v_line[i].node[j].dy+yscale2(v_line[i].node[j].y)+(SUM-graph[j][0]-graph[j][1])*rect_height_I;
        else 
           h=rect_height_I*v_line[i].node[j].dy+yscale2(v_line[i].node[j].y)-graph[j][1]*rect_height_I;
        Y.push(h);
        if(j<that.val.length-1)
        y1.push(h);
        if(j)
        y2.push(h);
    }
    var path=d3.path();
    for(let j=0;j<y1.length;j++){
       if((v_line[i].node[j+1].y==1||v_line[i].node[j+1].y==0)&&(v_line[i].node[j].y==0||v_line[i].node[j].y==1)){
        // var dx=(x2[j]-x1[j])/20;
        // var dy=(y2[j]-y1[j])/3;
        // let cpx1 = x1[j] + dx;
        // let cpy1 = y1[j] + dy;
        // let cpx2 = x2[j] - dx;
        // let cpy2 = y2[j] - dy;
        path.moveTo(x1[j],y1[j]);
        //path.bezierCurveTo(cpx1,cpy1,cpx2,cpy2,x2[j],y2[j]);  //曲线
        path.lineTo(x2[j],y2[j]);                                //直线
       }

    }
    g.append('path')
            .attr('class','v_line')
            .attr('d', path.toString())
            .style('stroke','#BFC9CA ')
            .style('stroke-width','0.8')//'0.5')
            .style('fill','none')
            .style('opacity',0.7)
            .style('z-index','-1')
            .on('mouseover',function(){
             
             this.style.stroke='red';
             this.style.opacity=1;
             d3.select(this)
               .style('z-index',999)
      
            var x='validator_index: '+v_line[i].index;
            d3.selectAll('.tooltip3')
              .html(x)
              .style("opacity",1.0)

            //  tooltip.html(x)
            //         .style("opacity",1.0);
            })
            .on('mouseleave',function(){
             this.style.stroke='#BFC9CA';
             this.style.opacity=0.7;
             d3.selectAll('.tooltip3').style("opacity",0);
             d3.select(this).style("z-index",-1)
            })
        }



      function  make_rect(i){
        for(let j=0;j<v_line[i].node.length;j++){
          if(v_line[i].node[j].y!=2){
            var y=v_line[i].node[j].y;
            var dy=v_line[i].node[j].dy;
            g.append('rect')
            .attr('class','v_rect')
            .attr('width',rect_width)
            .attr('height', rect_height_I*0.8)
            .attr('y',function(){
                var ans;
                if(!y)
                ans= (yscale2(y))+(dy-1)*rect_height_I+(SUM-graph[j][0]-graph[j][1])*rect_height_I;
                else
                ans=yscale2(y)-graph[j][1]*rect_height_I+(dy-1)*rect_height_I;
                return ans;
            })
            .attr('x',xscale2(j)+sub_width/2)
            .attr('fill',function(){
                if(v_line[i].node[j].isslashed)
                return 'black';
                else if(v_line[i].node[j].ispro)
                return '#6E00F5'
                else if(!y)
                return '#4D5656';
                else 
                return 'red';
            })
            .attr('opacity',v_line[i].node[j].ispro?1:0.8)
            .style('stroke',v_line[i].node[j].ispro?'#6E00F5':'none')
            .style('stroke-width',v_line[i].node[j].ispro?'0.5':'none')
          }
         }
        }
    for(let i=0;i< v_line.length;i++){
      make_line(i);
      make_rect(i);
    }
   

  }
   },
  created(){

  },
  watch:{
    message(){
        d3.select('#Validator').selectAll('g').remove()
        this.getValidator();
        console.log("draw");
        
      },
      vali(){
      // for(let i=0;i< v_line.length;i++){
      //  this.make_line(i);
      //  this.make_rect(i);
      // }
      this. data_processing();
    }
    }
}
</script>
<style>
 .axis text{
  font-family: sans-serif;
  font-size: 11px;
}

.v_line:hover{
  z-index:999;
  stroke-width:5px;
}

.tooltip3{
  position:absolute;
  stroke:black;
  left:850px;
  top:280px;
  width:auto;
  height:auto;
  border:1px solid lightcoral;
  border-radius:5px;
  padding-left:5px;
  padding-right:5px;
  padding-top:5px;
  padding:5px;
  background-color: white;
  font-size: 12px;
  text-align: center;
  opacity:0;
}

.panel-header_val {
  position: absolute;
  left:818px;
  top:250px;
  padding: 0px 5px;
  width: 75px;
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

.panel-header-end_val {
  position: absolute;
  top: 250px;
  left: 903px;
  border-top: 18px solid #455a64;
  border-right: 18px solid #ffffff;
  border-bottom: 0px solid #ffffff;
  z-index:98;
}
</style>