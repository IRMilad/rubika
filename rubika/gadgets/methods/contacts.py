import time


class ContactValues:
    pass


class DeleteContact(object):
    def __init__(self, user_guid: str, *args, **kwargs):
        """_DeleteContact_

        Args:
            user_guid (str):
                _user guid_
        """

        self.input = {'user_guid': user_guid}


class AddAddressBook(object):
    def __init__(self, phone_number: str,
                 first_name: str, last_name: str = None, *args, **kwargs):
        """_AddAddressBook_

        Args:
            phone_number (str):
                _phone number_

            first_name (str):
                _first name_

            last_name (str, optional):
                _last name_. Defaults to None.
        """

        self.input = {
            'phone': phone_number,
            'first_name': first_name, 'last_name': last_name}


class GetContactsUpdates(object):
    def __init__(self, state: int = None, *args, **kwargs):
        """_GetContactsUpdates_

        Args:
            state (int, optional):
                _state_. Defaults to int(time.time()).
        """

        if not state:
            state = int(time.time())
        self.input = {'state': state}


class GetContacts(object):
    def __init__(self, start_id: int = None, *args, **kwargs):
        """_GetContacts_

        Args:
            start_id (int, optional):
                _start id_. Defaults to None.
        """

        self.input = {'start_id': start_id}

