import dataclasses
from dataclasses import dataclass
import json
from enum import Enum, EnumType
from typing import get_type_hints, Union

from models.type import Missing


def cast(obj, type_hint, param_name=None, client=None):
    if type_hint is None:
        return obj

    if obj is None or obj == [] or obj == {} or obj is Missing:
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
    elif isinstance(type_hint, EnumType) and not isinstance(type(obj), EnumType):
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
            if isinstance(env, dict):
                prop = env.get(p, Missing)
            else:
                prop = getattr(env, p, Missing)
            params[p] = cast(prop, hint, p)
        obj = cls(**params)  # noqa
        obj.client = client
        return obj

    @classmethod
    def from_kwargs(cls, *, client=None, **kwargs):
        return cls.from_dict(kwargs, client)

    @staticmethod
    def is_base_model():
        return True

    def __eq__(self, other):
        result = True
        for eq_attr in get_type_hints(self.__class__):
            self_attr = getattr(self, eq_attr, None)
            other_attr = getattr(other, eq_attr, None)
            result = result and compare_missing_none(self_attr, other_attr)
        return result



class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, Enum):
            return o.value
        if o is Missing:
            return None
        return super().default(o)


def compare_missing_none(obj1, obj2):
    obj1_is_none_or_missing = obj1 is None or obj1 is Missing
    obj2_is_none_or_missing = obj2 is None or obj2 is Missing
    if obj1_is_none_or_missing and obj2_is_none_or_missing:
        return True
    else:
        if isinstance(obj1, Enum) and isinstance(obj2, Enum):
            return obj1.value == obj2.value
        else:
            return obj1.__eq__(obj2)

