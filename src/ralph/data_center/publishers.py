# -*- coding: utf-8 -*-
from copy import deepcopy

import pyhermes
from django.conf import settings


def _get_host_data(instance):
    from ralph.assets.api.serializers import DCHostSerializer
    serializer = DCHostSerializer(instance=instance)
    if hasattr(serializer.instance, '_previous_state'):
        data = deepcopy(serializer.data)
        data['_previous_state'] = {
            k: v for k, v in serializer.instance._previous_state.items()
            if k in serializer.instance.previous_dc_host_update_fields
        }
    else:
        data = serializer.data
    return data

if settings.HERMES_HOST_UPDATE_TOPIC_NAME:
    @pyhermes.publisher(
        topic=settings.HERMES_HOST_UPDATE_TOPIC_NAME, auto_publish_result=True
    )
    def publish_host_update(instance):
        return _get_host_data(instance)
