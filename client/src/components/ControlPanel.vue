<template>
  <div style="height: 100%">
    <div class="panel-header">政策文件</div>
    <div class="panel-header-end"></div>
    <a-table
      class="ant-table-selected"
      size="middle"
      :dataSource="dataSource"
      :columns="columns"
      :scroll="{ y: 856 }"
      :pagination="false"
      :showHeader="false"
      :customRow="customRow"
      :rowClassName="className"
    >
    </a-table>
  </div>
</template>

<script>
import { reactive, computed } from "vue";
import { useStore } from "vuex";

export default {
  setup(props) {
    const store = useStore();

    const dataSource = computed(() => store.getters.docList);
    const columns = reactive([{ title: "文件", dataIndex: "doc" }]);
    const customRow = (record) => {
      return {
        onClick: () => {
          store.commit("select", record.doc);
        },
      };
    };

    const selected = computed(() => store.selected);
    const className = (record) => {
      if (record === selected) {
        console.log(record);
      }
      return record === selected ? "table-selected" : null;
    };

    return {
      dataSource,
      columns,
      customRow,
      className,
    };
  },
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
