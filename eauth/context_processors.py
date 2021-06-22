from .forms import AuthenticationForm, UserCreationForm

def signup(request):
	sform = UserCreationForm()
	return {'sform':sform}

def login(request):
	aform = AuthenticationForm()
	return {'aform':aform}	