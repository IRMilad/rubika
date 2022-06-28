import re
import warnings


class AuthorisationValues:
    pass


class GetDCs(object):
    url = 'https://getdcmess.iranlms.ir/'
    encrypt = False

    def __init__(self, api_version='4', *args, **kwargs):
        """_GetDCs_

        Args:
            api_version (str, optional):
                _api version_. Defaults to '4'.
        """

        self.data = {'api_version': '4'}


class SignIn(object):
    tmp_session = True

    def __init__(self, phone_code, phone_number,
                 phone_code_hash, *args, **kwargs) -> None:
        """_SignIn_

        Args:
            phone_code (str):
                _verification code_
            phone_number (str):
                _phone number_
            phone_code_hash (str):
                _phone code hash_
        """
        self.input = {
            'phone_code': phone_code,
            'phone_number': phone_number,
            'phone_code_hash': phone_code_hash
        }


class SendCode(object):
    tmp_session = True

    def __init__(self, phone_number,
                 pass_key=None, force_sms=True, *args, **kwargs):
        """_summary_

        Args:
            phone_number (str):
                _phone number_
            pass_key (str, optional):
                _two-step password_. Defaults to None.
            force_sms (bool, optional):
                _verification code via sms_.Defaults to True.
        """
        self.data = {
            'input': {
                'phone_number': phone_number,
                'pass_key': pass_key,
                'send_type': 'SMS' if force_sms else 'Internal'
            }
        }


class RegisterDevice(object):
    def __init__(self, uaer_agent, app_version,
                 lang_code='fa', *args, **kwargs):
        """_RegisterDevice_

        Args:
            uaer_agent (str):
                _uaer agent_
            app_version (_type_):
                _app version_
            lang_code (str, optional):
                _lang code_. Defaults to 'fa'.
        """

        device_model = re.search(r'(opera|chrome|safari|firefox|msie'
                                 r'|trident)\/(\d+)', uaer_agent.lower())
        if not device_model:
            device_model = 'Unknown'
            warnings.warn(f'can not parse user-agent [ {uaer_agent} ]')

        else:
            device_model = device_model.group(1) + ' ' + device_model.group(2)

        if 'Windows NT 10.0' in uaer_agent:
            system_version = 'Windows 10'

        elif 'Windows NT 6.2' in uaer_agent:
            system_version = 'Windows 8'

        elif 'Windows NT 6.1' in uaer_agent:
            system_version = 'Windows 7'

        elif 'Windows NT 6.0' in uaer_agent:
            system_version = 'Windows Vista'

        elif 'Windows NT 5.1' in uaer_agent:
            system_version = 'windows XP'

        elif 'Windows NT 5.0' in uaer_agent:
            system_version = 'Windows 2000'

        elif 'Mac' in uaer_agent:
            system_version = 'Mac/iOS'

        elif 'X11' in uaer_agent:
            system_version = 'UNIX'

        elif 'Linux' in uaer_agent:
            system_version = 'Linux'

        else:
            system_version = 'Unknown'

        # window.navigator.mimeTypes.length (outdated . Defaults to '2')

        self.input = {
            'token': '',
            'lang_code': lang_code,
            'token_type': 'Web',
            'app_version': f'WB_{app_version}',
            'system_version': system_version,
            'device_model': device_model.title(),
            'device_hash': '2' + ''.join(re.findall(r'\d+', uaer_agent))}


class LoginDisableTwoStep(object):
    tmp_session = True

    def __init__(self, phone_number: str, email_code: str,
                 forget_password_code_hash: str, *args, **kwargs):
        """_summary_

        Args:
            phone_number (str):
                _phone number_

            email_code (str):
                _email code_

            forget_password_code_hash (str):
                _forget password code hash_
        """

        self.input = {
            'phone_number': phone_number, 'email_code': email_code,
            'forget_password_code_hash': forget_password_code_hash}


class LoginTwoStepForgetPassword(object):
    tmp_session = True

    def __init__(self, phone_number: str, *args, **kwargs):
        """_LoginTwoStepForgetPassword_

        Args:
            phone_number (str):
                _phone number_
        """

        self.input = {'phone_number': phone_number}
