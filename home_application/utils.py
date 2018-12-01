# -*- coding: utf-8 -*-
from django.http import JsonResponse


def result(object):
    data = {}
    data['result'] = True
    data['message'] = 'success'
    data['data'] = object
    return JsonResponse(data)
