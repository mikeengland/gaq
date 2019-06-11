<template>
    <v-container fluid>
        <v-layout text-xs-center justify-center>
            <v-flex xs11>
                <v-textarea solo v-model="query" :placeholder="queryPlaceholder"></v-textarea>
            </v-flex>

            <v-flex xs1 text-xs-center>
                <v-layout text-xs-center justify-center>
                    <v-tooltip bottom>
                        <template v-slot:activator="{ on }">
                            <v-btn color="blue" v-on="on" dark small @click="exportCsv(results)">
                                <v-icon>save_alt</v-icon>
                            </v-btn>
                        </template>
                        <span>Export as CSV</span>
                    </v-tooltip>
                </v-layout>

                <v-layout text-xs-center justify-center>
                    <v-tooltip bottom>
                        <template v-slot:activator="{ on }">
                            <v-btn color="orange" v-on="on" dark small @click="clear">
                                <v-icon>delete</v-icon>
                            </v-btn>
                        </template>
                        <span>Clear</span>
                    </v-tooltip>
                </v-layout>

                <v-layout text-xs-center justify-center>
                    <v-tooltip bottom>
                        <template v-slot:activator="{ on }">
                            <v-btn color="pink" v-on="on" dark small @click="execQuery">
                                <v-icon>send</v-icon>
                            </v-btn>
                        </template>
                        <span>Run Query</span>
                    </v-tooltip>
                </v-layout>
            </v-flex>
        </v-layout>

        <v-layout id="results">
            <v-layout justify-center v-show="loading">
                <v-progress-circular
                        :size="50"
                        color="primary"
                        indeterminate
                ></v-progress-circular>
            </v-layout>
            <v-alert
                    :value="true"
                    type="error"
                    v-show="errorMessage">
                {{ errorMessage }}
            </v-alert>

            <v-flex xs12 v-show="results">
                <v-layout justify-center>
                    <v-card id="search-card">
                        <v-card-title>
                            Query Results
                            <v-spacer></v-spacer>
                            <v-text-field
                                    v-model="tableSearch"
                                    append-icon="search"
                                    label="Search"
                                    single-line
                                    hide-details
                            ></v-text-field>
                        </v-card-title>

                        <v-data-table
                                expand
                                v-bind:headers="headers"
                                v-bind:items="rows"
                                class="elevation-1"
                                :search="tableSearch"
                                :pagination.sync="pagination"
                                :rows-per-page-items="rowsPerPageItems"
                        >
                            <template v-slot:items="props">
                                <td v-bind:key="col.id" v-for="col in props.item">{{ col }}</td>
                            </template>
                            <template v-slot:no-results>
                                <v-alert
                                        :value="true"
                                        color="error"
                                        icon="warning"
                                >Your search for "{{ tableSearch }}" found no results.
                                </v-alert>
                            </template>
                        </v-data-table>
                    </v-card>
                </v-layout>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<style scoped>
    #results {
        margin-bottom: 10px;
    }

    #search-card {
        width: 100%;
    }
</style>

<script>
  import {exportJsonAsCsv} from '../utils';

  export default {
    props: ['customerId', 'loginCustomerId'],
    methods: {
      execQuery: function () {
        this.loading = true;
        this.results = null;
        this.errorMessage = null;
        this.$http
          .post(`${process.env.VUE_APP_API_HOST}/api/query`, {
            query: this.query,
            customerId: this.customerId,
            loginCustomerId: this.loginCustomerId,
          })
          .then(response => (this.results = response.data))
          .then(() => this.loading = false)
          .catch(exception => {
            this.loading = false;
            this.errorMessage = exception.response.data.error;
          });
      },
      exportCsv: exportJsonAsCsv,
      clear: function () {
        this.results = null;
        this.query = null;
      },
    },
    computed: {
      headers: function () {
        // We assume all JSON documents returned have the same key structure
        return this.results
          ? Object.keys(this.results[0]).map(value => ({text: value, value}))
          : [];
      },
      rows: function () {
        return this.results || [];
      },
    },
    data() {
      return {
        results: null,
        loading: false,
        errorMessage: null,
        tableSearch: '',
        query: '',
        queryPlaceholder:
          'SELECT ad_group_criterion.keyword.text, metrics.average_cpc ' +
          'FROM keyword_view WHERE segments.date DURING LAST_30_DAYS',
        rowsPerPageItems: [
          {value: 10, text: '10'},
          {value: 25, text: '25'},
          {value: 50, text: '50'},
          {value: 100, text: '100'},
          {value: -1, text: 'All'},
        ],
        pagination: {
          rowsPerPage: 10,
        },
      };
    },
  };
</script>
