# Create your views here.
from django.shortcuts import render,redirect
from customer.forms import FormSignUp
from customer.models import Customer
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from cart.cart import Cart
from cart.models import Order, OrderItem
from store.models import Product
from EStore.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives

import json
# Create your views here.
def customer_login(request):
    # Kiểm tra trạng thái của session
    if 'session_KhachHang' in request.session:
        return redirect('store:index')

    # Đọc file json
    with open('vietnam.json', 'r',encoding="utf8") as f:
        du_lieu = json.load(f)
    
    # Tỉnh/TP
    list_provinces = []
    str_districts = []
    str_wards = []
    list_districts_2 = []
    for province in du_lieu:
        if province['name'] == "Hà Nội":
            list_provinces.append('Thủ đô ' + province['name'])
        elif province['name'] == 'Hồ Chí Minh' or province['name'] == 'Hải Phòng'\
             or province['name'] == 'Đà Nẵng' or province['name'] == 'Cần Thơ'  :
            list_provinces.append('Thành phố ' + province['name'])
        else:
            list_provinces.append('Tỉnh ' + province['name'])
        
        # Quận/Huyện
        list_districts = []
        for district in province['districts']:
            d = district['prefix'] + ' ' + district['name']
            list_districts.append(d)
            list_districts_2.append(d)
            #Phường/Xã
            list_wards = []
            for ward in district['wards']:
                w = ward['prefix'] + ' ' + ward['name']
                list_wards.append(w)
            str_wards.append('|'.join(list_wards))
        else:
            str_districts.append('|'.join(list_districts)) 
        


    # Đăng ký
    result_singup = ''
    form_signup =  FormSignUp()
    if request.POST.get('btnDangKy'): # Khi nút đc click
        form_signup = FormSignUp(request.POST, Customer)
        if form_signup.is_valid() and form_signup.cleaned_data['password'] == form_signup.cleaned_data['confirm_password']:
            hasher = PBKDF2PasswordHasher()
            request.POST._mutable = True
            post = form_signup.save(commit=False)
            post.last_name = form_signup.cleaned_data['last_name']
            post.first_name = form_signup.cleaned_data['first_name']
            post.email = form_signup.cleaned_data['email']
            post.tel = form_signup.cleaned_data['tel']
            post.password = hasher.encode(form_signup.cleaned_data['password'], 'b' ) # ở tham số thứ 2 trong PBKDF chỉ cần tối thiểu 1 bit, nên ghi cái gì cũng đc
            post.address = form_signup.cleaned_data['address'] + ', ' + form_signup.cleaned_data['ward']\
            + ', ' + form_signup.cleaned_data['district'] + ', ' + form_signup.cleaned_data['province']
            post.save()

            result_singup = '''
                <div class="alert alert-success" role="alert">
                    Đăng ký thành công
                </div>
            '''
        else:
            result_singup = '''
            <div class="alert alert-danger" role="alert">
                Đăng ký không thành công. Vui lòng kiểm tra lại thông tin nhập.
            </div>
        '''

    # Đăng nhập
    if request.POST.get('btnDangNhap'):
        # Gán biến
        email = request.POST.get('email')
        mat_khau = request.POST.get('mat_khau')
        hasher = PBKDF2PasswordHasher()
        encoded = hasher.encode(mat_khau, 'b')

        khach_hang = Customer.objects.filter(email = email, password = encoded)
        if khach_hang.count() > 0:
            request.session['session_KhachHang'] = khach_hang.values()[0] # khach_hang.values()[0] là một query set chứa dictionary
            return redirect('store:index')

    return render(request, 'store/login.html', {
        'form_signup': form_signup,
        'result_singup':  result_singup,
        'provinces': tuple(list_provinces),
        'str_districts':tuple(str_districts),
        'str_wards':tuple(str_wards),
        'list_districts':list_districts_2,
    })

# Đăng xuất
def customer_logout(request):
    if 'session_KhachHang' in request.session: # nếu session_KhachHang có tồn tại trong hệ thống session
        del request.session['session_KhachHang']
    return redirect('customer:customer_login')

