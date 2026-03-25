from oauth2_provider.views.mixins import OAuthLibMixin
from app.views.base import BaseViewSet

from app.views.base import BaseViewSet
from .models import Post, PostMedia, Comment, Like
from .serializer import PostSerializer, PostMediaSerializer, CommentSerializer, LikeSerializer
from rest_framework.exceptions import NotAuthenticated, PermissionDenied


class PostViewSet(BaseViewSet, OAuthLibMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"]],
        "create": [["admin"]],
        "update": [["admin"]],
        "destroy": [["admin"]],
    }

    # def get_queryset(self):
    #     user = self.request.user
    #     if not user or not user.is_authenticated:
    #         raise NotAuthenticated("You must be signin in to access this resource!")
    #     if not hasattr(user, "role") or user.role is None:
    #         raise PermissionDenied("You do not have a role assigned!")
    #     if user.role.name == "admin":
    #         return Post.objects.all()
    #     return Post.objects.filter(user_id=user.id)


class PostMediaViewSet(BaseViewSet, OAuthLibMixin):
    queryset = PostMedia.objects.all()
    serializer_class = PostMediaSerializer
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"]],
        "create": [["admin"]],
        "update": [["admin"]],
        "destroy": [["admin"]],
    }

class CommentViewSet(BaseViewSet, OAuthLibMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"]],
        "create": [["admin"]],
        "update": [["admin"]],
        "destroy": [["admin"]],
    }
    
class LikeViewSet(BaseViewSet, OAuthLibMixin):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"]],
        "create": [["admin"]],
        "update": [["admin"]],
        "destroy": [["admin"]],
    }
