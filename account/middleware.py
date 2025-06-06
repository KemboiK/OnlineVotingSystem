from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages


class AccountCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user  # Who is the current user ?
        if user.is_authenticated:
            if user.user_type == '1':  # Admin
                if modulename == 'voting.views':
                    error = True
                    if request.path == reverse('fetch_ballot'):
                        pass
                    else:
                        messages.error(
                            request, "You do not have access to this resource")
                        return redirect(reverse('adminDashboard'))
            elif user.user_type == '2':  # Voter
                if modulename == 'administrator.views':
                    messages.error(
                        request, "You do not have access to this resource")
                    return redirect(reverse('voterDashboard'))
            else:  # None of the aforementioned ? Please take the user to login page
                return redirect(reverse('account_login'))
        else:
            allowed_paths = [
                reverse('account_login'),
                reverse('account_register'),
                reverse('forgot_password'),
                reverse('verify_reset_otp'),
                reverse('reset_password'),
                reverse('resend_reset_otp'),
                reverse('help_home'),
                reverse('faq'),
                reverse('contact_support'),
            ]
            # If the path is login or has anything to do with authentication, pass
            if request.path in allowed_paths or modulename == 'django.contrib.auth.views':
                pass
            elif modulename == 'administrator.views' or modulename == 'voting.views':
                # If visitor tries to access administrator or voters functions
                messages.error(
                    request, "You need to be logged in to perform this operation")
                return redirect(reverse('account_login'))
            else:
                return redirect(reverse('account_login'))
