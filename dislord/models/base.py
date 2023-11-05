import dataclasses
import time
from dataclasses import dataclass
import json
import inspect
from enum import Enum, EnumType
from typing import get_type_hints, Union, Type

from models.type import PartialOptional


def cast(obj, type_hint, param_name=None, client=None):
    if type_hint is None:
        return obj

    if obj is None or obj is dataclasses.MISSING:
        if getattr(type_hint, "__origin__", None) is Union and type(None) in type_hint.__args__:
            return obj
        else:
            raise RuntimeError(f"Required field {param_name if param_name else ''} is not given for type: {type_hint}")

    if isinstance(obj, list) and getattr(type_hint, "__origin__", None) is list:
        return [cast(o, type_hint.__args__[0], param_name, client) for o in obj]
    elif isinstance(obj, dict) and getattr(type_hint, "__origin__", None) is dict:
        # return {ok: ov for (ok, ov) in obj.items()}
        raise NotImplementedError("TODO")
    elif getattr(type_hint, "__origin__", None) is obj.__class__:
        return obj

    if dataclasses.is_dataclass(type_hint):
        if type_hint.is_base_model():
            return type_hint.from_dict(obj, client)
        else:
            return type_hint.from_dict(obj)
    elif isinstance(type_hint, EnumType):
        return type_hint(obj)
    elif getattr(type_hint, '__origin__', None) is Union:
        for u_type in type_hint.__args__:
            return cast(obj, u_type, param_name, client)
    else:
        return obj


@dataclass
class BaseModel:
    @classmethod
    def from_dict(cls, env, client):
        type_hints = get_type_hints(cls)
        if cls == type(env):
            return env

        params = {}
        for p, hint in type_hints.items():
            params[p] = cast(env.get(p, dataclasses.MISSING), hint, p)
        obj = cls(**params)  # noqa
        obj.client = client
        return obj

    @classmethod
    def from_kwargs(cls, *, client, **kwargs):
        return cls.from_dict(kwargs, client)

    @staticmethod
    def is_base_model():
        return True


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, Enum):
            return o.value
        if dataclasses.MISSING:
            return None
        return super().default(o)
