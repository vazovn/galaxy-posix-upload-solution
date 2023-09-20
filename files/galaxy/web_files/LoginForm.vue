<template>
    <div class="container">
        <div class="row justify-content-md-center">
            <template v-if="!confirmURL">
                <div class="col col-lg-6">
                    <b-alert :show="messageShow" :variant="messageVariant" v-html="messageText" />
                        <span v-html="messageText" />
                                   <b-form id="login" @submit.prevent="submitLogin()">
                        <b-card no-body header="Welcome to the Galaxy-FOX : the Galaxy portal to the Fox cluster at UiO">
                            <b-card-body>
                                <div>
                                    <!-- standard internal galaxy login -->
                                     <b-form-group label="How to log in">
                                        <b-form-text>
                                                1. Apply for access to an educloud project : click on the educloud research icon below
                                                </p>
                                                <a href="https://research.educloud.no/login"><img src="https://research.educloud.no/_next/static/images/logo-text-ee0d4c59633474b318e00573994c7e60.svg" width="100"  height="20" class="center" ></a>
                                                </p>
                                                and select project <font color="red">ec73</font> at the next screen
                                                </p>
											    </b-form-text>
											    <b-form-text>
                                                2. Install Google, Microsoft or another authenticator on your smartphone and scan the QR-code for 2 factor authentication (2FA). See <a href="https://www.uio.no/english/services/it/research/platforms/edu-research/help/two-factor-authentication.html">instructions here</a>
                                                </p>
												</b-form-text>
												<b-form-text>
                                                3. When ready with previous steps, click on the Fox icon below to  log in
                                                </p>
											</b-form-text>
                                    </b-form-group>
                                </div>
                                <div v-if="enableOidc">
                                    <!-- OIDC login-->
                                    <external-login :login_page="true" :exclude_idps="[connectExternalProvider]" />
                                </div>
                            </b-card-body>
                                <div class="row justify-content-md-center">
                                        <b-form-text>
											</hr>
                                            If you have any questions, please write to <a href="mailto:hpc-drift@usit.uio.no">hpc-drift@usit.uio.no</a>
                                            </p>
                                        </b-form-text>
								</div>
                        </b-card>
                    </b-form>
                </div>
            </template>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import Vue from "vue";
import BootstrapVue from "bootstrap-vue";
import { withPrefix } from "utils/redirect";
import NewUserConfirmation from "./NewUserConfirmation";
import ExternalLogin from "components/User/ExternalIdentities/ExternalLogin";
import _l from "utils/localization";

Vue.use(BootstrapVue);

export default {
    components: {
        ExternalLogin,
        NewUserConfirmation,
    },
    props: {
        allowUserCreation: {
            type: Boolean,
            default: false,
        },
        enableOidc: {
            type: Boolean,
            default: false,
        },
        redirect: {
            type: String,
            default: null,
        },
        registrationWarningMessage: {
            type: String,
            default: null,
        },
        sessionCsrfToken: {
            type: String,
            required: true,
        },
        showWelcomeWithLogin: {
            type: Boolean,
            default: false,
        },
        termsUrl: {
            type: String,
            default: null,
        },
        welcomeUrl: {
            type: String,
            default: null,
        },
    },
    data() {
        const urlParams = new URLSearchParams(window.location.search);
        return {
            login: null,
            password: null,
            url: null,
            messageText: null,
            messageVariant: null,
            headerWelcome: _l("Welcome to Galaxy, please log in"),
            labelNameAddress: _l("Public Name or Email Address"),
            labelPassword: _l("Password"),
            confirmURL: urlParams.has("confirm") && urlParams.get("confirm") == "true",
            connectExternalEmail: urlParams.get("connect_external_email"),
            connectExternalProvider: urlParams.get("connect_external_provider"),
            connectExternalLabel: urlParams.get("connect_external_label"),
        };
    },
    computed: {
        welcomeUrlWithRoot() {
            return withPrefix(this.welcomeUrl);
        },
    },
    methods: {
        toggleLogin() {
            this.$emit("toggle-login");
        },
        submitLogin() {
            let redirect = this.redirect;
            if (this.connectExternalEmail) {
                this.login = this.connectExternalEmail;
            }
            if (localStorage.getItem("redirect_url")) {
                redirect = localStorage.getItem("redirect_url");
            }
            axios
                .post(withPrefix("/user/login"), {
                    login: this.login,
                    password: this.password,
                    redirect: redirect,
                    session_csrf_token: this.sessionCsrfToken,
                })
                .then(({ data }) => {
                    if (data.message && data.status) {
                        alert(data.message);
                    }
                    if (data.expired_user) {
                        window.location = withPrefix(`/root/login?expired_user=${data.expired_user}`);
                    } else if (this.connectExternalProvider) {
                        window.location = withPrefix("/user/external_ids?connect_external=true");
                    } else if (data.redirect) {
                        window.location = encodeURI(data.redirect);
                    } else {
                        window.location = withPrefix("/");
                    }
                })
                .catch((error) => {
                    this.messageVariant = "danger";
                    const message = error.response && error.response.data && error.response.data.err_msg;
                    if (this.connectExternalProvider && message && message.toLowerCase().includes("invalid")) {
                        this.messageText =
                            message + " Try logging in to the existing account through an external provider below.";
                    } else {
                        this.messageText = message || "Login failed for an unknown reason.";
                    }
                });
        },
        setRedirect(url) {
            localStorage.setItem("redirect_url", url);
        },
        resetLogin() {
            axios
                .post(withPrefix("/user/reset_password"), { email: this.login })
                .then((response) => {
                    this.messageVariant = "info";
                    this.messageText = response.data.message;
                })
                .catch((error) => {
                    this.messageVariant = "danger";
                    const message = error.response.data && error.response.data.err_msg;
                    this.messageText = message || "Password reset failed for an unknown reason.";
                });
        },
        returnToLogin() {
            window.location = withPrefix("/login/start");
        },
    },
};
</script>
<style scoped>
.card-body {
    overflow: visible;
}
</style>
