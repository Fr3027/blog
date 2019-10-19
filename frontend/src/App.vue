<template>
    <v-app id="inspire">
        <v-navigation-drawer v-model="drawer" app color="primary darken-1" src="./assets/background.jpg">
            <v-list dense class="mt-10">
                <div class="text-center">
                    <v-avatar color="primary" size="100">
                        <v-img src="https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1571387713498&di=d9e44d89dd1f066934d8ba2d84d1d4f8&imgtype=0&src=http%3A%2F%2Fa.hiphotos.baidu.com%2Fimage%2Fpic%2Fitem%2F838ba61ea8d3fd1fc9c7b6853a4e251f94ca5f46.jpg"></v-img>
                    </v-avatar>
                    <div class="title white--text mt-4">Destiny的博客</div>
                    <div class="subtitle-1 white--text lighten-5">Nothing to say......</div>
                </div>
                <v-container>
                    <v-row>
                        <v-col cols="12">
                            <div class="title text-center mt-10">Tags</div>
                            <v-chip-group column active-class="primary--text">
                                <v-chip v-for="tag in tags" :key="tag">{{ tag }}</v-chip>
                            </v-chip-group>
                        </v-col>
                    </v-row>
                </v-container>
            </v-list>
        </v-navigation-drawer>
        <v-app-bar app color="primary" src="./assets/background.jpg">
            <!-- <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon> -->
            <v-btn icon @click.stop="drawer = !drawer">
                <v-icon>mdi-chevron-left</v-icon>
            </v-btn>
            <v-toolbar-title>POSTS</v-toolbar-title>
            <div class="flex-grow-1"></div>
            <v-btn v-if="!isLogin" text @click.stop="loginDialog = true">登录</v-btn>
            <v-btn v-if="!isLogin" text @click.stop="registerDialog = true">注册</v-btn>
            <v-btn icon @click="logout" v-if="isLogin">
                <v-icon>mdi-power</v-icon>
            </v-btn>
        </v-app-bar>
        <v-content>
            <!-- Data Table -->
            <v-container fluid>
                <v-row>
                    <v-col cols="6">
                        <v-data-table :headers="headers" :items="desserts" :items-per-page="10" class="elevation-1" style="width:205%;height:100%">
                            <template v-slot:item.action="{ item }">
                                <v-btn color="success" icon>
                                    <v-icon>mdi-eye</v-icon>
                                </v-btn>
                                <v-btn color="warning" class="ml-3" icon :disabled="!isLogin">
                                    <v-icon>mdi-pencil</v-icon>
                                </v-btn>
                                <v-btn color="red" class="ml-3" icon :disabled="!isLogin">
                                    <v-icon>mdi-delete</v-icon>
                                </v-btn>
                            </template>
                        </v-data-table>
                        <v-btn class="mx-2" fab dark large color="cyan" fixed right bottom @click.stop="postDialog = true" v-if="isLogin">
                            <v-icon dark>mdi-pencil</v-icon>
                        </v-btn>
                    </v-col>
                </v-row>
                <!-- 发布文章Dialog -->
                <v-dialog v-model="postDialog">
                    <v-card>
                        <v-text-field class="title" placeholder="请在此输入文章标题" align="right" style="width:30%;margin-left: 34%" v-model="new_post.title"></v-text-field>
                        <v-text-field class="sub-title1" placeholder="tag" style="width:30%;margin-left: 34%" v-model="new_post.tag"></v-text-field>
                        <vue-editor v-model="new_post.content"></vue-editor>
                        <v-btn color="success" class="mt-5 mb-5" style="margin-left: 45%" width="100px" @click="save">发表</v-btn>
                    </v-card>
                </v-dialog>
                <!-- 登录Dialog -->
                <v-dialog v-model="loginDialog">
                    <LoginForm source="123"></LoginForm>
                </v-dialog>
                <!-- 注册Dialog -->
                <v-dialog v-model="registerDialog">
                    <RegisterForm source="123"></RegisterForm>
                </v-dialog>
            </v-container>
        </v-content>
    </v-app>
</template>
<script>
import axios from "axios";
import LoginForm from "./views/Login.vue";
import RegisterForm from "./views/Register.vue";
import EventBus from "./event-bus";
import { VueEditor } from "vue2-editor";
export default {
    name: "App",
    components: {
        LoginForm,
        RegisterForm,
        VueEditor
    },
    props: {
        source: String
    },
    data: () => ({
        /*控制新建文章,登录,注册的对话框*/
        postDialog: false,
        loginDialog: false,
        registerDialog: false,
        /*控制侧边栏的显示*/
        drawer: null,
        /*文章分类标签*/
        tags: [
            "Flask",
            "Improvement",
            "Vacation",
            "Food",
            "Spring",
            "Tomcat",
            "Angular",
            "React",
            "Vue"
        ],
        /*记录新建文章,编辑文章的相应字段*/
        new_post: {
            tag: "",
            title: "",
            content: "<h1>Some initial content</h1>",
        },
        edit_post: {
            tag: "",
            title: "",
            content: "",
        },
        /*DataTable*/
        headers: [{
                text: "标题",
                align: "left",
                sortable: false,
                value: "name"
            },
            { text: "时间", value: "time", sortable: false },
            { text: "Action", value: "action", sortable: false }
        ],
        desserts: [],
        /*控制登录状态
        更新触发事件: 重新加载组件后,成功执行登录,注销操作后
        */
        isLogin: false
        //
    }),
    methods: {

        /**
         将文章内容采用Base64编码方式存到数据库中
         操作字段: new_post
         @return void
        */
        save() {
            let Base64 = {
                encode(str) {
                    return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g,
                        function toSolidBytes(match, p1) {
                            return String.fromCharCode('0x' + p1)
                        }))
                },
                decode(str) {
                    return decodeURIComponent(atob(str).split('').map(function(c) {
                        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
                    }).join(''))
                }
            };
            axios.post("http://localhost:5000/create_post", {
                tag: this.new_post.tag,
                title: this.new_post.title,
                body: Base64.encode(this.new_post.content)
            }, {
                withCredentials: true
            })
        },

        /*
        执行服务器端下线操作,更新本地登录状态
        操作字段: isLogin
        @return void
        */
        logout() {
            axios.get("http://localhost:5000/logout", {
                withCredentials: true
            }).then(() => {
                this.isLogin = false
            })
        },
        /*
        删除相应文章
        @param {number} pid 文章的id
        @return void
        */
        deletePost() {

        }
    },
    /*
    通过EventBus监听其他组件的事件
    目前可监听close_dialog事件,关闭登录或注册对话框.
    @return void
    */
    mounted() {
        EventBus.$on("close_dialog", payLoad => {
            if (payLoad == "login") {
                this.loginDialog = false;
                this.isLogin = true;
            } else if (payLoad == "register") {
                this.registerDialog = false;
            }
        });
    },
    /**
    从服务器获得当前用户登录状态, 以及文章数据
    操作字段: isLogin
    @return void
    */
    created() {
        axios
            .get("http://localhost:5000/login", {
                withCredentials: true
            })
            .then(response => {
                if (response.data.status == "success")
                    this.isLogin = true;
            });
    }
};
</script>
<style scoped>
</style>