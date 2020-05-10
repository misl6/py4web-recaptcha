import requests

from yatl.helpers import DIV, XML

VERIFY_SERVER = "https://www.google.com/recaptcha/api/siteverify"

class ReCaptchaV3Field(object):
    def __init__(
        self, name, action, min_score, site_key, secret_key, on_captcha_score_low=None
    ):
        self.name = name
        self.action = action
        self.min_score = min_score
        self.site_key = site_key
        self.secret_key = secret_key
        self.on_captcha_score_low = on_captcha_score_low
        self.type = "captcha"
        self.readable = True
        self.writable = True
        self.label = ""
        self.comment = None

    def validate(self, value, record_id):
        if not value:
            return False, "Missing reCaptcha response"
        res = requests.post(
            VERIFY_SERVER, data=dict(secret=self.secret_key, response=value)
        )
        if res.status_code == 200:
            challenge_response = res.json()
            if challenge_response["success"] == True:
                if self.min_score <= challenge_response["score"]:
                    return True, None
                else:
                    if self.on_captcha_score_low:
                        self.on_captcha_score_low(challenge_response["score"])
                    return False, "Captcha score too low"
        return False, "Captcha not valid"

    def widget(self, table, value):
        return DIV(self.xml())

    def xml(self):
        return XML(
            "<input type='hidden', id='recaptchav3_{name}' name='{name}'>\
                    <script src='https://www.google.com/recaptcha/api.js?render={site_key}'></script>\
                    <script>\
                        grecaptcha.ready(function() {{\
                            grecaptcha.execute('{site_key}', {{action: '{action}'}}).then(function(token) {{\
                                document.getElementById('recaptchav3_{name}').value = token;\
                            }});\
                        }});\
                    </script>".format(
                **dict(name=self.name, action=self.action, site_key=self.site_key)
            )
        )
