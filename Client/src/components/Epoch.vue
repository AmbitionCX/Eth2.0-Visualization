  <template>
  <div id='text'>
    <text>text:{{msg}}</text>
</div>


</template>

<script>
//import axios from 'axios';

export default {
  name:'Epoch',
  data(){
    return {
      msg:100
    };
  },
  mounted(){

  },
  computed:{
    time(){
      
      // var d = new Date();
      // console.log(d.getTime());
      return this.msg;
    }
  },
  methods:{

     }

   },
   created(){
    //  var d = new Date();
    //   console.log(d.getTime());
   },
  watch:{
    time(){
      console.log(this.time)
      this.msg = this.time;
    }

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
