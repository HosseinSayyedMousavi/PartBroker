from django.urls import path , include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import permissions
app_name="v1"


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http"]
        return schema


schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
      description="API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   generator_class=BothHttpAndHttpsSchemaGenerator, # Here
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("accounts/",include("accounts.urls")),
    path("wallet/", include("wallet.urls")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0) , name='schema-swagger-ui'),
    ]

    
