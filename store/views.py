from django.http import HttpResponse
from django.shortcuts import render, reverse,redirect
from store.models import *
from django.core.paginator import Paginator
import re
from cart.cart import Cart
from urllib.parse import urlencode

# Create your views here.
def index(request):
    cart = Cart(request)
    ### Thiết bị gia đình
    subcategory_id_tbgd = SubCategory.objects.filter(category = 1).values_list('id') # category = category_id
    list_subcategory_id_tbgd = []
    for subcategory_id in subcategory_id_tbgd:
        list_subcategory_id_tbgd.append(subcategory_id[0])
    # Lấy danh sách sản phẩm
    product_tbgd = Product.objects.filter(subcategory__in = list_subcategory_id_tbgd).order_by('-public_day')

    ### Đồ dùng nhà bếp
    subcategory_id_ddnb = SubCategory.objects.filter(category_id = 2).values_list('id')
    list_subcategory_id_ddnb = []
    for subcategory_id in subcategory_id_ddnb:
        list_subcategory_id_ddnb.append(subcategory_id[0])
    # Lấy danh sách sản phẩm
    product_ddnb = Product.objects.filter(subcategory__in = list_subcategory_id_ddnb).order_by('-public_day')

    return render(request, 'store/index.html', {
        'product_tbgd':product_tbgd[:20],
        'product_ddnb':product_ddnb[:20],
        'products_tbgd_all':product_tbgd,
        'cart':cart,
    })




def contact(request):
    cart = Cart(request)
    if request.POST.get('btnSend'): # sự kiện click nút
        # Gán biến
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Khởi tạo class Contact
        contact = Contact(name = name, email = email, subject = subject, message = message)
        contact.save()
    return render(request, 'store/contact.html',{
        'cart':cart,
    })



def subcategory(request, pk):
    cart = Cart(request)
    # Danh sách subcategory
    subcategories = SubCategory.objects.order_by('name')
    # print(subcategories.values_list('id')[0][0])
    if pk == 0:
        # Đọc tất cả sp
        products = Product.objects.order_by('-public_day')
        title_subcategory = 'Tất cả sản phẩm (' + str(products.count()) + ')'
    else:
        products = Product.objects.filter(subcategory = pk).order_by('-public_day')
        name_subcategory = SubCategory.objects.get(pk = pk)
        title_subcategory = str(name_subcategory) +  '(' + str(products.count()) + ')'

    # Lọc theo range giá
    tu_gia = ''
    den_gia = ''
    tu_khoa = ''
    if request.GET.get('from_price'):
        tu_gia = float(re.sub('\D+', '',request.GET.get('from_price')))
        den_gia = float(re.sub('\D+', '',request.GET.get('to_price')))
        tu_khoa = request.GET.get('product_name')

        # Nếu có chứa từ khóa tìm kiếm (product_name)
        if tu_khoa != '':
            products = Product.objects.filter(name__contains = tu_khoa).order_by('-public_day')
        
        products = [product for product in products if tu_gia <= product.price and product.price <= den_gia]
        if tu_khoa != '':
            title_subcategory = 'Tìm thấy {} sản phẩm có từ khóa là: "{}" nằm trong khoảng giá {} - {}'.format(len(products), tu_khoa,'{:,}'.format(int(tu_gia)), '{:,}'.format(int(den_gia)))
        else:
            title_subcategory = 'Tìm thấy {} sản phẩm  trong khoảng giá {} - {}'.format(len(products),'{:,}'.format(int(tu_gia)), '{:,}'.format(int(den_gia)))
    # Phân trang
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 15)
    products_pager = paginator.page(page)
    
    return render(request, 'store/product-list.html', {
        'products': products_pager,
        'subcategories':subcategories,
        'title_subcategory':title_subcategory,
        'cart':cart,
        'tu_gia': tu_gia,
        'den_gia': den_gia,
        'tu_khoa':tu_khoa,
    })


