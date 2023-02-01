from django.shortcuts import render, redirect
from admin_estore.forms import FormUser, FormUserProfileInfo
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def user_auth(request):
    # ============ SIGN-UP ============
    frm_user = FormUser()
    frm_profile = FormUserProfileInfo()

    # Thực hiện lưu thông tin
    result_register = ''
    if request.POST.get('btnRegister'):
        frm_user = FormUser(request.POST)
        frm_profile = FormUserProfileInfo(request.POST, request.FILES)
        if frm_user.is_valid() and frm_profile.is_valid():
            if frm_user.cleaned_data['password'] == frm_user.cleaned_data['confirm_password']:
                # GHi vào CSDL
                # 1. User
                user = frm_user.save()
                user.set_password(user.password)
                user.save()

                # 2. UserProfileInfo
                profile = frm_profile.save(commit=False)
                profile.user = user # Quan hệ 1-1
                profile.save()

                result_register = '''
                <div class="alert alert-success" role="alert">
                    Đăng ký tài khoản admin thành công.
                </div>
                '''
            else:
                result_register = '''
                <div class="alert alert-danger" role="alert">
                    Mật khẩu và xác nhận mật khẩu không khớp. Vui lòng nhập lại
                </div>
                '''
        else:
            result_register = '''
                <div class="alert alert-danger" role="alert">
                    Dữ liệu không hợp lệ. Vui lòng kiểm tra lại
                </div>
                '''
    # ============ LOGIN ============
    result_login = ''
    if request.POST.get("btnLogin"):
        # Gán biến
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Xác thực
        user = authenticate(request, username = username, password = password)

        # Xét điều kiện
        if user is not None:
            login(request, user)
            return redirect('admin_estore:user_auth')
        else:
            result_login = '''
        <div class="alert alert-success" role="alert">
                    Đăng nhập không thành công. Vui lòng kiểm tra lại thông tin đăng nhập.
        </div>
    '''
    return render(request, 'admin_estore/user_auth.html',{
        'frm_user':frm_user,
        'frm_profile': frm_profile,
        'result_register': result_register,
        'result_login': result_login
    })

def logout_user_auth(request):
    logout(request)
    return redirect('admin_estore:user_auth')