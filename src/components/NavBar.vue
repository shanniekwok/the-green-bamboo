<!-- Component for global Navigation Bar. Used in most pages on the application. -->

<!-- Requires Review. Search function is not complete, and may require modification. -->
<!-- TODO: Implement this component into all pages that require them, replacing in-built navbar code -->

<template>
    <div class="navbar-container">

        <!-- Main NavBar -->
        <nav class="navbar pb-0">
            <div class="container-fluid align-items-center col-xxl-11 col-xl-11 col-lg-11 col-md-12 col-sm-12">

                <!-- logo -->
                <div class="align-items-center col-3">
                    <router-link :to="'/'">
                        <img src="../../Images/Logo/88 Bamboo.png" style="width: 70px; height: 70px;">
                    </router-link>
                </div>

                <!-- search bar tzh added mobile-view-hide -->
                <div class="col-6 mobile-view-hide">
                    <input class="search-bar form-control rounded fst-italic" type="text" placeholder="What are you drinking today?" style="height: 50px;" v-model="searchInput" v-on:keyup.enter="goSearch">
                </div>

                <div class="col-3 dropdown mobile-col-4">

                    <!-- profile icon -->
                    <button v-if="onProfile" type="button" class="btn p-0 me-1" @click="forceLoad(profileURL)">
                        <svg v-if="photo == ''" xmlns="http://www.w3.org/2000/svg" width="45" height="45" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
                            <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                            <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
                        </svg>
                        <!-- <img v-else :src="'data:image/png;base64,'+ photo"  style="width: 45px; height: 45px;" class="img-border"> -->
                        <img v-else :src="photo"  style="width: 45px; height: 45px;" class="img-border">
                    </button>
                    <router-link v-if="!onProfile" :to="profileURL" class="me-1">
                        <button type="button" class="btn p-0">
                            <svg v-if="photo == ''" xmlns="http://www.w3.org/2000/svg" width="45" height="45" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
                                <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                                <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
                            </svg>
                            <!-- <img v-else :src="'data:image/png;base64,'+ photo"  style="width: 45px; height: 45px;" class="img-border"> -->
                            <img v-else :src="photo"  style="width: 45px; height: 45px;" class="img-border">
                        </button>
                    </router-link>

                    <!-- dropdown button -->
                    <button class="navbar-toggler p-0" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                        <span class="navbar-toggler-icon"></span>
                    </button>

                    <!-- dropdown menu -->
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li><router-link :to="'/'" class="dropdown-item">Home</router-link></li>

                        <li v-if="onProfile"><span class="dropdown-item" @click="forceLoad(profileURL)">My Profile</span></li>
                        <li v-if="!onProfile"><router-link :to="profileURL" class="dropdown-item">My Profile</router-link></li>

                        <li v-if="onCreate && (accType == 'producer' || isAdmin || isModerator)"><span class="dropdown-item" @click="forceLoad('/listing/create')">Create New Listing</span></li>
                        <li v-if="!onCreate && (accType == 'producer' || isAdmin || isModerator)"><router-link :to="'/listing/create'" class="dropdown-item">Create New Listing</router-link></li>

                        <li v-if="onRequest && accType == 'user'"><span class="dropdown-item" @click="forceLoad('/request/new')">Request New Listing</span></li>
                        <li v-if="!onRequest && accType == 'user'"><router-link :to="'/request/new'" class="dropdown-item">Request New Listing</router-link></li>

                        <li v-if="accType == 'user' || accType == 'producer'"><router-link :to="'/request/view'" class="dropdown-item">View Requests</router-link></li>

                        <li v-if="isAdmin"><router-link :to="'/admin/dashboard'" class="dropdown-item">Admin Dashboard</router-link></li>
                        <li v-if="isAdmin"><router-link :to="'/admin/importListings'" class="dropdown-item">Import Listings</router-link></li>
                        
                        <div class="mobile-view-show">
                            <li><router-link :to="'/'" class="dropdown-item">Explore</router-link></li>
                            <li><router-link :to="'/'" class="dropdown-item">Best Of</router-link></li>
                            <li><router-link :to="dashboardURL" class="dropdown-item">My {{ dashboardWord }} Stats</router-link></li>
                            <li><span  @click="externalURL('https://88bamboo.co/')" class="dropdown-item">Latest Drink News</span></li>
                            <li v-if="onRequest && accType == 'user'"><span style="color:#D58D2D !important;" @click="forceLoad('/request/new')" class="dropdown-item">Submit A Drink</span></li>
                            <li v-if="!onRequest && accType == 'user'"><router-link  :to="'/request/new'"><span class="dropdown-item" style="color:#D58D2D !important;">Submit A Drink</span></router-link></li>
                            <li v-if="onCreate && (accType == 'producer' || isAdmin || isModerator)" ><span style="color:#D58D2D !important;" class="dropdown-item" @click="forceLoad('/listing/create')">Add A New Drink</span></li>
                            <li v-if="!onCreate && (accType == 'producer' || isAdmin || isModerator)" :to="'/listing/create'" ><span style="color:#D58D2D !important;" class="dropdown-item">Add A New Drink</span></li>
                        </div>

                        <li><hr class="dropdown-divider"></li>
                        <li v-if="profileURL == '/login'"><router-link :to="'/login'" class="dropdown-item">Login</router-link></li>
                        <li v-if="profileURL == '/login'"><router-link :to="'/signup'" class="dropdown-item">Sign Up</router-link></li>
                        <li v-if="profileURL != '/login'"><span class="dropdown-item" @click="logout">Log Out</span></li>


                    </ul>

                </div>

            </div>
        </nav>

        <!-- secondary nav bar -tzh added mobile-view-hide -->
        <div class="col-12 primary-square mt-2 py-1 ">
            <div class="mobile-view-show col-12 ps-4 pe-4">
                <input class="search-bar form-control rounded fst-italic " type="text" placeholder="What are you drinking today?" style="height: 50px;" v-model="searchInput" v-on:keyup.enter="goSearch">
            </div>
            <div class="mobile-view-hide container-fluid align-items-center col-xxl-8 col-xl-9 col-lg-10 col-md-11 col-sm-12">

                <router-link :to="'/'">
                    <button class="btn primary-btn border-0 fw-bold" type="button">
                        Explore
                    </button>
                </router-link>

                <router-link :to="'/'">
                    <button class="btn primary-btn border-0 fw-bold" type="button">
                        Best Of
                    </button>
                </router-link>

                <router-link :to="dashboardURL">
                    <button class="btn primary-btn border-0 fw-bold" type="button">
                        My {{ dashboardWord }} Stats
                    </button>
                </router-link>

                <button class="btn primary-btn border-0 fw-bold" type="button" @click="externalURL('https://88bamboo.co/')">
                    Latest Drink News
                </button>

                <button @click="forceLoad('/request/new')" v-if="onRequest && accType == 'user'" class="btn primary-btn border-0 fw-bold text-warning" type="button" style="color:#D58D2D !important;">
                    Submit A Drink
                </button>
                <router-link v-if="!onRequest && accType == 'user'" :to="'/request/new'">
                    <button class="btn primary-btn border-0 fw-bold text-warning" type="button"  style="color:#D58D2D !important;">
                        Submit A Drink
                    </button>
                </router-link>

                <button @click="forceLoad('/listing/create')" v-if="onCreate && (accType == 'producer' || isAdmin || isModerator)" class="btn primary-btn border-0 fw-bold text-warning" type="button" style="color:#D58D2D !important;">
                    Add A New Drink
                </button>
                <router-link v-if="!onCreate && (accType == 'producer' || isAdmin || isModerator)" :to="'/listing/create'" >
                    <button class="btn primary-btn border-0 fw-bold text-warning" type="button" style="color:#D58D2D !important;">
                        Add A New Drink
                    </button>
                </router-link>
            </div>
        </div>

    </div>
