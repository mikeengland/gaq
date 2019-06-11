<template>
    <v-app>
        <v-toolbar app>
            <v-toolbar-title class="headline text-uppercase">
                <span>GAQ -&nbsp;</span>
                <span class="font-weight-light">Query Google Ads reports interactively</span>
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <span
                    class="customer-id-nav"
                    v-show="customerId"
                    @click="changeCustomerId"
            >Account ID: {{ this.customerId }}</span>
        </v-toolbar>

        <v-content>
            <Welcome @clicked="onCustomerClick" v-show="!customerId"/>
            <Query v-show="customerId" :customerId="customerId" :loginCustomerId="loginCustomerId"/>
        </v-content>
        <v-footer height="auto" color="primary lighten-1">
            <v-layout justify-center>
        <span>
          For documentation on building queries, click
          <a href="https://developers.google.com/google-ads/api/docs/query/interactive-gaql-builder"
             target="_blank"
             rel="noopener noreferrer"
          >here</a>
        </span>
            </v-layout>
        </v-footer>
    </v-app>
</template>

<style scoped>
    .customer-id-nav {
        cursor: pointer;
        font-size: 12px;
    }

    .v-footer span {
        color: #ffffff;
        padding-left: 10px;
    }

    .v-footer a {
        color: #ffffff;
    }
</style>

<script>
  import Query from "./components/Query";
  import Welcome from "./components/Welcome";

  export default {
    name: "App",
    components: {
      Query,
      Welcome
    },
    methods: {
      onCustomerClick: function (loginCustomerId, customerId) {
        this.customerId = customerId;
        this.loginCustomerId = loginCustomerId;
      },
      changeCustomerId: function () {
        this.customerId = null;
        this.loginCustomerId = null;
      }
    },
    data() {
      return {
        customerId: null,
        loginCustomerId: null,
      };
    }
  };
</script>
