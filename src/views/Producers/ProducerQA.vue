<!-- HTML -->
<template>
    <NavBar />

    <!-- main content -->

    <div class="container pt-5">

        <!-- title -->
        <div class="d-grid gap-2" style="position: relative;">
            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="ms-5 bi bi-arrow-left-circle" viewBox="0 0 16 16" style="position: absolute; top: 10; left: 0;" v-on:click="goBack">
                <path fill-rule="evenodd" d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-4.5-.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5z"/>
            </svg>
            <h1> Q&As for {{ specified_producer["producerName"] }} </h1>
        </div>

        <!-- navtab to toggle between answered and unanswered -->
        <nav>
            <div class="nav nav-tabs justify-content-center" id="nav-tab" role="tablist">
                <button class="nav-link active w-25" id="nav-answered-tab" data-bs-toggle="tab" data-bs-target="#nav-answered" type="button" role="tab" aria-controls="nav-answered" aria-selected="true"> Answered </button>
                <button class="nav-link w-25" id="nav-unanswered-tab" data-bs-toggle="tab" data-bs-target="#nav-unanswered" type="button" role="tab" aria-controls="nav-unanswered" aria-selected="false"> Unanswered </button>
            </div>
        </nav>

        <!-- content in navtabs-->
        <div class="tab-content" id="nav-tabContent">

            <!-- answered questions -->
            <div class="tab-pane fade show active" id="nav-answered" role="tabpanel" aria-labelledby="nav-answered-tab">
                <!-- title-->
                <h3> Answered Questions </h3>
                <!-- number of answered questions -->
                <h5 v-if="answeredQuestions.length == 0"> No answered questions! </h5>
                <h5 v-else> {{ answeredQuestions.length }} answered questions! </h5>
                <!-- show all questions -->
                <div v-for="qa in answeredQuestions" :key="qa._id" class="py-3">
                    <div class="card text-start">
                        <div class="card-body">
                            <h5 class="card-title"> 
                                <b> Question: </b>
                                {{ qa.question }} 
                            </h5>
                            <p class="card-text"> 
                                <b> Answer: </b>
                                {{ qa.answer }}
                            </p>
                            <hr>
                            <b> Date: </b> {{ this.formatDate(qa.date.$date) }}
                        </div>
                    </div>
                </div>
            </div>

            <!-- unanswered questions -->
            <div class="tab-pane fade" id="nav-unanswered" role="tabpanel" aria-labelledby="nav-unanswered-tab">
                <!-- title-->
                <h3> Unanswered Questions </h3>
                <!-- number of unanswered questions -->
                <h5 v-if="unansweredQuestions.length == 0"> No unanswered questions! </h5>
                <h5 v-else> {{ unansweredQuestions.length }} unanswered questions! </h5>
                <!-- show all questions -->
                <div v-for="(qa, index) in unansweredQuestions" v-bind:key="qa._id" v-bind:class="{ 'active': index === 0 }" class="py-3">
                    <div class="card text-start">
                        <div class="card-body">
                            <h5 class="card-title"> 
                                <b> Question: </b>
                                {{ qa.question }} 
                            </h5>
                            <div class="card-text"> 
                                <b> Answer: </b>
                                <div class="d-flex align-items-center">
                                    <textarea class="search-bar form-control rounded fst-italic question-box flex-grow-1" type="text" placeholder="Respond to your fans latest questions." v-model="answers[qa._id.$oid]"></textarea>
                                    <div v-on:click="sendAnswer(qa)" class="send-icon ps-1">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                                            <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"/>
                                        </svg>
                                    </div>
                                </div>
                            </div>
                            <hr>
                            <b> Date: </b> {{ this.formatDate(qa.date.$date) }}
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div> <!-- end of main content -->

</template>

<!-- ---------------------------------------------------------------------------------------------------------------------------------------------------------- -->

<!-- JavaScript -->
<script>

    import NavBar from '@/components/NavBar.vue';


    export default {
        components: {
            NavBar
        },
        data() {
            return {
                // data from database
                producers: [],

                user_id: "",
                userType: "",
                correctProducer: false,

                // specified producer
                producer_id: null,
                specified_producer: {},

                // for Q&A section
                answeredQuestions: [],
                unansweredQuestions: [],

                // for answer
                answers: {},
            };
        },
        async mounted() {
            var userID = localStorage.getItem('88B_accID')
            if(userID != null){
                this.user_id = userID;
            }

            var userType = localStorage.getItem('88B_accType');
            if(userType != null){
                this.userType = userType;
                console.log(this.userType)
            }

            await this.loadData();
        },
        methods: {
            // load data from database
            async loadData() {
                // Get the query string parameters (listing ID) from the URL
                this.producer_id = this.$route.params.id;
                    if (this.producer_id == null) {
                        // redirect to page
                        this.$router.push('/');
                    }
                    else {
                        // check if user_id same as producer_id
                        if(this.user_id == this.producer_id && this.userType == "producer"){
                            this.correctProducer = true;
                        }
                    }
                // producers
                // _id, producerName, producerDesc, originCountry, statusOB, mainDrinks
                try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getProducers');
                        this.producers = response.data;
                        this.specified_producer = this.producers.find(producer => producer["_id"]["$oid"] == this.producer_id); // find specified producer
                        this.checkProducerQuestions();
                    } 
                    catch (error) {
                        console.error(error);
                    }
            },

            // go back to profile page
            goBack() {
                this.$router.go(-1)
            },

            // get producer's answered & unanswered questions
            checkProducerQuestions() {
                let answeredQuestions = this.specified_producer["questionsAnswers"];
                if (answeredQuestions.length > 0) {
                    for (let qa in answeredQuestions) {
                        let answer = answeredQuestions[qa]["answer"];
                        if (answer != "") {
                            this.answeredQuestions.push(answeredQuestions[qa]);
                        }
                        else {
                            this.unansweredQuestions.push(answeredQuestions[qa]);
                        }
                    }
                }
            },

            // format date
            formatDate(dateTimeString) {
                let datePart = dateTimeString.split("T")[0];
                // splitting the date into year, month, and day
                let [year, month, day] = datePart.split("-");
                // formatting the date
                let formattedDate = `${day}/${month}/${year}`;
                return formattedDate;
            },

            // send answer that producers give to users
            async sendAnswer (qa) {
                let q_and_a_id = qa._id.$oid;
                let answer = this.answers[q_and_a_id];
                try {
                    const response = await this.$axios.post('http://127.0.0.1:5200/sendAnswers', 
                        {
                            producerID: this.producer_id,
                            questionsAnswersID: q_and_a_id,
                            answer: answer,
                        },
                        {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                    console.log(response.data);
                } 
                catch (error) {
                    console.error(error);
                }

                // force page to reload
                window.location.reload();
            },

        }
    };
</script>