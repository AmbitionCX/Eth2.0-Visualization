<template>
<div>
  <Epoch/>
  <Overview/>
</div>
</template>
<script>
import Epoch from "./components/Epoch.vue"
import Overview from "./components/Overview.vue"
export default {
    name:'App',
    components:{
      Epoch,
      Overview
    }
  }
</script>
<style lang="scss">

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
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
