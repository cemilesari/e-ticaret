from rest_framework.generics import CreateAPIView,ListAPIView,DestroyAPIView, UpdateAPIView, RetrieveAPIView
from main.api.serializers.reseller.comments import CommentCreateSerializer, CommentListSerializer, CommentDeleteUpdateSerializer
from main.order.models import Comment
from main.api.permissions import IsOwner
from main.api.paginations import CommentPagination

class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    #otomatik user atama 
    def perform_create(self, serializer):
        serializer.save(user= self.request.user)


class CommentListAPIView(ListAPIView):
    #queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    pagination_class = CommentPagination
    #sadece parenti olanları getirmek için
    def get_queryset(self):
        queryset = Comment.objects.filter(parent = None)
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(post = query)
        return queryset

class CommentDeleteAPIView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteUpdateSerializer
    lookup_field = 'pk'
    permission_classes = [IsOwner]


class CommentUpdateAPIView(UpdateAPIView, RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteUpdateSerializer
    lookup_field = 'pk'
    permission_classes = [IsOwner]