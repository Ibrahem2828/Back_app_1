from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import User
from login.serializers import LoginSerializer,RegisterSerializer
from rest_framework.permissions import AllowAny

class LoginAPIView(APIView):
    # السماح لجميع المستخدمين بالوصول دون مصادقة مسبقة
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # التحقق من وجود المستخدم بناءً على البريد الإلكتروني
            user = User.get_user_by_email(email)
            if not user:
                return Response(
                    {"error": "User does not exist"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # التحقق من كلمة المرور
            if User.check_password(user['password'], password):
                return Response(
                    {
                        "message": "Login successful",
                        "user": {
                            "user_id": str(user['_id']),  # تحويل user_id إلى نص
                            "username": user['username'],
                            "email": user['email'],
                            "is_admin": user.get('is_admin', False),
                        },
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid password"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        # إعادة الأخطاء في حال فشل التحقق من البيانات
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class RegisterAPIView(APIView):
#     permission_classes = [AllowAny]  # السماح لجميع المستخدمين بالوصول
#     def post(self, request):
#         # طباعة البيانات المستلمة من العميل
#         print(f"Request Data: {request.data}")

#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user_data = serializer.save()  # حفظ البيانات
#             return Response(
#                 {
#                     "message": "User created successfully.",
#                     "user": {
#                         "user_id": str(user_data['_id']),  # إضافة user_id وتحويله إلى نص
#                         "username": user_data['username'],
#                         "email": user_data['email'],
#                         "is_admin": user_data.get('is_admin', False),  # التعامل مع is_admin بشكل صحيح
#                     },
#                 },
#                 status=status.HTTP_201_CREATED,
#             )
#         # في حالة حدوث خطأ في التحقق من البيانات
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


# رابط الصورة الافتراضية
DEFAULT_PROFILE_PICTURE = "../img/DEFAULT_PROFILE_PICTURE.png"

# API لإنشاء حساب
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]  # السماح لجميع المستخدمين بالوصول

    def post(self, request):
        # استخراج البيانات من الطلب
        data = request.data

        # التحقق من الحقول الإلزامية
        required_fields = ["username", "email", "password"]
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return Response(
                {"error": f"Missing required fields: {', '.join(missing_fields)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # إنشاء مستخدم جديد
            user_data = User.create_user({
                "username": data["username"],
                "email": data["email"],
                "password": data["password"],
                "profile_picture": data.get("profile_picture", DEFAULT_PROFILE_PICTURE),
            })

            # إعادة استجابة ناجحة
            return Response(
                {
                    "message": "User created successfully.",
                    "user": {
                        "user_id": str(user_data['_id']),
                        "username": user_data['username'],
                        "email": user_data['email'],
                        "profile_picture": user_data['profile_picture'],
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        except ValueError as e:
            # في حال وجود خطأ في البيانات (مثل تكرار البريد الإلكتروني أو اسم المستخدم)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # أي خطأ غير متوقع
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







# class LoginAPIView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             password = serializer.validated_data['password']

#             user = User.get_user_by_email(email)
#             if not user:
#                 return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

#             if User.check_password(user['password'], password):
#                 return Response(
#                     {
#                         "message": "Login successful",
#                         "user": {
#                             "user_id": str(user['_id']),  # إضافة user_id
#                             "username": user['username'],
#                             "email": user['email'],
#                             "is_admin": user.get('is_admin', False),
#                         },
#                     },
#                     status=status.HTTP_200_OK,
#                 )
#             else:
#                 return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class RegisterAPIView(APIView):
#     def post(self, request):
#         # طباعة البيانات المستلمة من العميل
#         print(f"Request Data: {request.data}")

#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user_data = serializer.save()  # حفظ البيانات
#             return Response(
#                 {
#                     "message": "User created successfully.",
#                     "user": {
#                         "user_id": str(user_data['_id']),  # إضافة user_id وتحويله إلى نص
#                         "username": user_data['username'],
#                         "email": user_data['email'],
#                         "is_admin": user_data.get('is_admin', False),  # التعامل مع is_admin بشكل صحيح
#                     },
#                 },
#                 status=status.HTTP_201_CREATED,
#             )
#         # في حالة حدوث خطأ في التحقق من البيانات
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



