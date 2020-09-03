from rest_framework import routers

from categories.views import CategoryView

router = routers.SimpleRouter()
router.register(r'categories', CategoryView)
urlpatterns = router.urls
