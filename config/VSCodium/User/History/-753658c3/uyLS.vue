<template>
    <div class="flex h-screen">
        <div class="bg-white rounded-xl m-5 ml-10 w-1/5 p-5" style="height: calc(100%);">
            <h1 class="text-xl font-bold">Вопросы:</h1>
            <div class="flex-col">
                <div class="flex justify-between">
                    <div class="flex-col">
                        <div class="mt-3" v-for="q, i in questions" :key="q.id">
                            <div @click="change_selected_question(q)"
                                class="flex text-gray-500 hover:text-blue-600 hover:cursor-pointer transition-all select-none">
                                <h1 class="mr-3 px-2 rounded-full font-bold"
                                    :class="q == selected_question ? 'bg-blue-600 text-white' : 'bg-gray-200'">{{ i + 1 }}
                                </h1>
                                <v-tooltip :text="q.question" location="end">
                                    <template v-slot:activator="{ props }">
                                        <h1 v-bind="props">{{ (q.question.length > 20) ? q.question.slice(0, 20) + "..." :
                                            q.question }}</h1>
                                    </template>
                                </v-tooltip>
                                <div class="ml-5">
                                    <v-icon v-if="results.find(el => el[0] === q && el[1] == true)" icon="mdi-check-circle"
                                        color="green"></v-icon>
                                    <v-icon v-if="results.find(el => el[0] === q && el[1] == false)" icon="mdi-close-circle"
                                        color="red"></v-icon>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="flex flex-col mt-5 border-t pt-5 select-none">
                    <div class="text-xl font-bold border-2 p-5 rounded-xl">
                        {{ selected_question.question }}
                    </div>
                    <complexity-line class="mt-2" :complexity="selected_question.complexity"></complexity-line>
                </div>
            </div>
        </div>
        <div class="flex flex-col w-3/5 flex-grow" style="height: calc(100% + 40px);">
            <div class="bg-white rounded-xl m-5 flex-grow p-5 pb-20">
                <div class="flex flex-col h-5">
                    <div class="block">
                        <textarea ref="sqlEditor"></textarea>
                    </div>
                    <div class="flex justify-end border-t-2 pt-5">
                        <v-btn v-if="results.some(([question, _]) => question === selected_question)" disabled
                            @click="send_answer" rounded="lg" variant="flat" color="blue-accent-4">Вы уже ответили</v-btn>
                        <v-tooltip v-else text="Вы можете отправить ответ только 1 раз" location="top">
                            <template v-slot:activator="{ props }">
                                <v-btn v-bind="props" @click="send_answer" rounded="lg" variant="flat"
                                    prepend-icon="mdi-check" color="blue-accent-4">Отправить ответ</v-btn>
                            </template>
                        </v-tooltip>
                        <v-btn class="ml-5" rounded="lg" prepend-icon="mdi-play" variant="outlined"
                            @click="send_query">Выполнить</v-btn>
                    </div>
                    <div>
                        <h1 class="text-xl font-bold">Результат запроса:</h1>
                        <v-alert rounded="pill" class="mt-10" closable v-if="error" :text="error" type="error"></v-alert>
                        <ResponseTable class="mt-5" :result="response" />
                        <v-progress-linear v-if="loading" color="blue-accent-4" indeterminate
                            :height="10"></v-progress-linear>
                    </div>
                </div>
            </div>
        </div>
        <div class="bg-white rounded-xl m-5 mr-10 w-1/5 p-5 flex flex-col justify-between"
            style="height: calc(100% );">
            <div>
                <v-zoomer :pivot="'image-center'" ref="er_diagram" class="h-96 rounded-xl border-2 mb-5">
                    <img :src="'data:image/png;base64,' + er_diagram" alt="ER Diagram"
                        style="object-fit: contain; width: 100%; height: 100%;">
                </v-zoomer>
                <div>
                    <v-btn size="sm" @click="$refs.er_diagram.zoomIn(scale = 2)" class="mr-2" variant="outlined"
                        icon="mdi-plus">
                    </v-btn>

                    <v-btn size="sm" @click="$refs.er_diagram.zoomOut(scale = 0.5)" class="mr-2" variant="outlined"
                        icon="mdi-minus">
                    </v-btn>

                    <v-dialog v-model="dialog" width="auto">
                        <template v-slot:activator="{ props }">
                            <v-btn size="sm" variant="outlined" icon="mdi-fullscreen" v-bind="props">
                            </v-btn>
                        </template>
                        <v-card rounded="xl">
                            <v-zoomer ref="er_diagram" class="rounded-xl">
                                <img :src="'data:image/png;base64,' + er_diagram" alt="ER Diagram"
                                    style="object-fit: width: 100%; height: 100%;">
                            </v-zoomer>
                            <v-card-actions>
                                <v-btn rounded="pill" color="blue-accent-4" block @click="dialog = false">Закрыть</v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                    <div class="mt-5">
                        <v-btn v-if="results.length === questions.length" @click="send_results" class="w-full"
                append-icon="mdi-arrow-right" rounded="lg" color="blue-accent-4">Завершить</v-btn>

                        <v-btn v-else disabled @click="send_results" class="w-full" append-icon="mdi-arrow-right" rounded="lg"
                            color="blue-accent-4">Завершить</v-btn>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
