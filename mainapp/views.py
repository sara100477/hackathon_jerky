from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from upload.forms import UploadFileForm
from upload.models import UploadFileModel
from .models import category,brand_for_category
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt


class main:
    @csrf_exempt
    def home( request, flag=99999 , id_num=99999,brand="all",sale="all",sorting=99999):
        if flag != 2 and sorting == 99999:
            sorting = 99999
        if brand not in ('all','스타벅스','투썸플레이스'):
            brand = 'all'
        if sale not in ('경매','급매','all'):
            sale = 'all'


        print('#################################')
        print( flag,id_num,brand,sale,sorting)
        ufl = UploadFileModel.objects.all()
        brand_for_categorys = brand_for_category.objects

        details = None
        if flag==1: # datail
            if id_num == 99999:
                print("html에서 값을 제대로 지정하지 않음")
                return render(request,'home.html')
            details = get_object_or_404(UploadFileModel, pk=id_num) 
            if brand != 'all':
                ufl = ufl.filter(pbrand=brand)
            if sale != 'all':
                ufl = ufl.filter(saletype=sale)
            
            if sorting in (1,2,3):
                id_num = sorting

                if id_num == 2:
                    ufl = ufl.order_by('lowerlimit')
                elif id_num == 1:
                    ufl = ufl.order_by('pub_date')
                elif id_num == 3:
                    ufl = ufl.order_by('-lowerlimit')
                else:
                    ufl = ufl


        elif flag ==2:  # sort
            if brand != 'all':
                ufl = ufl.filter(pbrand=brand)
            if sale != 'all':
                ufl = ufl.filter(saletype=sale)

            sort = id_num
            sorting = id_num
            if id_num == 2:
                ufl = ufl.order_by('lowerlimit')
            elif id_num == 1:
                ufl = ufl.order_by('pub_date')
            elif id_num == 3:
                ufl = ufl.order_by('-lowerlimit')
            else:
                ufl = ufl

        else:    # 브랜드/상품 카테고리 선택
            if request.method == 'POST':
                select_brand = request.POST['brand']
                select_sale = request.POST['saletype']
    
                if select_brand != 'all':
                    print(request.POST['brand'])
                    ufl = ufl.filter(pbrand=select_brand)
    
                if select_sale != 'all':
                    print(request.POST['saletype'])
                    ufl = ufl.filter(saletype=select_sale)

                checked_brand = select_brand
                checked_sale = select_sale

                paginator = Paginator(ufl, 10)
                page = request.GET.get('page')
                posts = paginator.get_page(page)


                return render(request, 'home.html',{ 'posts':posts,'brand_for_categorys':brand_for_categorys,'details':details,'checked_brand':checked_brand,'checked_sale':checked_sale,'sorting':sorting})
        
        if brand == 'all' and sale == 'all':         
            checked_brand = None
            checked_sale = None
        else:
            checked_brand = brand
            checked_sale = sale 

        paginator = Paginator(ufl, 10)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
  
        return render(request, 'home.html',{ 'posts':posts,'brand_for_categorys':brand_for_categorys,'details':details,'checked_brand':checked_brand,'checked_sale':checked_sale,'sorting':sorting})





def about(request):
    return render(request,'about.html')

@csrf_exempt
@login_required
def auction(request,product_id):

    details = UploadFileModel.objects.get( pk=product_id)

    ufl = UploadFileModel.objects
    brand_for_categorys = brand_for_category.objects
    sort = request.GET.get('sort','')

    if sort == 'lowprice':
        ufl = UploadFileModel.objects.all().order_by('lowerlimit')
    elif sort == 'date':
        ufl = UploadFileModel.objects.all().order_by('pub_date')
    elif sort == 'highprice':
        ufl = UploadFileModel.objects.all().order_by('-lowerlimit')
    else:
        ufl =  ufl = UploadFileModel.objects.all()

    product_list = ufl
    paginator = Paginator(product_list, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)


    bidprice = request.POST.get('bidprice', '오류')
    if int(bidprice) < details.lowerlimit and int(bidprice)<= details.bidprice:
        print('하한가, 현재입찰가보다 낮은 가격으로 입찰할 수 없음  이라는 메시지 띄워야함')
        return render(request,'home.html',{'ufl':ufl, 'posts':posts,'brand_for_categorys':brand_for_categorys,'details':details})
    else:
        details.bidprice = bidprice
        details.biduser = request.user.username
        details.save()
    return redirect('home')



@login_required
def mypage(request):
    ufl = UploadFileModel.objects.filter(user_id = request.user.username)
    return render(request, 'mypage.html',{'ufl':ufl})

@login_required
def buy(request, product_id):
    productbuy = get_object_or_404(UploadFileModel ,pk=product_id)
    return render(request,'buy.html',{'productbuy':productbuy})
    
@login_required
def pay(request, product_id):
    productpay = get_object_or_404(UploadFileModel ,pk=product_id)
    return render(request,'pay.html',{'productpay':productpay})

def delete(request, product_id):
    productdelete = get_object_or_404(UploadFileModel ,pk=product_id)
    productdelete.delete()
    return redirect('home')