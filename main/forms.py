from .models import ClientsList, ContactsCard, ServiseCard, TechInformationCard, Integration
from django.forms import ModelForm, TextInput, Textarea, formset_factory, Select, CheckboxInput
from django import forms


class ClientListForm(ModelForm):
    class Meta:
        model = ClientsList
        fields = ["client_name"]
        widgets = {
            "client_name": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Введите наименование клиента"
            }),
        }

    def clean_client_name(self):
        client_name = self.cleaned_data.get("client_name")
        # Дополнительная валидация и обработка ошибок для поля client_name
        if not client_name:
            raise forms.ValidationError("Поле 'Наименование клиента' обязательно для заполнения.")
        return client_name


class ContactForm(ModelForm):
    class Meta:
        model = ContactsCard
        fields = ['contact_name', 'contact_position', 'contact_email', 'notification_update', 'contact_notes']
        widgets = {
            'contact_name': TextInput(attrs={'class': 'form-control'}),
            'contact_position': TextInput(attrs={'class': 'form-control'}),
            'contact_email': TextInput(attrs={'class': 'form-control'}),
            'notification_update': Select(attrs={'class': 'form-control'}),
            'contact_notes': Textarea(attrs={'class': 'form-control'}),
        }

    def clean_contact_name(self):
        contact_name = self.cleaned_data.get("contact_name")
        if not contact_name:
            raise forms.ValidationError("Поле 'ФИО' обязательно для заполнения.")
        return contact_name

    def clean_contact_position(self):
        contact_position = self.cleaned_data.get("contact_position")
        if not contact_position:
            raise forms.ValidationError("Поле 'Должность' обязательно для заполнения.")
        return contact_position

    def clean_contact_email(self):
        contact_email = self.cleaned_data.get("contact_email")
        if not contact_email:
            raise forms.ValidationError("Поле 'Почта' обязательно для заполнения.")
        return contact_email

    def clean_notification_update(self):
        notification_update = self.cleaned_data.get("notification_update")
        if not notification_update:
            raise forms.ValidationError("Поле 'Отправка рассылки' обязательно для заполнения.")
        return notification_update


ContactFormSet = formset_factory(ContactForm, extra=1)


class ServiseCardForm(ModelForm):
    class Meta:
        model = ServiseCard
        fields = ['service_pack', 'manager', 'loyal']
        widgets = {
            'service_pack': Select(attrs={'class': 'form-control'}),
            'manager': Select(attrs={'class': 'form-control'}),
            'loyal': Select(attrs={'class': 'form-control'}),
        }

    def clean_service_pack(self):
        service_pack = self.cleaned_data.get("service_pack")
        if not service_pack:
            raise forms.ValidationError("Поле 'Сервис план' обязательно для заполнения.")
        return service_pack

    def clean_manager(self):
        manager = self.cleaned_data.get("manager")
        if not manager:
            raise forms.ValidationError("Поле 'Менеджер' обязательно для заполнения.")
        return manager


class TechInformationCardForm(ModelForm):
    class Meta:
        model = TechInformationCard
        exclude = ['client_card']  # Исключаем поле client_card, так как оно будет автоматически привязано при сохранении
        widgets = {
            'server_version': TextInput(attrs={'class': 'form-control'}),
            'update_date': TextInput(attrs={'class': 'form-control'}),
            'api': CheckboxInput(attrs={'class': 'form-check-input'}),
            'ipad': TextInput(attrs={'class': 'form-control'}),
            'android': TextInput(attrs={'class': 'form-control'}),
            'mdm': TextInput(attrs={'class': 'form-control'}),
            'localizable_web': CheckboxInput(attrs={'class': 'form-check-input'}),
            'localizable_ios': CheckboxInput(attrs={'class': 'form-check-input'}),
            'skins_web': CheckboxInput(attrs={'class': 'form-check-input'}),
            'skins_ios': CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ClientForm(forms.Form):
    client_id = forms.IntegerField()


class IntegrationForm(forms.ModelForm):
    class Meta:
        model = Integration
        fields = [
            'elasticsearch',
            'ad',
            'adfs',
            'oauth_2',
            'module_translate',
            'ms_oos',
            'exchange',
            'office_365',
            'sfb',
            'zoom',
            'teams',
            'smtp',
            'cryptopro_dss',
            'cryptopro_csp',
            'smpp',
            'limesurvey',
        ]
        widgets = {
            'elasticsearch': forms.CheckboxInput(attrs={'class': 'js-switch'}),
            'ad': forms.CheckboxInput(attrs={'class': 'js-switch'}),
            'adfs': forms.CheckboxInput(attrs={'class': 'js-switch'}),
            'oauth_2': forms.CheckboxInput(attrs={'class': 'js-switch'}),
            'module_translate': forms.CheckboxInput(attrs={'class': 'js-switch'}),
            'ms_oos': forms.CheckboxInput(attrs={'class': 'js-switch'}),
            'exchange': forms.CheckboxInput(attrs={'class': 'js-switch'}),
            'office_365': forms.CheckboxInput(attrs={'class': 'js-switch'}),
            'sfb': forms.CheckboxInput(attrs={'class': 'js-switch'}),
            'zoom': forms.CheckboxInput(attrs={'class': 'js-switch'}),
            'teams': forms.CheckboxInput(attrs={'class': 'js-switch'}),
            'smtp': forms.CheckboxInput(attrs={'class': 'js-switch'}),
            'cryptopro_dss': forms.CheckboxInput(attrs={'class': 'js-switch'}),
            'cryptopro_csp': forms.CheckboxInput(attrs={'class': 'js-switch'}),
            'smpp': forms.CheckboxInput(attrs={'class': 'js-switch'}),
            'limesurvey': forms.CheckboxInput(attrs={'class': 'js-switch'}),
        }

class AdvancedSearchForm(forms.Form):
    serverVersionCheckbox = forms.BooleanField(label='Версия сервера', required=False)
    serverVersionInput = forms.CharField(label='Введите версию сервера', max_length=255, required=False)


class URLInputForm(forms.Form):
    service_url = forms.URLField(label='URL адрес стенда', required=True)

class ServerInputForm(forms.Form):
    service_url = forms.CharField(label='Адрес сервера, где развёрнут стенд', required=True)