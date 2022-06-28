class StickerValues:
    All = 'All'

    Add = 'Add'
    Remove = 'Remove'


class SearchStickers(object):
    def __init__(self, search_text: str,
                 start_id: int = None, *args, **kwargs):
        """_SearchStickers_

        Args:
            search_text (str):
                _search text_

            start_id (int, optional):
                _start id_. Defaults to None.
        """

        self.input = {'search_text': search_text, 'start_id': start_id}


class GetMyStickerSets(object):
    pass


class GetStickerSetByID(object):
    def __init__(self, sticker_set_id: str, *args, **kwargs):
        """_GetStickerSetByID_

        Args:
            sticker_set_id (str):
                _sticker set id_
        """

        self.input = {'sticker_set_id': sticker_set_id}


class ActionOnStickerSet(object):
    def __init__(self, sticker_set_id: str,
                 action: str = StickerValues.Add, *args, **kwargs):
        """_ActionOnStickerSet_

        Args:
            sticker_set_id (str):
                _sticker set id_
            action (str, optional):
                _action_. Defaults to StickerValues.Add. (
                    StickerValues.Add,
                    StickerValues.Remove
                )
        """

        self.input = {'sticker_set_id': sticker_set_id, 'action': action}


class GetStickersByEmoji(object):
    def __init__(self, emoji_character: str,
                 suggest_by: str = StickerValues.All, *args, **kwargs):
        """_GetStickersByEmoji_

        Args:
            emoji_character (str):
                _emoji character_

            suggest_by (str, optional):
                _suggest by_. Defaults to StickerValues.All.
        """

        self.input = {
            'emoji_character': emoji_character, 'suggest_by': suggest_by}


class GetStickersBySetIDs(object):
    def __init__(self, sticker_set_ids: list, *args, **kwargs):
        """_GetStickersBySetIDs_

        Args:
            sticker_set_ids (list):
                _sticker set ids_
        """

        self.input = {'sticker_set_ids': sticker_set_ids}


class GetTrendStickerSets(object):
    def __init__(self, start_id: int = None, *args, **kwargs):
        """_GetTrendStickerSets_

        Args:
            start_id (int, optional):
                _star id_. Defaults to None.
        """

        self.input = {'start_id': start_id}