</template>

<script>
    export default {
        name: "NavBar",
        data() {
            return {
                searchInput: '',
                accType: '',
                photo: '',
                profileURL: '/login',
                dashboardURL: '/login',
                isAdmin: false,
                isModerator: false,
                onProfile: false,
                onCreate: false,
                onRequest: false,
                dashboardWord: '',
            }
        },
        mounted() {
            // Obtain user's profile picture + set profile URL
            if (localStorage.getItem('88B_accID') != null) {

                this.accType = localStorage.getItem('88B_accType');
                let accID = localStorage.getItem('88B_accID');
                let url = 'http://127.0.0.1:5000/getData/get';

                if (this.accType == 'user') {
                    url = url + 'User/' + accID;
                    this.loadData(url);

                    this.profileURL = '/profile/user/'+accID;
                    this.dashboardURL = '/dashboard/user';
                    this.dashboardWord = 'Drink';
                } 
                else if (this.accType == 'producer') {
                    url = url + 'Producer/' + accID;
                    this.loadData(url);

                    this.profileURL = '/profile/producer/' + accID;
                    this.dashboardURL = '/Producers/ProducersDashboard/' + accID;
                    this.dashboardWord = 'Brand';
                    
                } 
                else if (this.accType == 'venue') {
                    url = url + 'Venue/' + accID;
                    this.loadData(url);

                    this.profileURL = '/profile/venue';
                    this.dashboardURL = '/dashboard/venue';
                    this.dashboardWord = 'Venue';
                }

                // check if current page is profile page
                if (this.$route.path.split('/')[1] == 'profile') {
                    this.onProfile = true;
                }

                // check if current page is create listing page
                if (this.$route.path.split('/').length >= 3 && this.$route.path.split('/')[2] == 'create') {
                    this.onCreate = true;
                }

                // check if current page is request page
                if (this.$route.path.split('/')[1] == 'request') {
                    this.onRequest = true;
                }
            }
        },
        methods: {
            // load data from database (profile picture)
            async loadData(url) {
                    try {
                        const response = await this.$axios.get(url);
                        this.photo = response.data["photo"];

                        if (this.accType == 'user') {
                            if (response.data.isAdmin) {
                                this.isAdmin = true;
                            }
                            if (Array.isArray(response.data.modType) && response.data.modType.length > 0) {
                                this.isModerator = true;
                            }
                        }
                    } 
                    catch (error) {
                        console.error(error);
                    }
            },

            // for search feature
            goSearch() {
                if (this.searchInput != '') {
                    // remove any '/' from search input
                    this.searchInput = this.searchInput.replace(/\//g, '');

                    // if already on search page, refresh the page with new search input
                    if (this.$route.path.split('/')[1] == 'search') {
                        window.location.href = '/search/' + this.searchInput;
                    }
                    else {
                        // re-route to search page
                        this.$router.push({path: '/search/' + this.searchInput});
                    }
                }
            },

            // logout function
            logout() {
                localStorage.removeItem('88B_accID');
                localStorage.removeItem('88B_accType');
                this.$router.push({path: '/login'});
            },

            // force reload of page
            forceLoad(url) {
                window.location.assign(this.$route.path.split('/')[0] + url);
            },

            // open external URL
            externalURL(url) {
                window.location.assign(url);
            }

        }
    }
</script>