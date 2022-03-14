<template>
  <div>
    <div>
      <Overview></Overview>
    </div>
    <div>
      <Epoch @details='Details'></Epoch> 
    </div>
    <div>
      <Slot v-if='details_display > 0' v-bind:msg = "details_display"/>
    </div>
  </div>
</template>
<script>
import Epoch from "./components/Epoch.vue"
import Overview from "./components/Overview.vue"
import Slot from "./components/Slot.vue"
export default {
    name:'App',
    components:{
      Epoch,
      Overview,
      Slot
    },
 
    data(){
      return{
      details_display: 0
      }
    },
    methods:{
      Details(data){
        this.details_display = data;
      }
    }
  }
</script>
<style lang="scss">

#Epoch {
  position: absolute;
  top:15px;
  left:10px;
  background: #ffffff;
  border-radius: 2px;
  border-color: blueviolet;
}

#Slot {
  position:absolute;
  top:400px;
  left:10px;
}

a {
  text-decoration: none;
}
.el-menu-item.is-disabled {
  opacity: 1;
  color: gray;
}
.el-menu-item {
  height: 30px;
}
.activeText {
  font-size: 1.3em;
  color: black;
  opacity: 1
}

#nav {
  padding: 5px;

  a {
    font-weight: bold;
    color: #2c3e50;
    &.router-link-exact-active {
      color: #409EFF;
    }
  }
}

  #app {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
</style>
