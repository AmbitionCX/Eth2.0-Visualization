<template>
  <div>
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
      epoch_index:-1
      }
    },
    methods:{
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
#Overview{
  position: absolute;
  top:10px;
  left:10px;
}

#Epoch {
  position: absolute;
  top:15px;
  left:860px;
  background: #ffffff;
  border-radius: 2px;
  border-color: blueviolet;
}
// #Epoch {
//   position: absolute;
//   top:415px;
//   left:10px;
//   background: #ffffff;
//   border-radius: 2px;
//   border-color: blueviolet;
// }

#Validator {
  position: absolute;
  top: 300px;
  left: 810px;
}

#Slot {
  position:absolute;
  top:360px;
  left:10px;
}

// #Slot {
//   position:absolute;
//   top:1000px;
//   left:10px;
// }


#app {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
</style>