body {
    margin-top: 85px;
}
</style>

<script>
import pb from "../pocketbase.js";
import { mapGetters } from 'vuex'
import { user_db_api } from "../api";
import { emitter } from '../eventBus'
import SqlEditor from "../components/SqlEditor.vue";
import ResponseTable from "../components/ResponseTable.vue"
import ComplexityLine from "../components/ComplexityLine.vue"

export default {
    components: {
        SqlEditor,
        ResponseTable,
        ComplexityLine
    },
    data() {
        return {
            test_id: this.$route.params.testId,
            questions: [],
            dialog: false,
            number_of_questions: 0,
            response: [],
            selected_question: "",
            error: '',
            er_diagram: '',
            answer: [],
            loading: false,
            results: [],
            show_answer_status_good: false,
            show_answer_status_bad: false
        }
    },
    computed: {
        ...mapGetters(['currentUser']),
    },
    methods: {
        async fetch_questions() {
            this.questions = await pb.collection('questions').getFullList({
                filter: `test_id = "${this.test_id}"`,
                sort: '-created',
            });
            this.number_of_questions = this.questions.length
        },

        async send_query() {
            this.loading = true;

            const user_query = this.editor.getValue().replace(/\n/g, ' ');
            try {
                this.error = '';
                const response = await user_db_api.query_to_user_db(this.test_id, user_query);
                this.response = response.data;
            } catch (error) {
                this.error = 'Error: ' + error.response.data.detail;
                this.response = [];
            }
            this.loading = false;
        },


        async change_selected_question(q) {
            this.selected_question = q
            this.answer = await user_db_api.query_to_user_db(this.test_id, this.selected_question.correct_answer)
        },

        async send_answer() {
            try {
                const user_query = this.editor.getValue().replace(/\n/g, ' ');
                const user_answer = await user_db_api.query_to_user_db(this.test_id, user_query)

                this.results.push([this.selected_question, JSON.stringify(this.answer.data.result) == JSON.stringify(user_answer.data.result)])

                if (this.questions.indexOf(this.selected_question) >= this.questions.length - 1) {
                    this.selected_question = this.questions[0]
                } else {
                    this.change_selected_question(this.questions[this.questions.indexOf(this.selected_question) + 1])
                }

                this.editor.setValue('')
            } catch (error) {
                console.log(error)
                this.error = 'Error: ' + error.response.data.detail;
                this.response = []; s
            }
        },

        async send_results() {
            const data = {
                "user_id": this.currentUser.id,
                "test_id": this.test_id,
                "correct_answers": this.results.filter(pair => pair[1] === true).length,
                "number_of_questions": this.questions.length
            }
            await pb.collection('results').create(data);
            this.$router.push("/")
        }
    },
    async mounted() {
        emitter.on('questionsUpdated', () => {
            this.fetch_questions();
        });
        this.fetch_questions();
        const sqlEditor = this.$refs.sqlEditor;
        this.editor = CodeMirror.fromTextArea(sqlEditor, {
            mode: 'text/x-sql',
            lineNumbers: true,
            autofocus: true,
        });
        this.er_diagram = await user_db_api.create_er_diagram(this.test_id)
        this.er_diagram = this.er_diagram.data.er_diagram
        this.change_selected_question(this.questions[0])
        this.answer = await user_db_api.query_to_user_db(this.test_id, this.selected_question.correct_answer)
    },
}
</script>
