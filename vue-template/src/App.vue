<template>
  <div>
    <svg id = "botteomLayer" style = 'width:1260px; height:570px; background-color:lightgrey'></svg>
    <Overview @day_detail = 'DayDetail'></Overview>
    <Epoch v-if = 'epoch_index >= 0' v-bind:day = "epoch_index"
             @details='Details'>
    </Epoch> 
    <Validator v-if= 'details_display > 0' v-bind:msg = "details_display"></Validator>
    <Slot v-if= 'details_display > 0' v-bind:msg = "details_display"> </Slot>
  </div>
</template>
<script>
import Epoch from "./components/Epoch.vue"
import Overview from "./components/Overview.vue"
import Slot from "./components/Slot.vue"
import Validator from "./components/Validator.vue"
export default {
    name:'App',
    components:{
      Epoch,
      Overview,
      Slot,
      Validator
    },
 
    data(){
      return{
      details_display: 0,
      epoch_index:-1,
      value:0
      }
    },
    mounted(){
  },
    methods:{
      // check(){
      //   this.value ++;
      //   console.log(this.value);
      // },
      Details(data){
        this.details_display = data;
      },
      DayDetail(data){
        this.epoch_index = data;
      }
    }
  }
</script>
<style lang="scss">
#bottomLayer{
  z-index: -1;
}
#Overview{
  position: absolute;
  top:0px;
  left:3px;
  background: #ffffff;
  z-index:0;
}

#Epoch {
  position: absolute;
  top:0px;
  left:823px;
  background: #ffffff;
  border-radius: 2px;
  border-color: blueviolet;
  z-index:0;
}

#Validator {
  position: absolute;
  top: 252px;
  left: 823px;
  background: #ffffff;
}

#Slot {
  position:absolute;
  top:252px;
  left:3px;
  background: #ffffff;
}


#app {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
</style>
