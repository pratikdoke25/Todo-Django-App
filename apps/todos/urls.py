from rest_framework.routers import SimpleRouter
from .views import CategoryViewSet, TodoViewSet

router = SimpleRouter()
router.register('todos',TodoViewSet)
router.register("categories", CategoryViewSet)


urlpatterns = router.urls