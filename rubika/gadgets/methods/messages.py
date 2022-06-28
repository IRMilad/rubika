import time
import typing
import random


class MessageValues:
    Pin = 'Pin'
    Unpin = 'Unpin'

    File = 'File'
    Image = 'Image'

    Quiz = 'Quiz'
    Regular = 'Regular'

    Text = 'Text'

    FromMin = 'FromMin'
    FromMax = 'FromMax'

    Local = 'Local'
    Global = 'Global'


class MetaData(object):
    markdowns = {
        'Mono': '`',
        'Bold': '**',
        'Italic': '__'
    }

    def allowed(self, from_index, length):
        for part in self.marks:
            ln = from_index + length
            lp = part['from_index'] + part['length']
            if from_index <= part['from_index']:
                if ln >= lp:
                    return False

            if from_index >= part['from_index']:
                if ln <= lp:
                    return False
        return True

    def __init__(self, text: str = None):
        self.marks = []
        if isinstance(text, str):
            marks_length = None
            while marks_length is None or len(self.marks) != marks_length:
                marks_length = len(self.marks)
                for name, value in self.markdowns.items():
                    from_index = text.find(value)
                    if from_index != -1:
                        length = text.find(value, from_index + len(value))
                        if length != -1:
                            length -= from_index + len(value)
                            if self.allowed(from_index, length=length):
                                text = text.replace(value, '', 2).strip(' ')
                                if len(text) <= from_index + length:
                                    length = len(text) - from_index
                                self.marks.append({
                                    'type': name,
                                    'length': length,
                                    'from_index': from_index
                                })
        self.text = text


class RequestSendFile(object):
    def __init__(self, file_name: str,
                 size: int = None, mime: str = None, *args, **kwagrs):
        """_RequestSendFile_

        Args:
            file_name (str):
                _file name_
            size (int, optional):
                _file size_. Defaults to None.
            mime (str, optional):
                _file format_. Defaults to None.
        """

        self.input = {
            'mime': mime or file_name.split('.')[-1],
            'size': size,
            'file_name': file_name}


class DeleteMessages(object):
    def __init__(self, object_guid: str,
                 message_ids: typing.Union[str, list],
                 delete_type: str = MessageValues.Global, *args, **kwargs):
        """_summary_

        Args:
            object_guid (str):
                _object guid_

            message_ids (list, str):
                _message ids_

            delete_type (str, optional):
                _delete type_ Default MessageValues.Global (
                    MessageValues.Local,
                    MessageValues.Global
                )
        """

        if not isinstance(message_ids, list):
            message_ids = [message_ids]
        self.input = {'object_guid': object_guid,
                      'message_ids': message_ids, 'type': delete_type}


class ForwardMessages(object):
    def __init__(self, from_object_guid: str, to_object_guid: str,
                 message_ids: typing.Union[list, str], *args, **kwargs):
        """_ForwardMessages_

        Args:
            from_object_guid (str):
                _from object guid_

            to_object_guid (str):
                _to object guid_

            message_ids (list, str):
                _message ids_
        """

        if not isinstance(message_ids, list):
            message_ids = [message_ids]
        self.input = {

            'rnd': str(int(random.random() * 1e6 + 1)),
            'from_object_guid': from_object_guid,
            'to_object_guid': to_object_guid,
            'message_ids': message_ids}


class EditMessage(object):
    def __init__(self, object_guid: str,
                 message_id: str, text: str, *args, **kwargs):
        """_EditMessage_

        Args:
            object_guid (str):
                _object guid_

            message_id (str):
                _message id_

            text (str):
                _message id_
        """
        marks = MetaData(text)
        self.input = {'object_guid': object_guid,
                      'message_id': message_id, 'text': text}
        if marks.marks:
            self.input['metadata'] = {'meta_data_parts': marks.marks}


class SendMessage(object):
    def __init__(self,
                 object_guid: str,
                 text: str = None,
                 reply_to: str = None,
                 file: typing.Union[dict, object] = None,
                 thumb: typing.Union[dict, object] = None,
                 send_type: str = MessageValues.File, *args, **kwargs):
        """_SendMessage_

        Args:
            object_guid (str):
                _object guid_

            text (str, optional):
                _text or caption_. Defaults to None.

            reply_to (str, optional):
                _reply to_. Defaults to None.

            file (object, dict, optional):
                _file_. Defaults to None.

            thumb (object, dict, optional):
                _description_. Defaults to None.

            send_type (str, optional):
                _send type_. Defaults to MessageValues.File (
                    MessageValues.File,
                    MessageValues.Image)
        """

        if file is not None:
            if not isinstance(file, dict):
                file = file.__dict__

            if thumb is not None:
                if not isinstance(file, dict):
                    file = file.__dict__
                if isinstance(thumb, dict):
                    file.update(thumb)

            file['type'] = send_type
        marks = MetaData(text)
        self.input = {
            'text': marks.text,
            'rnd': str(int(random.random() * 1e6 + 1)),
            'object_guid': object_guid,
            'file_inline': file,
            'reply_to_message_id': reply_to
        }
        if marks.marks:
            self.input['metadata'] = {'meta_data_parts': marks.marks}