def search(request):
    
    cart = Cart(request)
    subcategories = SubCategory.objects.all() # Hiển thị kèm danh mục sản phẩm sau khi search ra sản phẩm
    keyword = ''
    title_search = ''
    
    if request.GET.get('product_name'):
        keyword = request.GET.get('product_name')
        # loại bỏ khoảng trắng nếu lỡ như có ai đó vô tình thêm khoảng trắng vào ô tìm kiếm
        keyword = re.sub(r'^\s+','', keyword.rstrip()) # rstring nhằm loại bỏ khoảng trắng ở cuối chuỗi
        objects = Product.objects.all().values()
        id_products = []
        for object in objects:
            object['content'] = re.sub(r'<[^<]+?>', '', object['content'])
            if keyword.lower() in object['name'].lower() or keyword.lower() in object['content'].lower():
                id_products.append(object['id'])
        else:
            products = Product.objects.filter(id__in = id_products).order_by('-public_day')
            title_search = 'CÓ %i SẢN PHẨM PHÙ HỢP VỚI KẾT QUẢ TÌM KIẾM: ' %(len(products)) + keyword
    

    # Phân trang
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 15)
    products_pager = paginator.page(page)

    # Tìm kiếm sản phẩm kèm theo giá
    tu_gia = ''
    den_gia = ''
    if request.GET.get('from_price'):
        tu_gia = float(re.sub('\D+', '',request.GET.get('from_price')))
        den_gia = float(re.sub('\D+', '',request.GET.get('to_price')))
        keyword = request.GET.get('product_name')

        base_url = reverse('store:subcategory', kwargs = {'pk':0})
        query_string = urlencode({
            'from_price':round(tu_gia),
            'to_price':round(den_gia),
            'product_name':keyword,
        })
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)

    return render(request, 'store/product-list.html',{
            'title_search':title_search,
            'subcategories': subcategories,
            'cart':cart,
            'tu_khoa': keyword,
            'products': products_pager,
        })
    
    

def login(request):
    return render(request, 'store/login.html')


def product_detail(request, pk):
    cart = Cart(request)
    subcategories = SubCategory.objects.order_by('name')
    product = Product.objects.get(id = pk)
    
    # id sản phẩm
    id_subcategory = product.subcategory.pk
    relate_product = Product.objects.filter(subcategory = id_subcategory).exclude(id = pk).order_by('-public_day')[:20]
    
    # Tên danh mục
    subcategory_name = product.subcategory
    return render(request, 'store/product-detail.html',{
        'product_detail': product,
        'relate_product': relate_product,
        'subcategories':subcategories,
        'subcategory_name':subcategory_name,
        'id_subcategory':id_subcategory,
        'cart':cart,
    })
    
def wishlist(request):
    return render(request, 'store/wishlist.html')


def thiet_bi_gia_dinh(request):
    cart = Cart(request)
    tbgd = Category.objects.filter(id = 1)[0] # Hiển thị tên trên breadcrum

    subcategories = SubCategory.objects.filter(category = 1)
    list_id_tbgd = SubCategory.objects.filter(category = 1).values_list('id')
    list_id = []
    for id_tbgd in list_id_tbgd:
        list_id.append(id_tbgd[0])

    products = Product.objects.filter(subcategory_id__in = list_id).order_by('-public_day')

    # Lọc theo range giá
    tu_gia = ''
    den_gia = ''
    title_subcategory = ''
    if request.GET.get('from_price'):
        tu_gia = float(re.sub('\D+', '',request.GET.get('from_price')))
        den_gia = float(re.sub('\D+', '',request.GET.get('to_price')))

        products = [product for product in products if tu_gia <= product.price and product.price <= den_gia]
        title_subcategory = 'Tìm thấy {} sản phẩm  trong khoảng giá {} - {}'.format(len(products),'{:,}'.format(int(tu_gia)), '{:,}'.format(int(den_gia)))
    
    # Phân trang
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 15)
    products_pager = paginator.page(page)

    

    return render(request, 'store/product-list.html',{
        'products': products_pager,
        'subcategories': subcategories,
        'tbgd':tbgd,
        'cart':cart,
        'tu_gia':tu_gia,
        'den_gia':den_gia,
        'title_subcategory':title_subcategory,
    })


def dung_cu_nha_bep(request):
    cart = Cart(request)
    dcnb = Category.objects.filter(id = 2)[0]
    subcategories = SubCategory.objects.filter(category = 2)
    list_id_dcnb = SubCategory.objects.filter(category = 2).values_list('id')
    list_id = []
    for id_dcnb in list_id_dcnb:
        list_id.append(id_dcnb[0])

    products = Product.objects.filter(subcategory_id__in = list_id).order_by('-public_day')

     # Lọc theo range giá
    tu_gia = ''
    den_gia = ''
    title_subcategory = ''
    if request.GET.get('from_price'):
        tu_gia = float(re.sub('\D+', '',request.GET.get('from_price')))
        den_gia = float(re.sub('\D+', '',request.GET.get('to_price')))

        products = [product for product in products if tu_gia <= product.price and product.price <= den_gia]
        title_subcategory = 'Tìm thấy {} sản phẩm  trong khoảng giá {} - {}'.format(len(products),'{:,}'.format(int(tu_gia)), '{:,}'.format(int(den_gia)))
    
    # Phân trang
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 15)
    products_pager = paginator.page(page)

    return render(request, 'store/product-list.html',{
        'dcnb':dcnb,
        'products': products_pager,
        'subcategories': subcategories,
        'cart':cart,
        'tu_gia':tu_gia,
        'den_gia':den_gia,
        'title_subcategory':title_subcategory,
    })