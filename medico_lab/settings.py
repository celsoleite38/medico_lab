from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent



# SEGURANÇA: segredos vêm de variáveis de ambiente.
# Gere uma nova chave com: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-somente-para-desenvolvimento-troque-em-producao')

# DEBUG só deve ser ligado em desenvolvimento (padrão: desligado em produção)
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('1', 'true', 'sim')

ALLOWED_HOSTS = ['medicos.innosoft.com.br', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'evolucoes.apps.EvolucoesConfig',
    'autenticacao',
    'prontuario',
    'agenda',
    'notificacoes',
    'exames',
    'receituario',
    'atestados',
    'sugestoes',
    'import_export',
    'paginas_vendas'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'medico_lab.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'autenticacao.context_processors.perfil_profissional',
                'notificacoes.context_processors.avisos_nao_lidos',
            ],
        },
    },
]

WSGI_APPLICATION = 'medico_lab.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True

DATE_FORMAT = 'd/m/Y'  # Formato de data: dia/mês/ano
DATETIME_FORMAT = 'd/m/Y'  # Formato de data e hora: dia/mês/ano hora:minuto:segundo


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'templates/static'),)
STATIC_ROOT = os.path.join('static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#mensagen de erro
from django.contrib.messages import constants
MESSAGE_TAGS = {
    constants.DEBUG: 'alert-primary',
    constants.ERROR: 'alert-danger',
    constants.SUCCESS: 'alert-success',
    constants.INFO: 'alert-info',
    constants.WARNING: 'alert-warning',
}

#email
# Credenciais vêm de variáveis de ambiente — NUNCA coloque senha no código.
# Em desenvolvimento, comente o EMAIL_BACKEND SMTP e use o backend de console:
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

if os.environ.get('EMAIL_HOST_USER'):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'Medicos-Innosoft <noreply@medicosinnosoft.com.br>'
EMAIL_FAIL_SILENTLY = False

# Integrações opcionais (deixe vazias se não usar)
WHATSAPP_TOKEN = os.environ.get('WHATSAPP_TOKEN', '')
WHATSAPP_BUSINESS_ID = os.environ.get('WHATSAPP_BUSINESS_ID', '')
MERCADO_PAGO_ACCESS_TOKEN = os.environ.get('MERCADO_PAGO_ACCESS_TOKEN', '')

LOGIN_URL = '/auth/logar/'
LOGIN_REDIRECT_URL = '/prontuario/dashboard/'
LOGOUT_REDIRECT_URL = '/auth/logar/'
