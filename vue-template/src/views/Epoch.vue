  <template>
<svg id = "mainsvg" style = 'width:4200px; height:3600px'>
    <text>'Testing'</text>
    <button id = 'ghost' style = 'appearance: none;
    background-color: #2ea44f;
    border: 1px solid rgba(27, 31, 35, .15);
    border-radius: 6px;
    box-shadow: rgba(27, 31, 35, .1) 0 1px 0;
    box-sizing: border-box;
    color: #fff;
    cursor: pointer;
    display: inline-block;
    font-family: -apple-system,system-ui,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji";
    font-size: 56px;
    font-weight: 1200;
    line-height: 80px;
    padding: 24px 64px;
    position: relative;
    text-align: center;
    text-decoration: none;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
    vertical-align: middle;
    white-space: nowrap'
    @click = 'GHOST(epochs)'>Head</button><br/>
    <button @click = 'Casper(epochs)'>Checkpoint</button>
</svg>



</template>

<script>
export default {
  name:'Epoch',
  data(){

  },
  mounted(){

  },
  computed:{

  },
  methodes:{

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
