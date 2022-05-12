from allauth.account.utils import send_email_confirmation
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.api.models import UserAPIKey

from .forms import CustomUserChangeForm, UploadAvatarForm
from .helpers import require_email_confirmation, user_has_confirmed_email_address
from .models import CustomUser


@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user_before_update = CustomUser.objects.get(pk=user.pk)
            need_to_confirm_email = (
                user_before_update.email != user.email
                and require_email_confirmation()
                and not user_has_confirmed_email_address(user, user.email)
            )
            if need_to_confirm_email:
                # don't change it but instead send a confirmation email
                # email will be changed by signal when confirmed
                new_email = user.email
                send_email_confirmation(request, user, signup=False, email=new_email)
                user.email = user_before_update.email
                # recreate the form to avoid populating the previous email in the returned page
                form = CustomUserChangeForm(instance=user)
            user.save()
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'account/profile.html', {
        'form': form,
        'active_tab': 'profile',
        'api_keys': request.user.api_keys.filter(revoked=False),
    })


@login_required
@require_POST
def upload_profile_image(request):
    user = request.user
    form = UploadAvatarForm(request.POST, request.FILES)
    if form.is_valid():
        user.avatar = request.FILES['avatar']
        user.save()
    return HttpResponse('Success!')


@login_required
def create_api_key(request):
    api_key, key = UserAPIKey.objects.create_key(
        name=f"{request.user.get_display_name()} API Key",
        user=request.user
    )
    messages.success(
        request,
        'API Key created. Your key is: {key}. Save this somewhere safe - you will only see it once!'.format(
            key=key,
        )
    )
    return HttpResponseRedirect(reverse('users:user_profile'))


@login_required
@require_POST
def revoke_api_key(request):
    key_id = request.POST.get('key_id')
    api_key = request.user.api_keys.get(id=key_id)
    api_key.revoked = True
    api_key.save()
    messages.success(
        request,
        'API Key {key} has been revoked. It can no longer be used to access the site.'.format(
            key=api_key.prefix,
        )
    )
    return HttpResponseRedirect(reverse('users:user_profile'))
