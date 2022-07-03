import os
import re
import sys
import json
import time
import random
import typing
import warnings
from .classino import Classino

with open(os.path.join(os.path.dirname(__file__), '../methods.json')) as grouping:
    grouping = json.load(grouping)


class Funcs:
    system_versions = {
        'Windows NT 10.0': 'Windows 10',
        'Windows NT 6.2': 'Windows 8',
        'Windows NT 6.1': 'Windows 7',
        'Windows NT 6.0': 'Windows Vista',
        'Windows NT 5.1': 'windows XP',
        'Windows NT 5.0': 'Windows 2000',
        'Mac': 'Mac/iOS',
        'X11': 'UNIX',
        'Linux': 'Linux'
    }
    
    @classmethod
    def GetPhone(cls, value, *args, **kwargs):
        phone_number = ''.join(re.findall(r'\d+', value))
        if not phone_number.startswith('98'):
            phone_number = '98' + phone_number
        return phone_number
    
    @classmethod
    def GetBrowser(cls, user_agent, lang_code, app_version, *args, **kwargs):
        device_model = re.search(r'(opera|chrome|safari|firefox|msie'
                                 r'|trident)\/(\d+)', user_agent.lower())
        if not device_model:
            device_model = 'Unknown'
            warnings.warn(f'can not parse user-agent ({user_agent})')

        else:
            device_model = device_model.group(1) + ' ' + device_model.group(2)
        
        system_version = 'Unknown'
        for key, value in cls.system_versions.items():
            if key in user_agent:
                system_version = value
                break
        # window.navigator.mimeTypes.length (outdated . Defaults to '2')
        device_hash = '2'
        return {
            'token': '',
            'lang_code': lang_code,
            'token_type': 'Web',
            'app_version': f'WB_{app_version}',
            'system_version': system_version,
            'device_model': device_model.title(),
            'device_hash': device_hash + ''.join(re.findall(r'\d+', user_agent))}
        
    @classmethod 
    def RandomNumber(cls, *args, **kwargs):
        return int(random.random() * 1e6 + 1)

    @classmethod
    def Timestamp(cls, *args, **kwargs):
        return int(time.time())

    @classmethod
    def GetFormat(cls, value, *args, **kwargs):
        return value.split('.')[-1]

    @classmethod
    def GetHashLink(cls, value, *args, **kwargs):
        return value.split('/')[-1]

    @classmethod
    def ToFloat(cls, value, *args, **kwargs):
        return float(value)

    @classmethod
    def ToNumber(cls, value, *args, **kwargs):
        return int(value)
    
    @classmethod
    def ToString(cls, value, *args, **kwargs):
        return str(value)
    
    @classmethod
    def ToArray(cls, value, *args, **kwargs):
        if isinstance(value, list):
            return value
        
        elif isinstance(value, str):
            return [value]
        
        try:
            return dict(value)
        
        except ValueError:
            try:
                return value.to_dict()
            
            except:
                return value

    @classmethod
    def ToMetadata(cls, value, *args, **kwargs):
        conflict = 0
        meta_data_parts = []
        for markdown in re.finditer(r'`.*`|\*\*.*\*\*|__.*__|\[.*\]\(\S+:\S+\)', value):
            span = markdown.span()
            markdown = markdown.group(0)
            if markdown.startswith('`'):
                value = re.sub(r'`(.*)`', r'\1', value, count=1)
                meta_data_parts.append({
                        'type': 'Mono',
                        'from_index': span[0] - conflict,
                        'length': span[1] - span[0] - 2
                    }
                )
                conflict += 2

            elif markdown.startswith('**'):
                value = re.sub(r'\*\*(.*)\*\*', r'\1', value, count=1)
                meta_data_parts.append({
                        'type': 'Bold',
                        'from_index': span[0] - conflict,
                        'length': span[1] - span[0] - 4
                    }
                )
                conflict += 4

            elif markdown.startswith('__'):
                value = re.sub(r'__(.*)__', r'\1', value, count=1)
                meta_data_parts.append({
                        'type': 'Italic',
                        'from_index': span[0] - conflict,
                        'length': span[1] - span[0] - 4
                    }
                )
                conflict += 4

            else:
                mention = re.search(r'\[(.*)\]\((\S+):(\S+)\)', markdown)
                if mention is not None:
                    value = re.sub(r'\[(.*)\]\((\S+):(\S+)\)', r'\1', value, count=1)
                    meta_data_parts.append({
                            'type': 'MentionText',
                            'from_index': span[0] - conflict,
                            'length': len(mention.group(1)),
                            'mention_text_object_guid': mention.group(3),
                            'mention_text_object_type': mention.group(2).title()
                        }
                    )
                    conflict += 5 + len(mention.group(3)) + len(mention.group(2))

        result = {'text': value}
        if meta_data_parts:
            result['metadata'] = {
                'meta_data_parts': meta_data_parts
            }
        
        return result


