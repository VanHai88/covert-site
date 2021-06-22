from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, ButtonHolder, Submit, HTML

from .models import StreamPost

class CreatePostForm(forms.ModelForm):

    class Meta:
        model = StreamPost
        fields = ['group','title','content']

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.fields['group'].empty_label = "Post to (optional):"
        self.fields['group'].label = ""
        self.fields['content'].widget.attrs['placeholder'] = "Share what's going on"

        if self.initial == {}:
            type = None
            btn_text = 'Submit'
        else:
            type = "hidden" #hides group field on edit
            btn_text = 'Save changes'

        self.helper.layout = Layout(
            Field('group', wrapper_class="field", type=type),
            'title',
            'content',
            ButtonHolder(
                Submit('submit', btn_text, css_class="button is-primary is-inline"),
                HTML("<span class='loading'></span>"),
                css_class="level level-left"
            ),
            
        )
        self.helper[1:3].wrap(Field, wrapper_class="field", css_class="input")