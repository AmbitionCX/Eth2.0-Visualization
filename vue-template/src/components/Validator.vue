<template>
  <div>
    <svg id = "Validator" style = 'width:700px; height:340px'>
    </svg>
    <text>This is the Validator View</text>
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
      casper:[],
      proposer:[],
      width: 700,
      height: 340,
      margin:{
        top:30,
        right:130,
        bottom:0,
        left:30
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
    val(){
      console.log(this.casper);
      return this.casper.reverse()
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
          this.casper=res.data[0];
          this.proposer = res.data[1]
        })
        .catch(error => {
          console.error(error);
        });

    },

    data_processing(){

    const g = svg.append('g').attr('id', 'maingroup')
      .attr('transform', `translate(${margin.left},${margin.top})`);
      
      var tooltip3 = d3.select("body")
		                   .append("div")
		                   .attr("class","tooltip3")
      


let that = this;

for(j=that.casper[that.casper.length-1].validator.length-1;j>0&&that.casper[that.casper.length-1].validator[j].vote==-2;j--)

for(i=0;i<that.casper.length;i++){
    that.casper[i].validator.splice(j,1);
}


that.proposer=that.proposer.reverse();


 const SUM=that.val[0].validator.length;


//  console.log(data);

 var graph = [];
 var v_line = [];
 for(var i=0; i < SUM; i++)
   v_line.push({index:that.val[0].validator[i].validator_index,node:[]});
 for(var i=0;i<that.val.length;i++){
    graph.push([]);
    for( var j=0;j<2;j++){
        graph[i].push(0);
    }
 }

 //graph保留数量信息
var k = []
for(var i = 0;i < that.proposer.length; i++)
 k.push(0);
for(var j = 0; j < SUM; j++){
  for(var i = 0; i < that.val.length; i++){
   while(k[i] < that.proposer[i].length && that.val[i].validator[j].validator_index>that.proposer[i][k[i]])
        k[i]++;
    var Y=that.val[i].validator[j].vote+1;
    if(Y==-1)
       console.log(i,j);
    if(Y<2){
    if(Y<0)
        Y=0;
    var X= ++graph[i][Y];
    v_line[j].node.push( {dy:X,y:Y,ispro:0});
    }
    else{
     v_line[j].node.push( {dy:0,y:2,ispro:0})
    }
    if(k[i]<proposer[i].length&&that.val[i].validator[j].validator_index==proposer[i][k[i]])
    v_line[j].node[i].ispro=1;
   }
}
console.log(proposer);
console.log(graph);
console.log(v_line);

    var data_rect=[];
   for(var i=0;i<graph.length;i++){
       for(var j=0;j<graph[i].length;j++){
        data_rect.push({i:i,j:j,size:graph[i][j]})
       }
   }

 //设置矩阵的行列
var r=2,c=that.val.length;
const yValue=['decline','abstain'];
const xValue=[];
for(let i=0;i<c;i++){
    xValue.push('epoch:'+ that.val[i].epoch);
}
//设置坐标轴
const xscale = d3.scaleBand()
        .domain(xValue)
        .range([0, that.innerWidth]);

 const xscale2 = d3.scaleLinear()
        .domain([0,c])
        .range([0, that.innerWidth]);
const yscale = d3.scalePoint() 
        .domain(yValue)
        .range([that.innerHeight,0])
        
const yscale2 = d3.scaleLinear() 
        .domain([0,1])
        .range([0,that.innerHeight])
const yaxis = d3.axisLeft(yscale)
        .ticks(r)
        .tickSize(10)
        .tickPadding(10)
const xaxis = d3.axisTop(xscale)
        .ticks(c)
        .tickSize(-10)
        .tickPadding(-50);
g.append('g').call(yaxis)
        .attr('id' ,'yaxis') 
        .style("font-size","24px");
 
g.append('g').call(xaxis)
        .attr('id', 'xaxis')
        .attr('transform', `translate(0, ${that.innerHeight})`)
        .style("font-size","20px");
//添加矩阵

const  rect_width=innerWidth/(5*c);
const  sub_width=innerWidth/c-rect_width;
const rect_height_I=innerHeight/SUM;
// g.selectAll('.datarect').data(data_rect).enter().append('rect')
// .attr('class','datarect')
// .attr('width',rect_width)
// .attr('height', d=>d.size*rect_height_I)
// .attr('y',function(d){
//     if(!d.j)
//     return (yscale2(d.j));
//     else
//     return yscale2(d.j)-d.size*rect_height_I;
// })
// .attr('x',d=>xscale2(d.i))
// .attr('fill',function(d){
//     if(!d.j)
//     return 'grey';
//     else 
//     return 'red';
// })
// .attr('opacity',0.8);


var x1=[];
var x2=[];
for(j=0;j<that.val.length-1;j++){
       x1.push((j+1)*rect_width+j*sub_width+sub_width/2);
       x2.push((j+1)*rect_width+(j+1)*sub_width+sub_width/2);
  }

    },

    make_line(i){
      var Y=[];
      var y1=[];
      var y2=[];
      for(j=0;j<that.val.length;j++){
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
    for(j=0;j<y1.length;j++){
       if((v_line[i].node[j+1].y==1||v_line[i].node[j+1].y==0)&&(v_line[i].node[j].y==0||v_line[i].node[j].y==1)){
        var dx=(x2[j]-x1[j])/20;
        var dy=(y2[j]-y1[j])/3;
        let cpx1 = x1[j] + dx;
        let cpy1 = y1[j] + dy;
        let cpx2 = x2[j] - dx;
        let cpy2 = y2[j] - dy;
        path.moveTo(x1[j],y1[j]);
        //path.bezierCurveTo(cpx1,cpy1,cpx2,cpy2,x2[j],y2[j]);  //曲线
        path.lineTo(x2[j],y2[j]);                                //直线
       }

    }
    g.append('path')
            .attr('class','v_line')
            .attr('d', path.toString())
            .style('stroke','blue')
            .style('stroke-width','0.5')
            .style('fill','none')
            .style('opacity','0.7')
            .on('mouseover',function(){
             this.style.stroke='red';
             this.style.opacity=1;
             var x='validator_index: '+v_line[i].index;
             tooltip3.html(x)
				.style("left", margin.left+150+"px")
				.style("top", margin.top+50+"px")
				.style("opacity",1.0);
            })
            .on('mouseleave',function(){
             this.style.stroke='blue';
             this.style.opacity=0.7;
             tooltip3
				.style("opacity",0.0);
            })
        },

        make_rect(i){
        for(j=0;j<v_line[i].node.length;j++){
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
                if(v_line[i].node[j].ispro)
                return '#6E00F5'
                else if(!y)
                return 'grey';
                else 
                return 'red';
            })
            .attr('opacity',v_line[i].node[j].ispro?1:0.8)
            .style('stroke',v_line[i].node[j].ispro?'#6E00F5':'none')
            .style('stroke-width',v_line[i].node[j].ispro?'0.5':'none')
          }
         }
        }

  },
  created(){

  },
  watch:{
    message(){
        this.getValidator();
        d3.select('#Validator').selectAll('g').remove()
        console.log("draw");
      },
      val(){
      for(let i=0;i< v_line.length;i++){
       this.make_line(i);
       this.make_rect(i);
      }
    }
    }
}
</script>
<style scoped>

</style>