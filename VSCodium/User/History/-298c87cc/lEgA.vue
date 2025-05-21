<template>
    <div>

        <div class="mt-28">
            <v-row justify="center">
                <v-col cols="12" sm="8" md="8">
                    <v-card rounded="xl" color="white">
                        <div class="p-5">
                            <v-card-title>
                                <div class="flex justify-between align-middle text-center">
                                    <h1 class="text-3xl font-black">❓ Вопросы для теста: <p class="inline-block"
                                            v-if="number_of_questions != 0">{{ number_of_questions }}</p>
                                    </h1>
                                    <create-question-btn :test_id="test_id" />
                                </div>
                            </v-card-title>
                            <v-card-text>
                                <transition-group name="slide">
                                    <div class="mt-5" v-for="question, i in questions" :key="question.id">
                                        <div class="flex flex-col">
                                            <question-card :question="question.question" :answer="question.correct_answer"
                                                :id="question.id" :complexity="question.complexity" :counter="i + 1" />
                                        </div>
                                    </div>
                                </transition-group>
                            </v-card-text>
                        </div>
                    </v-card>
                    <v-card v-if="draw" rounded="xl" color="white" class="mt-10">
                        <div class="p-5">
                            <v-card-title>
                                <div class="flex justify-between align-middle text-center">
                                    <h1 class="text-3xl font-black">📊 Статистика: </h1>
                                </div>
                            </v-card-title>
                            <v-card-text>
                                <div class="flex">
                                    <v-table>
                                        <thead>
                                            <tr>
                                                <th class="text-left">
                                                    Группа
                                                </th>
                                                <th class="text-left">
                                                    Студент
                                                </th>
                                                <th class="text-left">
                                                    Правильных ответов
                                                </th>
                                                <th class="text-left">
                                                    Время ответа
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="item in results" :key="item.id">
                                                <td>{{ item.expand.user_id.group }}</td>
                                                <td>{{ item.expand.user_id.name }}</td>
                                                <td>{{ item.correct_answers }} / {{ item.number_of_questions }}</td>
                                                <td>{{ new Date(item.created).toLocaleString(undefined, { hour12: false })
                                                }}
                                                </td>
                                            </tr>
                                        </tbody>
                                    </v-table>
                                    <div class="w-1/3">
                                        <Doughnut v-if="draw" id="my-chart-id" :options="chartOptions"
                                            :data="chart_data" />
                                    </div>
                                </div>
                            </v-card-text>
                        </div>
                    </v-card>
                </v-col>
            </v-row>
        </div>
    </div>
</template>

<script>
import pb from "../pocketbase.js";
import { mapGetters } from 'vuex'
import { emitter } from '../eventBus'
import QuestionCard from "../components/QuestionCard.vue";
import CreateQuestionBtn from "../components/CreateQuestionBtn.vue";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Doughnut } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend)

export default {
    components: {
        QuestionCard,
        CreateQuestionBtn,
        Doughnut
    },
    data() {
        return {
            test_id: this.$route.params.testId,
            questions: null,
            dialog: false,
            number_of_questions: 0,
            results: [],
            chartOptions: {
                responsive: true,

            },
            draw: false,
            chart_data: {}
        }
    },
    computed: {
        ...mapGetters(['currentUser']),
    },
    methods: {
        async delete_question(test_id) {
            await pb.collection('tests').delete(test_id)
            await this.fetch_questions()
        },
        async fetch_questions() {
            this.questions = await pb.collection('questions').getFullList({
                filter: `test_id = "${this.test_id}"`,
                sort: '-created',
            });
            this.number_of_questions = this.questions.length
        },
        async fetch_chart_data(res) {
            console.log(res)
            this.chart_data = {
                labels: Array.from(Array(res[0].number_of_questions + 1).keys(), x => (x).toString()),
                datasets: [
                    {
                        backgroundColor: ['#3662E3', '#436CE5', '#2353E1', '#1A44C2', '#7D99ED', '#A8BBF3', '#13328D'],
                        data: Array.from(Array(res[0].number_of_questions + 1).keys(), x => (x)).map(grade => res.map(result => result.correct_answers).filter(result => result === grade).length)
                    }
                ]
            }
            console.log(this.chart_data)
        }
    },
    async mounted() {
        emitter.on('questionsUpdated', () => {
            this.fetch_questions()
        })
        this.fetch_questions()

        const res = await pb.collection('results').getFullList({
            sort: '-created',
            expand: 'user_id, users.id',
            filter: `test_id = "${this.test_id}"`
        })

        if (res.length > 0){
            this.results = res
            this.fetch_chart_data(res)
            this.draw = true
        }
    }
}
</script>


<style>
.slide-enter-active,
.slide-leave-active {
    transition: all 0.5s cubic-bezier(0.5, 0, 0.5, 1);
}

.slide-enter {
    transform: translateX(-100%) scale(0.8);
    opacity: 0;
}

.slide-leave-to {
    transform: translateX(100%) scale(0.8);
    opacity: 0;
}
</style>
