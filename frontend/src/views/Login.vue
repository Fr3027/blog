<template>
    <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
            <v-col cols="12" sm="8" md="4">
                <v-card class="elevation-12">
                    <v-toolbar color="primary" dark flat>
                        <v-toolbar-title align="center">登录</v-toolbar-title>
                        <v-spacer></v-spacer>
                    </v-toolbar>
                    <v-card-text>
                        <v-form>
                            <v-text-field label="用户名" name="username" prepend-icon="mdi-account" type="text" v-model="username"></v-text-field>
                            <v-text-field id="password" label="密码" name="password" prepend-icon="mdi-lock" type="password" v-model="password"></v-text-field>
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" @click="login">登录</v-btn>
                    </v-card-actions>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
import axios from "axios";
import EventBus from "../event-bus";
export default {
    props: {
        source: String
    },
    data: () => ({
        drawer: null,
        username: "",
        password: "",
        remember: true
    }),
    methods: {
        /*
        执行登录操作
        操作字段: username,password,remember
        触发事件: close login dialog
        @return void
        */
        login() {
            axios
                .post(
                    "http://localhost:5000/login", {
                        username: this.username,
                        password: this.password,
                        remember: this.remember
                    }, {
                        withCredentials: true
                    }
                )
                .then(response => {
                    if (response.data.status == "success") {
                        EventBus.$emit("close_dialog", "login");
                    }
                });
        }
    }
};
</script>