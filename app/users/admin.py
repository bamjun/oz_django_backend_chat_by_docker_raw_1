from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 어드민 페이지에서 상세페이지로 볼 정보들
    fieldsets = (
        (
            '유저 정보',
            {
                'fields': ('email', 'password', 'nickname', 'is_business')
            }
        ),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    # 유저를 만들때 보이는 화면
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'nickname',
                    'is_business',
                    'password1',
                    'password2'
                    ),
            }
        ),
    )

    # 표에서 보이는 정보
    list_display = (
        'id',
        'email',
        'nickname',
        'is_business',
        'is_active',
        'is_staff',
        'last_login'
    )
    search_fields = ('email', 'nickname')
    ordering = ('email',)
