from django.shortcuts import render, redirect
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.views.generic import View

from user.models import Address
from goods.models import GoodsSKU
from django_redis import get_redis_connection
from utils.mixin import LoginRequiredMixin


# Create your views here.
# /order/place
class OrderPlaceView(LoginRequiredMixin, View):
    '''提交订单页面显示'''

    def post(self, request):
        '''提交订单页面显示'''
        # 获取登录的用户
        user = request.user
        # 获取参数sku_ids
        sku_ids = request.POST.getlist('sku_ids')  # [1,26]

        # 校验参数
        if not sku_ids:
            # 跳转到购物车页面
            return redirect(reverse('cart:show'))

        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id

        skus = []
        # 保存商品的总件数和总价格
        total_count = 0
        total_price = 0
        # 遍历sku_ids获取用户要购买的商品的信息
        for sku_id in sku_ids:
            # 根据商品的id获取商品的信息
            sku = GoodsSKU.objects.get(id=sku_id)
            # 获取用户所要购买的商品的数量
            count = conn.hget(cart_key, sku_id)
            # 计算商品的小计
            amount = sku.price * int(count)
            # 动态给sku增加属性count,保存购买商品的数量
            sku.count = int(count)
            # 动态给sku增加属性amount,保存购买商品的小计
            sku.amount = amount
            # 追加
            skus.append(sku)
            # 累加计算商品的总件数和总价格
            total_count += int(count)
            total_price += amount

        # 运费:实际开发的时候，属于一个子系统
        transit_price = 10  # 写死

        # 实付款
        total_pay = total_price + transit_price

        # 获取用户的收件地址
        addrs = Address.objects.filter(user=user)

        # 组织上下文
        sku_ids = ','.join(sku_ids)  # [1,25]->1,25
        context = {'skus': skus,
                   'total_count': total_count,
                   'total_price': total_price,
                   'transit_price': transit_price,
                   'total_pay': total_pay,
                   'addrs': addrs,
                   'sku_ids': sku_ids}
        # 使用模板
        return render(request, 'place_order.html', context)
