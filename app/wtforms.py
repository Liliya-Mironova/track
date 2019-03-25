from wtforms_alchemy import ModelForm, DataRequired, Length
from wtforms import TextField
from .models import User
import requests

# class UserForm(ModelForm):
#     class Meta:
#         model = User

    #requests.post('http://127.0.0.1:5000/', data={"jsonrpc": "2.0", "method": "auth", "params": ["lmironov", "11"], "id": "3"})

class UserForm(ModelForm):
    login = TextField(validators=[DataRequired(), Length(min=4, max=100)])
    password = TextField(validators=[DataRequired(), Length(min=2, max=255)])