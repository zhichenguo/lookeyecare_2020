from allauth.account.forms import AddEmailForm


class MyCustomAddEmailForm(AddEmailForm):

    def save(self):
        # Ensure you call the parent class's save.
        # .save() returns an allauth.account.models.EmailAddress object.
        email_address_obj = super(MyCustomAddEmailForm, self).save()

        # Add your own processing here.

        # You must return the original result.
        return email_address_obj
