from rest_framework.permissions import BasePermission

class IsAuthor(BasePermission): #проверяем может ли юзер изменить/удалить комментарии
    def has_object_permission(self, request, view, obj):
    #проверяем есть ли право у юзера на изменения объекта. пишем когда работаем с конкретным объектом
        return request.user == obj.user

