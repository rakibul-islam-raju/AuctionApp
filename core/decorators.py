from django.contrib.auth.decorators import user_passes_test


def staff_required(login_url=None):
    return user_passes_test(lambda user: user.is_staff, login_url=login_url)