class CreatePoll(object):
    def __init__(self,
                 object_guid: str,
                 question: str,
                 options: list,
                 poll_type: str = MessageValues.Regular,
                 is_anonymous: bool = True,
                 allows_multiple_answers: bool = False,
                 correct_option_index: int = 0,
                 explanation: str = None):
        """_CreatePoll_

        Args:
            object_guid (str):
                _objec guid_

            question (str):
                _question_

            options (list):
                _options_

            poll_type (str, optional):
                _poll type_. Defaults to MessageValues.Regular. (
                    MessageValues.Quiz,
                    MessageValues.Regular
                )

            is_anonymous (bool, optional):
                _is anonymous_. Defaults to True.

            allows_multiple_answers (bool, optional):
                _allows multiple answers_. Defaults to False.

            correct_option_index (int, optional):
                _correct option index_. Defaults to 0.

            explanation (str, optional):
            _explanation_. Defaults to None.

        Raises:
            ValueError: _the minimum number of options is two_
            IndexError: _correct option index not found_
        """

        if len(options) <= 1:
            raise ValueError('the minimum number of options is two')

        if poll_type == MessageValues.Quiz:
            allows_multiple_answers = False
            try:
                options[correct_option_index]

            except IndexError:
                raise IndexError('correct option index not found')

        self.input = {
            'object_guid': object_guid,
            'question': question,
            'options': options,
            'type': poll_type,
            'is_anonymous': is_anonymous,
            'allows_multiple_answers': allows_multiple_answers,
            'correct_option_index': correct_option_index,
            'explanation': explanation}


class VotePoll(object):
    def __init__(self, poll_id, selection_index: int):
        """_VotePoll_

        Args:
            poll_id (_type_):
                _poll id_
            selection_index (int):
                _selection index_
        """

        self.input = {'poll_id': poll_id, 'selection_index': selection_index}


class GetPollStatus(object):
    def __init__(self, poll_id: str):
        """_GetPollStatus_

        Args:
            poll_id (str): _poll id_
        """

        self.input = {'poll_id': poll_id}


class GetPollOptionVoters(object):
    def __init__(self, poll_id: str, selection_index: int, start_id=None):
        """_GetPollOptionVoters_

        Args:
            poll_id (str):
                _poll id_
            selection_index (int):
                _selection index_
            start_id (_type_, optional):
                _start id_. Defaults to None.
        """

        self.input = {
            'poll_id': poll_id,
            'start_id': start_id,
            'selection_index': selection_index}


class SetPinMessage(object):
    def __init__(self, object_guid: str, message_id: str,
                 action: str = MessageValues.Pin, *args, **kwargs):
        """_SetPinMessage_

        Args:
            object_guid (str):
                _object guid_

            message_id (str):
                _message id_

            action (str, optional):
                _action_. Defaults to MessageValues.Pin. (
                    MessageValues.Pin,
                    MessageValues.Unpin
                )
        """

        self.input = {
            'object_guid': object_guid,
            'message_id': message_id,
            'action': action}


class GetMessagesUpdates(object):
    def __init__(self, object_guid: str, state: int = None, *args, **kwargs):
        """_GetMessagesUpdates_

        Args:
            object_guid (str):
                _object guid_

            state (int, optional):
                _state_. Defaults to int(time.time()).
        """

        if not state:
            state = int(time.time())
        self.input = {'object_guid': guid, 'state': state}


class SearchGlobalMessages(object):
    def __init__(self, search_text: str, search_type=MessageValues.Text,
                 start_id: int = None, *args, **kwargs):
        """_SearchGlobalMessages_

        Args:
            search_text (str):
                _search text_

            search_type (str, optional):
                _search type_. Defaults to MessageValues.Text.

            start_id (int, optional):
                _start id_. Defaults to None.
        """

        self.input = {'search_text': search_text,
                      'type': search_type, 'start_id': start_id}


class ClickMessageUrl(object):
    def __init__(self, object_guid: str,
                 message_id: str, link_url: str, *args, **kwargs):
        """_ClickMessageUrl_

        Args:
            object_guid (str):
                _object guid_

            message_id (str):
                _message id_

            link_url (str):
                _link url_
        """

        self.input = {'object_guid': object_guid,
                      'message_id': message_id, 'link_url': link_url}


class GetMessagesById(object):
    def __init__(self, object_guid: str,
                 message_ids: typing.Union[list, str], *args, **kwargs):
        """_summary_

        Args:
            object_guid (str):
                _object guid_

            message_ids (list, str):
                _message ids_
        """

        if not isinstance(message_ids, list):
            message_ids = [message_ids]
        self.input = {'object_guid': object_guid, 'message_ids': message_ids}


class GetMessages(object):
    def __init__(self, object_guid: str,
                 sort: str = MessageValues.FromMin,
                 min_id: int = None,
                 max_id: int = None,
                 limit: int = 15,
                 filter_type: str = None, *args, **kwargs):
        """_GetMessages_

        Args:
            object_guid (str):
                _object guid_

            sort (str, optional):
                _sort_. Defaults to MessageValues.FromMin.(
                    MessageValues.FromMin,
                    MessageValues.FromMax
                )

            min_id (int, optional):
                _min id_. Defaults to None.

            max_id (int, optional):
                _max id_. Defaults to None.

            limit (int, optional):
                _limit_. Defaults to 15.

            filter_type (str, optional):
                _filter type_. Defaults to None.
        """

        self.input = {
            'sort': sort,
            'limit': limit,
            'min_id': min_id,
            'max_id': max_id,
            'object_guid': object_guid,
            'filter_type': filter_type}


class GetMessagesInterval(object):
    def __init__(self, object_guid: str, middle_message_id: str,
                 filter_type: str = None, *args, **kwargs):
        """_GetMessagesInterval_

        Args:
            object_guid (str):
                _object guid_

            middle_message_id (str):
                _middle messag id_

            filter_type (str, optional):
                _filter type_. Defaults to None.
        """

        self.input = {
            'object_guid': object_guid,
            'middle_message_id': middle_message_id,
            'filter_type': filter_type}



