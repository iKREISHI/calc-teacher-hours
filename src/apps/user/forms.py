from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
import re


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    middle_name = forms.CharField(max_length=150, required=False, help_text="Необязательно")

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'middle_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.middle_name = self.cleaned_data.get('middle_name', '')

        # Always generate username from first, middle, and last names
        user.username = self.generate_username(user.first_name, user.last_name, user.middle_name)

        if commit:
            user.save()
        return user

    def generate_username(self, first_name, last_name, middle_name):
        """
        Generate username from first, last, and middle names using Latin characters only
        Example: Иванов Иван Иванович -> ivanov-i-i
        """
        # Transliterate Cyrillic to Latin
        first_name_translit = self.transliterate_cyrillic(first_name)
        last_name_translit = self.transliterate_cyrillic(last_name)
        middle_name_translit = self.transliterate_cyrillic(middle_name) if middle_name else ''

        # Take first letter of first name
        first_initial = first_name_translit[0].lower() if first_name_translit else ''

        # Take first letter of middle name if provided
        middle_initial = middle_name_translit[0].lower() if middle_name_translit else ''

        # Use full last name
        last_name_clean = re.sub(r'[^a-zA-Z\-]', '', last_name_translit.lower())

        # Create username in format: lastname-firstinitial-middleinitial
        if middle_initial:
            username = f"{last_name_clean}-{first_initial}-{middle_initial}"
        else:
            username = f"{last_name_clean}-{first_initial}"

        # Ensure uniqueness
        original_username = username
        counter = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1

        return username

    def transliterate_cyrillic(self, text):
        """
        Transliterate Cyrillic characters to Latin characters
        """
        if not text:
            return ""

        # Define transliteration mapping
        cyrillic_to_latin = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
            'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
            'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
            'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu',
            'я': 'ya', 'і': 'i', 'ї': 'yi', 'є': 'ye'
        }

        result = ""
        for char in text.lower():
            if char in cyrillic_to_latin:
                result += cyrillic_to_latin[char]
            elif char.isalpha():
                result += char
            # Skip non-alphabetic characters except hyphens

        return result

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide the username field since it's auto-generated
        if 'username' in self.fields:
            self.fields['username'].widget = forms.HiddenInput()
            self.fields['username'].required = False