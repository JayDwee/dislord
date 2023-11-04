import dataclasses
import time
from dataclasses import dataclass
import json
import inspect
from enum import Enum, EnumType
from typing import get_type_hints, Union


def cast(obj, type_hint, param_name=None):
    if type_hint is None:
        return obj

    if isinstance(obj, list) and getattr(type_hint, "__origin__", None) is list:
        return [cast(o, type_hint.__args__[0]) for o in obj]
    elif isinstance(obj, dict) and getattr(type_hint, "__origin__", None) is dict:
        # return {ok: ov for (ok, ov) in obj.items()}
        raise NotImplementedError("TODO")

    if obj is None:
        if getattr(type_hint, "__origin__", None) is Union and type(None) in type_hint.__args__:
            return None
        else:
            raise RuntimeError(f"Required field {param_name if param_name else ''} is not given for type: {type_hint}")

    if dataclasses.is_dataclass(type_hint):
        return type_hint.from_dict(obj)
    elif isinstance(type_hint, EnumType):
        return type_hint(obj)
    elif getattr(type_hint, '__origin__', None) is Union:
        for u_type in type_hint.__args__:
            return cast(obj, u_type)
    else:
        return obj


@dataclass
class BaseModel:
    @classmethod
    def from_dict(cls, env):
        type_hints = get_type_hints(cls)

        params = {}
        for p, hint in type_hints.items():
            params[p] = cast(env.get(p), hint, p)
        return cls(**params) # noqa


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, Enum):
            return o.value
        return super().default(o)
