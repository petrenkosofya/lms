from .base import *

DEBUG = False

# Override database to use SQLite for tests (no need for PostgreSQL permissions)
# Use file-based SQLite instead of in-memory to allow proper migrations
import tempfile
import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(tempfile.gettempdir(), "lms_test_db.sqlite3"),
    }
}
MODELTRANSLATION_DEBUG = False
THUMBNAIL_DEBUG = False
for template in TEMPLATES:
    template["OPTIONS"]["debug"] = DEBUG
    if "auto_reload" in template["OPTIONS"]:
        template["OPTIONS"]["auto_reload"] = DEBUG

TEST_RUNNER = "django.test.runner.DiscoverRunner"
TEST_DISCOVER_TOP_LEVEL = str(SHARED_APPS_DIR)
TEST_DISCOVER_ROOT = str(SHARED_APPS_DIR)
TEST_DISCOVER_PATTERN = "test_*"

# django-coverage settings

COVERAGE_REPORT_HTML_OUTPUT_DIR = str(SHARED_APPS_DIR / "coverage")
COVERAGE_USE_STDOUT = True
COVERAGE_MODULE_EXCLUDES = [
    "tests$",
    "settings$",
    "urls$",
    "locale$",
    "common.views.test",
    "__init__",
    "django",
    "migrations",
    "^sorl",
    "__pycache__",
]
COVERAGE_PATH_EXCLUDES = [r".svn", r"fixtures", r"node_modules"]

TEST_DOMAIN = "compscicenter.ru"
TEST_DOMAIN_ID = 1
ANOTHER_DOMAIN = "compsciclub.ru"
ANOTHER_DOMAIN_ID = 2
SITE_ID = TEST_DOMAIN_ID
LMS_DOMAIN = TEST_DOMAIN
ALLOWED_HOSTS = [f".{TEST_DOMAIN}", f".{ANOTHER_DOMAIN}"]

# This makes tests almost 2x faster; we don't need strong security and DEBUG
# during tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

USE_CLOUD_STORAGE = False
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
PRIVATE_FILE_STORAGE = DEFAULT_FILE_STORAGE
MEDIA_ROOT = "/tmp/django_test_media/"
MEDIA_URL = "/media/"
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
EMAIL_SEND_COOLDOWN = 0

# Disable migrations for tests - create schema directly from models
# This avoids issues with outdated migrations referencing non-existent fields
# Setting to None disables migrations and creates schema from models
MIGRATION_MODULES = {
    "core": None,
    "universities": None,
    "files": None,
    "auth": None,
    "users": None,
    "courses": None,
    "study_programs": None,
    "learning": None,
    "notifications": None,
    "info_blocks": None,
    "alumni": None,
    "api": None,
    "faq": None,
    "staff": None,
}

LANGUAGE_CODE = "en"

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

THUMBNAIL_KVSTORE = "sorl.thumbnail.kvstores.cached_db_kvstore.KVStore"

SILENCED_SYSTEM_CHECKS = ["captcha.recaptcha_test_key_error"]

for queue_config in RQ_QUEUES.values():
    queue_config["ASYNC"] = False

for bundle_conf in WEBPACK_LOADER.values():
    bundle_conf["LOADER_CLASS"] = "core.webpack_loader.TestingWebpackLoader"
