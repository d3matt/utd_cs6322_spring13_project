from django import forms

class TopicSearchForm(forms.Form):
    block = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        """sets the class to 'span12' so it matches the rest of the page to begin with"""
        super(TopicSearchForm, self).__init__(*args, **kwargs)
        self.fields['block'].widget.attrs['class'] = 'span12'
    
    def clean_block(self):
        txt = self.cleaned_data['block']
        topics = 0
        for line in self.cleaned_data['block'].splitlines():
            line=line.strip()
            if len(line) == 0:
                continue
            topics += 1
        if topics < 3:
            raise forms.ValidationError("Probably a good idea to have at least three topics...")
        return txt
