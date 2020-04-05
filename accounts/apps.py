from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):    # need to add this
    	import accounts.signals    # need to add this
