<template>
    <v-container fluid>
        <v-layout text-xs-center row justify-center>
            <v-flex xs5>
                <v-text-field
                        v-model="loginCustomerId"
                        label="Please enter the parent MCC ID of the account you would like to query"
                        box
                        required
                ></v-text-field>
            </v-flex>
        </v-layout>
        <v-layout text-xs-center row justify-center>
            <v-flex xs5>
                <v-text-field
                        v-model="customerId"
                        @keyup.enter="onClickButton"
                        label="Please enter the ID of the account you would like to query"
                        box
                        required
                ></v-text-field>
            </v-flex>
        </v-layout>
        <v-layout text-xs-center row justify-center>
            <v-flex xs4>
                <v-btn color="blue" dark @click="onClickButton">
                    <v-icon>send</v-icon>
                </v-btn>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
  export default {
    methods: {
      onClickButton: function () {
        this.$emit('clicked', this.loginCustomerId, this.customerId);
      },
    },
    data() {
      return {
        customerId: null,
        loginCustomerId: null,
      };
    },
  };
</script>
