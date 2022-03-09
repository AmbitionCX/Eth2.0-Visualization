<template>
  <div class="template">
    <h1>This is an illustration page for HTML template in Vue.js.</h1>
    <p>
      Ask a yes/no question:
      <input v-model="question" />
    </p>
    <p>   Reverse: {{ question.split('').reverse().join('')}} </p>
    <p>Answer: {{ answerFull }}</p>

    <br />
    <button @click="say('hi')">Say hi</button>
    &nbsp;
    <button v-on:click="say('what')">Say what</button>

    <br />


  </div>
</template>

<script lang="js">
import * as axios from "axios"
export default {
    name: "Component",
    components: {

    },
    data() {
        return {
            question: '',
            answer: 'Questions usually contain a question mark.'
        }
    },
    computed: { /* computed dynamic data (based on basic data)*/
        answerFull() {
            return this.answer + ';-)'
        }
    },
    mounted() {

    },
    watch: {  /* watch data change */
      // whenever the variable question changes, this function will run
      question(newQuestion, oldQuestion) {
        console.log('question changed:', oldQuestion, '->', newQuestion)
        if (newQuestion.indexOf('?') > -1) {
          this.getAnswer()
        }
      }
    },
    methods: {
        getAnswer() {
            this.answer = 'Thinking...'
            // send a request to backend
            axios
            .get('https://yesno.wtf/api')
            .then(response => {
                this.answer = response.data.answer
            })
            .catch(error => {
                this.answer = 'Error! Could not reach the API. ' + error
            })
        },
         say(message) {
          alert(message)
        }
    }

}
</script>

<style lang="scss" scoped>
p {
  font-size: 1em;
}
</style>
