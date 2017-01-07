from django import forms


class MyForm(forms.Form):
    text = forms.CharField(max_length=100, required=False, label='テキスト')


class VoteForm(forms.Form):
    choice = forms.ModelChoiceField(
        queryset=None,
        label='選択',
        widget=forms.RadioSelect(),
        empty_label=None,
        error_messages={
            'required': "You didn't select a choice.",
            'invalid_choice': "invalid choice.",
        }
    )

    def __init__(self, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choice'].queryset = question.choice_set.all()
