<template>
  <div style="height: 100%">
    <div class="panel-header">政策明细</div>
    <div class="panel-header-end"></div>
    <a-table
      :dataSource="dataSource"
      :columns="columns"
      :pagination="false"
      :scroll="{ x: 1190, y: 795 }"
      @resizeColumn="handleResizeColumn"
    >
      <template #entity_type="{ text }">
        <a-tag :color="text == '政策文号'? 'volcano': text == '句子类型'? 'purple': 'cyan'">
          {{ text }}
        </a-tag>
      </template>
    </a-table>
  </div>
</template>

<script>
import { reactive, computed } from "vue";
import { useStore } from "vuex";

export default {
  setup(props) {
    const store = useStore();

    // const dataSource = computed(() => store.getters.sentences);
    const dataSource = computed(() => store.getters.getSelectedDoc);

    const columns = reactive([
      // { title: "文件", dataIndex: "doc_index", fixed: true, minWidth: 100 },
      {
        title: "句子编号",
        key: "sen_index",
        dataIndex: "sen_index",
        resizable: true,
        minWidth: 100,
        width: 100,
      },
      {
        title: "实体类别",
        key: "entity_type",
        dataIndex: "entity_type",
        resizable: true,
        minWidth: 100,
        width: 100,
        slots: { customRender: "entity_type" },
      },
      {
        title: "实体",
        key: "entity",
        dataIndex: "entity",
        resizable: true,
        width: 500,
      },
      {
        title: "句子",
        key: "sentence",
        dataIndex: "sentence",
        resizable: true,
        width: 500,
      },
    ]);

    return {
      dataSource,
      columns,
      handleResizeColumn: (w, col) => {
        col.width = w;
      },
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
</style>
