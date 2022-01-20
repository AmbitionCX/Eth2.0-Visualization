<template>
  <a-row :gutter="[2, 2]">
    <a-col :span="6">
      <ControlPanel id="control_panel_container"/>
    </a-col>
    <a-col :span="18">
      <DataTable id="policy_detail_container"/>
    </a-col>
  </a-row>
</template>

<script>
import { ref } from "vue";
import DataTable from "./components/DataTable.vue";
import ControlPanel from "./components/ControlPanel.vue";

export default {
  name: "App",
  components: {
    DataTable,
    ControlPanel,
  },
  computed: {},
  data() {
    return {
      // checked: ref(false),
    };
  },
  watch: {},
  mounted: function () {},
  methods: {},
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  width: 1600px;
  height: 900px;
  margin: 2px;
  border: 1px solid lightblue;
}

#control_panel_container {
  height: 1123px;
  border: 1px solid #455a64;
  width: 100%;
  box-sizing: border-box;
}

#policy_detail_container {
  height: 1123px;
  width: 100%;
  border: 1px solid #455a64;
}
</style>
