from rest_framework.generics import RetrieveUpdateApiView
from rest_framework.permissions import IsAuthenticated

class ProfileView(RetrieveUpdateApiView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


    def get_object(self):
        queryset = self.queryset()
        obj = get_object_or_404(queryset, id = self.request.user.id)
        return obj

    def perform_update(self, serializer):
        serializer.save(user = self.request.user)