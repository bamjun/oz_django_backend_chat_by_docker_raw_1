from django.contrib import admin
from .models import ChatRoom, ChatRoomConnector, Message


@admin.register(ChatRoom)
class ChatAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            '채팅방',
            {
                'fields': ('roomname',)
            },
        ),
    )

    # 표에서 보이는 정보
    list_display = (
        'id','roomname'
    )
    search_fields = ('roomname',)
    ordering = ('created_at',)

@admin.register(ChatRoomConnector)
class ConnectorAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            '채팅방',
            {
                'fields': ('chatroom','user')
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'user',
                    'chatroom',
                    ),
            }
        ),
    )
    # 표에서 보이는 정보
    list_display = (
        'chatroom','user'
    )

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            '채팅기록',
            {
                'fields': ('sender','message','chatroom')
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'sender',
                    'message',
                    'chatroom',
                    ),
            }
        ),
    )
    # 표에서 보이는 정보
    list_display = (
        'chatroom','sender','message'
    )