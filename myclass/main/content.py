from django.http import JsonResponse

from monsters.models import Monster


def change_content(request, name, resource):
    if 'Super_Game_Admin' in request.COOKIES.keys():
        if name == 'cover' or name == 'action':
            value = request.FILES.get('value')
            exec('resource.' + name + '=value')
        elif 'floor' in name:
            value = request.POST.get('value')
            value = value.split(' ')
            eval('resource.'+name+'.clear()')
            for v in value:
                exec('resource.'+name+'.add(Monster.objects.get(id=v))')
            value = []
            for v in eval('resource.'+name+'.all()'):
                value.append(v.name)
            value = '、'.join(value)
        else:
            value = request.POST.get('value')
            exec('resource.' + name + '=value')
        if not value:
            return JsonResponse({'tip': '未填充数据'})
        resource.save()
        return JsonResponse({'tip': '改动成功', 'result': str(value)})
    else:
        return JsonResponse({'tip': '权限不足'})
        # return redirect(request.headers['REFERER'])
