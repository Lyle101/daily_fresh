from django.conf.urls import url
from order.views import OrderPlaceView

urlpatterns = [
    url(r'^place$', OrderPlaceView.as_view(), name='place'), # 提交订单页面显示
]
