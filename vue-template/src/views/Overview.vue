 <template>
<div>
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
      epochs:[],
      width: 2000,
      height: 1750,
      margin:{
        top:100,
        right:90,
        bottom:60,
        left:90
      },
      r:15,
      c:15
    };
  },
  mounted(){
    this.Scale();
  },
  computed:{
    innerWidth(){
      return this.width - this.margin.left - this.margin.right
    },
    innerHeight(){
      return this.height - this.margin.top - this.margin.bottom
    }
  },
  methods:{
     getAll(){
       const path = 'http://127.0.0.1:5000/Overview';
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
      const g = d3.select('svg').append('g').attr('id', 'maingroup')
                   .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
      const xscale = d3.scaleLinear()
                       .domain([0,this.c])
                       .range([0, this.innerWidth]);
      const yscale = d3.scaleLinear()
          .domain([0,this.r])
          .range([0, this.innerHeight]);

      const yaxis = d3.axisLeft(yscale)
          .ticks(this.r)
          .tickSize(10)
          .tickPadding(10);
      const xaxis = d3.axisBottom(xscale)
          .ticks(this.c)
          .tickSize(-10)
          .tickPadding(-50);
          g.append('g').call(yaxis)
    .attr('id' ,'yaxis');
  g.append('g').call(xaxis)
    .attr('id', 'xaxis');
  },

  },
  created(){
    this.getAll();
  },
  watch:{

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
