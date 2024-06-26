from django import forms

Time_choices = [
    ('1 hour', '1 Hour'),
    ('4 hour', '4 Hour'),
    ('12 hour', '12 Hour'),
    ('1 day', '1 Day'),
    ('3 days', '3 Days'),
]

class TimeForm(forms.Form):
    time_choice = forms.ChoiceField(choices=Time_choices)