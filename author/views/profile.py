from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from author.models import Profile


@method_decorator(
    login_required(redirect_field_name='next', login_url='author:login'),
    name='dispatch'
)
class ProfileView(TemplateView):
    template_name = 'author/pages/profile.html'

    def get(self, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        profile_id = context.get('id')
        profile = get_object_or_404(
            Profile.objects.filter(
                pk=profile_id
            ).select_related('author'), pk=profile_id
        )
        return self.render_to_response({
            **context,
            'profile': profile,
        })
