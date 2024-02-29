
from functools import wraps
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


def group_required(group_names):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                # Si l'utilisateur n'est pas connecté, redirigez-le vers la page de connexion
                return redirect('login')

            user_groups = Group.objects.filter(user=request.user, name__in=group_names)
            if not user_groups.exists():
                # Si l'utilisateur n'appartient à aucun des groupes spécifiés, renvoyez une erreur 403
                return render(request, 'pbent/page_404.html')

            # L'utilisateur appartient à au moins l'un des groupes, exécutez la vue normalement
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


