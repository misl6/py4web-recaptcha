## Usage

```python
..
from py4web_recaptcha import ReCaptchaV3Field
..

@action("captcha_form", method=["GET", "POST"])
@action.uses("captcha_form.html", session)
def example_captcha_form():
    def low_score_callback(score):
        session.min_captcha_score = score
        print("low_score_callback_called")

    def get_form(readonly=False):
        print("generating_new_form")
        extra_fields = []

        if hasattr(session, "min_captcha_score"):
            min_score = session.min_captcha_score
            extra_fields = [Field("email", requires=IS_EMAIL())]
        else:
            min_score = 1.0

        return Form(
            [
                Field("name", requires=IS_NOT_EMPTY()),
                *extra_fields,
                ReCaptchaV3Field(
                    name="captcha",
                    action="form1_submit",
                    min_score=min_score,
                    site_key="YOUR_SITE_KEY",
                    secret_key="YOUR_SECRET_KEY",
                    on_captcha_score_low=low_score_callback,
                ),
            ],
            formstyle=FormStyleBulma,
            readonly=readonly
        )

    form = get_form()
    message = ""
    print("accepting/erroring form")
    if form.accepted:
        message = "form accepted with: %s " % (form.vars)
    elif form.errors:
        message = "form has errors: %s " % (form.errors)
        if "captcha" in form.errors:
            form = get_form(readonly=True)
            form.readonly = False
            form.errors['captcha'] = 'Bad score! We need some more info about you ...'
    return dict(form=form, message=message)

```