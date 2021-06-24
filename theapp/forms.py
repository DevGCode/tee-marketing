from django.contrib.auth.forms import UserChangeForm

from django.forms import ModelForm
from .models import *
# from django.contrib.admin import forms
from django import forms


class EditProfileForm(UserChangeForm):
    # email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password')



class EditScriptForm(ModelForm):
    class Meta:
        model= Script
        fields = ('title', 'body')
        widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control',}),
        'body': forms.TextInput(attrs={'class': 'form-control',}),
    }

class EditVoicemailForm(ModelForm):
    class Meta:
        model= VoicemailScript
        fields = ('title', 'body')
        widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control',}),
        'body': forms.TextInput(attrs={'class': 'form-control',}),
    }






# class CreateLeadForm(forms.ModelForm):
#     class Meta:
#         model = Lead
#         fields = '__all__'
#         widgets = {
#         'contacted': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contacted'}),
#         'responded': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Responded'}),
#         'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
#         'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
#         'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
#         'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Designation'}),
#         'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
#         'notes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Notes'}),
#         'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Main Phone'}),
#         'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
#         'website_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Website URL'}),
#     }



# class UpdateLeadForm(forms.ModelForm):
#     class Meta:
#         model = Lead
#         fields = '__all__'
#         widgets={
#             'contacted': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contacted'}),
#             'responded': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Responded'}),
#             'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
#             'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
#             'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Designation'}),
#             'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
#             'notes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Notes'}),
#             'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Main Phone'}),
#             'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
#             'website_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Website URL'}),
#                 }



# ### CAMPAIGN ###
# class CreateCampaignForm(forms.ModelForm):
#     class Meta:
#         model = Campaign
#         fields = '__all__'
#         widgets = {
#         # 'user': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User'}),
#         'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
#         'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
#     }


# class UpdateCampaignForm(forms.ModelForm):
#     class Meta:
#         model = Campaign
#         fields = '__all__'
#         widgets={
#             # 'user': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User'}),
#         'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
#         'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
#                 }


# ### NOTES ###
# class CreateNoteForm(forms.ModelForm):
#     class Meta:
#         model = Note
#         fields = '__all__'
#         widgets = {
#         'body': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write your note here..'}),
#     }


# class UpdateNoteForm(forms.ModelForm):
#     class Meta:
#         model = Note
#         fields = '__all__'
#         widgets={
#             'body': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write your note here..'}),
#                 }


# ### EMAIL TEMPLATE ###
# class CreateEmailTemplateForm(forms.ModelForm):
#     class Meta:
#         model = EmailTemplate
#         fields = '__all__'
#         widgets = {
#         'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Subject'}),
#         'body': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Body'}),
#         'cc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CC'}),
#         'bcc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'BCC'}),
#     }


# class UpdateEmailTemplateForm(forms.ModelForm):
#     class Meta:
#         model = EmailTemplate
#         fields = '__all__'
#         widgets={
#             'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Subject'}),
#             'body': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Body'}),
#             'cc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CC'}),
#             'bcc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'BCC'}),
#                 }



# ### EMAIL FOOTER ###
# class CreateEmailFooterForm(forms.ModelForm):
#     class Meta:
#         model = EmailFooter
#         fields = '__all__'
#     #     widgets = {
#     #     'body': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write your note here..'}),
#     # }


# class UpdateEmailFooterForm(forms.ModelForm):
#     class Meta:
#         model = EmailFooter
#         fields = '__all__'
#         # widgets={
#         #     'body': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write your note here..'}),
#         #         }
