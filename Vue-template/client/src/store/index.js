import { createStore } from "vuex";
import document from "../assets/document.json";

export default createStore({
  state: {
    data: document,
    selected: null,
  },
  getters: {
    /* Define how different views access the global data. */
    docList(state) {
      return [...new Set(state.data.map((d) => d.doc_index))]
        .sort()
        .map((d) => {
          return { doc: d };
        });
    },
    getSelectedDoc: (state) => {
      return state.data.filter((record) => record.doc_index == state.selected);
    },
    sentences(state) {
      return state.data;
    },
  },
  mutations: {
    /* Change state value in synchronous manner*/
    update(state, payload) {
      state[payload.field] = payload.data;
    },
    select(state, doc_index) {
      state.selected = doc_index;
    },
  },
  actions: {
    /* only functions here can use mutations in asynchronous manner*/
    async getDocuments(context) {
      // console.log(document[0])
    },
    notify(context) {
      context.commit("simpleNotify");
    },
  },
  modules: {},
});
