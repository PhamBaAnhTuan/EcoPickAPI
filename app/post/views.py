from oauth2_provider.views.mixins import OAuthLibMixin
from app.views.base import BaseViewSet
from .models import Post, PostMedia, Comment, Like
from .serializer import (
    PostSerializer,
    PostMediaSerializer,
    CommentSerializer,
    LikeSerializer,
)
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from drf_spectacular.utils import extend_schema, extend_schema_view
from app.swagger import common_list_params


@extend_schema_view(
    list=extend_schema(
        summary="Danh sách bài viết",
        description="Lấy tất cả bài viết cộng đồng. Hỗ trợ textSearch và phân trang.",
        parameters=common_list_params,
        tags=["Post"],
    ),
    retrieve=extend_schema(
        summary="Chi tiết bài viết",
        description="Lấy chi tiết 1 bài viết bao gồm thông tin author, location, hashtags, tagged_users, like/comment/share count.",
        tags=["Post"],
    ),
    create=extend_schema(
        summary="Tạo bài viết mới",
        description="Tạo bài viết mới.\n\n**Body fields:** author_id (UUID FK), title, content, latitude, longitude, location, address, hashtags (comma-separated), tagged_users (JSON array UUID), related_report_id (FK), related_event_id (FK), is_hidden",
        tags=["Post"],
    ),
    update=extend_schema(summary="Cập nhật bài viết", tags=["Post"]),
    partial_update=extend_schema(summary="Cập nhật một phần bài viết", tags=["Post"]),
    destroy=extend_schema(summary="Xóa bài viết", tags=["Post"]),
)
class PostViewSet(BaseViewSet, OAuthLibMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "create": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "update": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "destroy": [["admin"], ["organizer"], ["moderator"], ["user"]],
    }

    def get_queryset(self):
        return Post.objects.all()

    def perform_update(self, serializer):
        user = self.request.user
        instance = self.get_object()
        
        # Kiểm tra quyền: admin hoặc chính tác giả bài viết
        is_admin = user.role and user.role.name == "admin"
        is_owner = instance.author_id == user.id
        
        if not (is_admin or is_owner):
            raise PermissionDenied("Bạn không có quyền chỉnh sửa bài viết này.")
            
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        
        # Kiểm tra quyền: admin hoặc chính tác giả bài viết
        is_admin = user.role and user.role.name == "admin"
        is_owner = instance.author_id == user.id
        
        if not (is_admin or is_owner):
            raise PermissionDenied("Bạn không có quyền xóa bài viết này.")
            
        instance.delete()


@extend_schema_view(
    list=extend_schema(
        summary="Danh sách media bài viết",
        description="Lấy tất cả media (hình ảnh, video) đính kèm bài viết.",
        parameters=common_list_params,
        tags=["Post Media"],
    ),
    retrieve=extend_schema(summary="Chi tiết media", tags=["Post Media"]),
    create=extend_schema(
        summary="Thêm media mới",
        description="Upload media cho bài viết.\n\n**Body fields:** post_id (UUID FK), url, thumbnail_url, type (image/video), height, width, order_index",
        tags=["Post Media"],
    ),
    update=extend_schema(summary="Cập nhật media", tags=["Post Media"]),
    partial_update=extend_schema(
        summary="Cập nhật một phần media", tags=["Post Media"]
    ),
    destroy=extend_schema(summary="Xóa media", tags=["Post Media"]),
)
class PostMediaViewSet(BaseViewSet, OAuthLibMixin):
    queryset = PostMedia.objects.all()
    serializer_class = PostMediaSerializer
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "create": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "update": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "destroy": [["admin"], ["organizer"], ["moderator"], ["user"]],
    }
    # def get_queryset(self):
    #     user = self.request.user
    #     if user.role and user.role.name == "admin":
    #         return PostMedia.objects.all()
    #     return PostMedia.objects.filter(author_id=user.id)


@extend_schema_view(
    list=extend_schema(
        summary="Danh sách bình luận",
        description="Lấy tất cả bình luận.",
        parameters=common_list_params,
        tags=["Comment"],
    ),
    retrieve=extend_schema(summary="Chi tiết bình luận", tags=["Comment"]),
    create=extend_schema(
        summary="Tạo bình luận mới",
        description="Thêm bình luận vào bài viết.\n\n**Body fields:** user_id (UUID FK), post_id (UUID FK), event_id (UUID FK, optional), repost_id (UUID FK, optional), content, photo_url",
        tags=["Comment"],
    ),
    update=extend_schema(summary="Cập nhật bình luận", tags=["Comment"]),
    partial_update=extend_schema(
        summary="Cập nhật một phần bình luận", tags=["Comment"]
    ),
    destroy=extend_schema(summary="Xóa bình luận", tags=["Comment"]),
)
class CommentViewSet(BaseViewSet, OAuthLibMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "create": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "update": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "destroy": [["admin"], ["organizer"], ["moderator"], ["user"]],
    }

    def get_queryset(self):
        user = self.request.user
        if user.role and user.role.name == "admin":
            return Comment.objects.all()
        return Comment.objects.filter(user_id=user.id)
    
    def perform_update(self, serializer):
        instance = self.get_object()
        user = self.request.user
        if instance.user_id != user.id and not (user.role and user.role.name == "admin"):
            raise PermissionDenied("You do not have permission to edit this comment.")
        serializer.save()


@extend_schema_view(
    list=extend_schema(
        summary="Danh sách lượt thích",
        description="Lấy tất cả lượt thích.",
        parameters=common_list_params,
        tags=["Like"],
    ),
    retrieve=extend_schema(summary="Chi tiết lượt thích", tags=["Like"]),
    create=extend_schema(
        summary="Thích bài viết",
        description="Thêm lượt thích.\n\n**Body fields:** user_id (UUID FK), post_id (UUID FK), repost_id (UUID FK, optional)\n\n**Unique constraint:** user_id + post_id + repost_id",
        tags=["Like"],
    ),
    update=extend_schema(summary="Cập nhật lượt thích", tags=["Like"]),
    partial_update=extend_schema(summary="Cập nhật một phần", tags=["Like"]),
    destroy=extend_schema(summary="Bỏ thích", tags=["Like"]),
)
class LikeViewSet(BaseViewSet, OAuthLibMixin):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "create": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "update": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "destroy": [["admin"], ["organizer"], ["moderator"], ["user"]],
    }

    def get_queryset(self):
        user = self.request.user
        if user.role and user.role.name == "admin":
            return Like.objects.all()
        return Like.objects.filter(user_id=user.id)
