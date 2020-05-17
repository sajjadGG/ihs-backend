from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter , URLRouter
import chat.routing 
from chat.mixins import TokenAuthMiddleware

# application = ProtocolTypeRouter({
#     # Empty for now (http->django views is added by default)
#     'websocket' : AuthMiddleware(
#         URLRouter(
#             chat.routing.websocket_urlpatterns
#         )
#     ),
# })

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket' : TokenAuthMiddleware(
    AuthMiddlewareStack(
       URLRouter(
            chat.routing.websocket_urlpatterns
        )
    )
    )
    
})