class BaseMethod(dict):
    __name__ = 'CustomMethod'

    def __init__(self, method: dict, *args, **kwargs) -> None:
        self.method = method

    @property
    def method_name(self):
        return self.__name__[0].lower() + self.__name__[1:]

    def build(self, argument, param, *args, **kwargs):
        ifs = param.get('ifs')
        func = param.get('func')
        types = param.get('types')
        alloweds = param.get('alloweds')

        # set defualt value
        try:
            value = self.request[argument]
        
        except KeyError:
            value = param['default']
            if isinstance(value, dict):
                default_func = value.get('func')
                if isinstance(default_func, str):
                    value = getattr(Funcs, default_func)(**value, **self.request)

        # get value heirship
        for heirship in param.get('heirship', []):
            try:
                value = self.request[heirship]
            except KeyError:
                pass
            
        # clall func method
        if isinstance(func, str) and value is not None:
            value = getattr(Funcs, func)(value, **self.request)
            argument = param.get('cname', argument)
            
        # check value types
        if types and not type(value).__name__ in types:
            if not value is None and 'optional' in types:
                raise TypeError(f'The given {argument} must be {types}')


        if alloweds is not None:
            if isinstance(value, list):
                for _value in value:
                    if _value not in alloweds:
                        raise ValueError(f'the {argument}({_value}) value is not in the allowed list {alloweds}')

            elif value not in alloweds:
                raise ValueError(f'the {argument}({value}) value is not in the allowed list {alloweds}')
    
        # get ifs 
        if isinstance(ifs, dict):
            
            # move to the last key
            if 'otherwise' in ifs:
                ifs['otherwise'] = ifs.pop('otherwise')

            for operator, work in ifs.items():
                if type(value).__name__ == operator or operator == 'otherwise':
                    func = work.get('func')
                    param = work
                    if isinstance(func, str):
                        value = getattr(Funcs, func)(value, **self.request)
                    break

        # to avoid adding an extra value if there is "cname"
        if argument in self.request:
            self.request.pop(argument)
                
        if value is not None:
            if param.get('unpack'):
                self.request.update(value)

            else:
                self.request[param.get('cname', argument)] = value


    def __call__(self, *args, **kwargs) -> dict:
        self.request = {}

        if isinstance(self.method['params'], dict):
            params = list(self.method['params'].keys())
            for index, value in enumerate(args):
                try:
                    self.request[params[index]] = value

                except IndexError:
                    pass
 
            for argument, value in kwargs.items():
                if self.method['params'].get(argument):
                    self.request[argument] = value

            for argument, param in self.method['params'].items():
                try:
                   self.build(argument, param)
                except KeyError:
                    if not 'optional' in param['types']:
                        raise TypeError(
                            f'{self.__name__}() required argument ({argument})')


        if self.method.get('urls') is not None:
            self.request['method'] = self.method_name
        
        else:
            self.request = {'method': self.method_name, 'input': self.request}
        

        self.request['urls'] = self.method.get('urls')
        self.request['encrypt'] = self.method.get('encrypt', True)
        self.request['tmp_session'] = bool(self.method.get('tmp_session'))
        
        return self.request


class BaseGrouping(Classino):
    def __init__(self, methods: dict, *args, **kwargs) -> None:
        self.methods = methods

    def __dir__(self) -> typing.Iterable[str]:
        return self.methods.keys()

    def __getattr__(self, name) -> BaseMethod:
        if name in self.methods['Values']:
            return name

        method = self.create(name, (BaseMethod,), dir(self))
        return method(self.methods[method.__name__])


class Methods(Classino):
    def __init__(self, name, *args, **kwargs) -> None:
        self.__name__ = name

    def __dir__(self) -> typing.Iterable[str]:
        return grouping.keys()
    
    def __getattr__(self, name) -> BaseGrouping:
        group = self.create(name, (BaseGrouping,), dir(self))
        return group(methods=grouping[group.__name__])
           

sys.modules[__name__] = Methods(__name__)