def my_account(request):
    cart = Cart(request)
    if 'session_KhachHang' not in request.session:
        return redirect('customer:customer_login')

    # Lất thông tin tỉnh/tp, quận/huyện, phường/xã
    # Đọc file json
    with open('/home/quochuybh0404/estore_project/vietnam.json', 'r',encoding="utf8") as f:
        du_lieu = json.load(f)
    # Tỉnh/TP
    list_provinces = []
    str_districts = []
    str_wards = []
    list_districts_2 = []
    for province in du_lieu:
        if province['name'] == 'Hồ Chí Minh' or province['name'] == "Hà Nội"\
             or province['name'] == 'Hải Phòng' or province['name'] == 'Đà Nẵng'\
                 or province['name'] == 'Cần Thơ'  :
            list_provinces.append('Thành phố ' + province['name'])
        else:
            list_provinces.append('Tỉnh ' + province['name'])
        
        # Quận/Huyện
        list_districts = []
        for district in province['districts']:
            d = district['prefix'] + ' ' + district['name']
            list_districts.append(d)
            list_districts_2.append(d)
            #Phường/Xã
            list_wards = []
            for ward in district['wards']:
                w = ward['prefix'] + ' ' + ward['name']
                list_wards.append(w)
            str_wards.append('|'.join(list_wards))
        else:
            str_districts.append('|'.join(list_districts)) 

    # Cập nhật thông tin khách hàng
    result_update_info = ''' '''
    form_signup =  FormSignUp()
    if request.POST.get('btnCapNhat'):
        form_signup = FormSignUp(request.POST)
        
        # Gán biến
        ho = request.POST.get('ho')
        ten = request.POST.get('ten')
        sdt = request.POST.get('sdt')
        # email = request.POST.get('email') 
        if form_signup.is_valid():
            dia_chi = request.POST.get('dia_chi') + ', ' + form_signup.cleaned_data['ward']\
                + ', ' + form_signup.cleaned_data['district'] + ', ' + form_signup.cleaned_data['province']
        else:
            dia_chi = request.POST.get('dia_chi') + ', ' + form_signup.cleaned_data['ward']\
                + ', ' + form_signup.cleaned_data['district'] + ', ' + form_signup.cleaned_data['province']
        # Cập nhật vào CSDL
        khach_hang = Customer.objects.get(id = request.session['session_KhachHang']['id'])
        khach_hang.last_name = ten
        khach_hang.first_name = ho
        khach_hang.tel = sdt
        khach_hang.address = dia_chi  
        khach_hang.save()
        
        # Cập nhật vào session
        request.session['session_KhachHang']['last_name'] = ten
        request.session['session_KhachHang']['first_name'] = ho
        request.session['session_KhachHang']['tel'] = sdt
        request.session['session_KhachHang']['address'] = dia_chi

        # Thông báo kết quả
        result_update_info = ''' 
            <div class="alert alert-success" role="alert">
                    Cập nhật thông tin cá nhân thành công
            </div>
        '''

    # Đổi mật khẩu
    result_changepassword = ''' '''
    if request.POST.get('btnDoiMatKhau'):
        # Gán biến
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')
        hasher = PBKDF2PasswordHasher()
        encoded_old = hasher.encode(old_password, 'b')

        if encoded_old == request.session['session_KhachHang']['password'] and new_password == confirm_new_password:
            encoded_new = hasher.encode(new_password, 'b')
            khach_hang = Customer.objects.get(id = request.session['session_KhachHang']['id'])
            khach_hang.password = encoded_new
            khach_hang.save()
            result_changepassword = ''' 
            <div class="alert alert-success" role="alert">
                    Đổi mật khẩu thành công
            </div>
        '''
        else:
            result_changepassword = ''' 
            <div class="alert alert-danger" role="alert">
                    Đổi mật khẩu không thành công
            </div>
        '''
            
    # Đơn hàng
    orders = Order.objects.filter(customer = request.session['session_KhachHang']['id'])
    dict_orders = {}
    for order in orders:
        order_items = list(OrderItem.objects.filter(order = order.pk).values())
        for order_item in order_items:
            product = Product.objects.get(pk = order_item['product_id'])
            order_item['product_name'] = product.name
            order_item['product_image'] = product.image
            order_item['total_price'] = order.total
        dict_order_items = {
            order.pk: order_items
        }
        dict_orders.update(dict_order_items)

    return render(request, 'store/my-account.html',
        {
            'result_update_info':result_update_info,
            'orders':orders,
            'dict_orders':dict_orders,
            'cart':cart,
            'form_signup': form_signup,
            'provinces': tuple(list_provinces),
            'str_districts':tuple(str_districts),
            'str_wards':tuple(str_wards),
            'list_districts':list_districts_2,
            'result_changepassword':result_changepassword,
        }
    )


# Quên mật khẩu
def reset_password(request):
    if request.POST.get('btnResetPassword'):
        # Đổi mật khẩu
        email = request.POST.get('email')
        
        try:
            khach_hang = Customer.objects.get(email = email)
            
            new_password = 1
            hasher = PBKDF2PasswordHasher()
            encoded = hasher.encode(new_password, 'b')
            khach_hang.password = encoded
            khach_hang.save()

            # Gửi mail
            # Có định dạng html
            message = '''<b>Bạn đã đổi mật khẩu thành công.<br>
            Mật khẩu mới của bạn là:</b>''' + str(new_password)
            subject = 'Đặt lại mật khẩu'
            msg = EmailMultiAlternatives(subject, message, EMAIL_HOST_USER, [email])
            msg.attach_alternative(message, 'text/html')
            msg.send()

            result = 'Đặt lại mật khẩu thành công'
            notification = 'Chúng tôi đã gửi cho bạn mật khẩu mới. Vui lòng kiểm tra email.'
            return render(request, 'customer/password-reset-done.html', {
                'result':result,
                'notification':notification,
                })
        except Customer.DoesNotExist:
            result = 'Đặt lại mật khẩu không thành công.'
            notification = '''Tài khoản không tồn tại. Vui lòng nhập đúng email mà bạn đã đăng ký'''
            
            return render(request, 'customer/password-reset-done.html', {
                'result':result,
                'notification':notification,
                })
        
    return render(request, 'store/reset-password.html')