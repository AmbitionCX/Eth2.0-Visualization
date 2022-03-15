<template>
  <div>
    <text id = "Validator">This is the Validator View</text>
  </div>
</template>

<script>
//import axios from 'axios'
//import * as d3 from 'd3'

export default {
  name:'Validator',
  props:["msg"],
  data(){
    return {
    };
  },
  mounted(){

  },
  computed:{
    message(){
      console.log(this.msg);
      return this.msg;
    }
  },
  methods:{

  },
  created(){

  },
  watch:{
      message(){

      }
    }
}
</script>
<style scoped>

</style>