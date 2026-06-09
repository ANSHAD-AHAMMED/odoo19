import {patch} from "@web/core/utils/patch";

const UserPresenceEvents = ["mousemove", "mousedown", "touchmove", "click", "scroll", "keypress"];
const SurveyForm = odoo.loader.modules.get("@survey/interactions/survey_form").SurveyForm;


patch(SurveyForm.prototype, {
    start() {
        super.start();

        this.idleTimer = document.querySelector(".idle_timer");
        this.idleLimitSeconds = Number(this.idleTimer.dataset.idle || 5);

        this.remainingSeconds = this.idleLimitSeconds;

        this.idleThreshold = 5000;
        this.isIdle = false;
        this.idleCountdownInterval = null;
        this.idleTimeout = null;

        const userActivity = () => {
            if (this.isIdle) {
                this.pauseIdleTimer();
                this.isIdle = false;
            }

            clearTimeout(this.idleTimeout);

            this.idleTimeout = setTimeout(() => {
                this.isIdle = true;
                this.startIdleTimer();
            }, this.idleThreshold);
        }

        UserPresenceEvents.forEach((event) => {
            window.addEventListener(event, userActivity);
        });
        userActivity();
    },

    startIdleTimer() {
        const submitBtn = document.querySelector("button[type='submit']");
        const nextBtn = document.querySelector("#next_page");

        this.idleCountdownInterval = setInterval(() => {
            this.remainingSeconds--;
            this.idleTimer.textContent = this.remainingSeconds

            if (this.remainingSeconds <= 0) {
                clearInterval(this.idleCountdownInterval);
                this.idleCountdownInterval = null;

                if (submitBtn) {
                    submitBtn.click();

                } else {
                    if (nextBtn) {
                        nextBtn.click();
                    }
                }
                this.remainingSeconds = this.idleLimitSeconds
            }
        }, 1000);
    },

    pauseIdleTimer() {
        if (this.idleCountdownInterval) {
            clearInterval(this.idleCountdownInterval);
            this.idleCountdownInterval = null;
        }
    },

});
