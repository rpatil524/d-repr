import copy
from typing import Dict

import orjson
import uuid
import xmltodict

from drepr.models import DRepr, ResourceType, ResourceDataFile, ResourceData, ResourceDataString


def patch(repr: DRepr, resources: Dict[str, ResourceData]) -> DRepr:
    """
    This patch will turn any XML resources to JSON using xmltodict
    """
    need_patch = False
    for resource in repr.resources:
        if resource.type == ResourceType.XML:
            need_patch = True

    if need_patch:
        repr = copy.deepcopy(repr)
        for resource in repr.resources:
            if resource.type == ResourceType.XML:
                if isinstance(resources[resource.id], ResourceDataFile):
                    with open(resources[resource.id].file_path, "r") as f:
                        doc = xmltodict.parse(f.read())
                else:
                    doc = xmltodict.parse(resources[resource.id].value)

                resource.type = ResourceType.JSON
                resources[resource.id] = ResourceDataString(orjson.dumps(doc))
                # resources[resource.id] = ResourceDataFile(f"/tmp/{str(uuid.uuid4())}.json")
                # with open(resources[resource.id].file_path, "wb") as f:
                #     f.write(orjson.dumps(doc))

    return repr