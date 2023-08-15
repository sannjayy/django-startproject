from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'E-mail address'
        }))


ACTION_CHOICES =(
    ("", "-- SELECT A ACTION FROM THIS LIST -- "),
    ("BlacklistedToken", "Remove All Blacklisted Token."),
    ("OutstandingToken", "Remove All Outstanding Token."),
)
class ActionsListForm(forms.Form):
    action = forms.ChoiceField(choices = ACTION_CHOICES, 
        widget=forms.Select(
        attrs={
            'class':'form-control',
            'placeholder':'Select Action'
        }))

    