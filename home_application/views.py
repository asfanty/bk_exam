# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""
import base64
import json

from django.http import JsonResponse

from blueking.component.shortcuts import get_client_by_request
from common.mymako import render_mako_context
from home_application.utils import result


def home(request):
    """
    首页
    """
    # return render_mako_context(request, '/home_application/home.html')
    return render_mako_context(request, '/home_application/index.html')


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')


def test(request):
    return result('zhangjunjie')


#获取业务列表
def get_business(request):
    client = get_client_by_request(request)
    kwargs = {}
    result = client.cc.search_business(kwargs)
    return JsonResponse(result)


#主机查询功能
def search_host(request):
    client = get_client_by_request(request)
    # content = json.loads(request.body)
    bk_app_id = int(request.GET.get('bk_biz_id'))
    data = request.GET.get('ip_list')
    kwargs = {
        "page": {"start": 0, "limit": 100, "sort": "bk_host_id"},
        "ip": {
            "flag": "bk_host_innerip|bk_host_outerip",
            "exact": 1,
            "data": []
        },
        "condition": [
            {
                "bk_obj_id": "host",
                "fields": [
                ],
                "condition": []
            },
            {
                "bk_obj_id": "biz",
                "fields": [
                    "default",
                    "bk_biz_id",
                    "bk_biz_name",
                ],
                # 根据业务ID查询主机
                "condition": [
                    {
                        "field": "bk_biz_id",
                        "operator": "$eq",
                        "value": bk_app_id
                    }
                ]
            }
        ]
    }
    result = client.cc.search_host(kwargs)
    return JsonResponse(result)


#执行脚本
def execute_script(request):
    f = open('./media/stat.sh')
    test = f.read()
    test = base64.b64encode(test)
    bk_app_id = int(request.GET.get('bk_biz_id'))
    # content = json.loads(request.body)
    client = get_client_by_request(request)
    kwargs = {
        "bk_biz_id": bk_app_id,
        "script_content": test,
        "script_param": "aGVsbG8=",
        "script_timeout": 1000,
        "account": "root",
        "is_param_sensitive": 0,
        "script_type": 1,
        "ip_list": [
            {
                "bk_cloud_id": 0,
                "ip": "10.0.1.13"
            }
        ],
        "custom_query_id": [
            "3"
        ]
    }
    result = client.job.fast_execute_script(kwargs)

    inst_id = result['data']['job_instance_id']
    client = get_client_by_request(request)
    kwargs = {
        "bk_biz_id": bk_app_id,
        "job_instance_id": inst_id
    }
    result = client.job.get_job_instance_status(kwargs)

    client = get_client_by_request(request)
    kwargs = {
        "bk_biz_id": bk_app_id,
        "job_instance_id": inst_id
    }
    result = client.job.get_job_instance_log(kwargs)
    return JsonResponse(result)
