import requests


class AresApiClient:
    """Retrieves and manipulates data from the Czech Republic's ARES register

    The lookup is based on unique ID number called "IČO" that each company in the Czech republic has
    Since the word "IČO" contains czech diacritics, it is further replaced with "ICO" or "ico" in the code
    The subject's data can be further manipulated by other methods

    Methods:
        get_subject_by_ico: This is "the core method" of the whole class. It returns subject data from ARES based on a given ICO
        get_subject_formal_description: Returns a description of a subject in a way expected in formal written communication
    """

    # "constants"
    ICO_LENGTH = 8  # ICO in the Czech Republic is always eight-digit long
    ARES_REQUEST_URL = "https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/"  # ARES API endpoint

    @staticmethod
    def get_subject_by_ico(ico):
        """Returns subject data as dictionary from ARES register

        Looks up subject by its ICO IN ARES register REST Api endpoint
        Returns subject data as dictionary (with some nested dictionaries)

        The ICO is always eight-digit. If less digits are passed, zeros are added before it up to full length
        This is because lot of state institutions in the Czech Republic have ICO starting with several zeros
        If ICO parameter is ever passed by a user input, it would be cumbersome to write them all

        The result relies on the ARES server REST Api settings to not change over time
        If request is not successfull, None is returned

        Args:
            ico (string or int): the unique ID number used to look up the subject in the ARES register

        Returns:
            dictionary or None

        Raises:
            TypeError: if ico arg can't be converted to a string

        """
        try:
            string_ico = str(ico)  # we force ico argument to be string even if it was passed as a number
        except TypeError as e:
            print(f'string conversion failed on {ico}: {e}')
            return

        # if less than 8 digits were passed, the length is insufficient
        length_insufficient = AresManager.ICO_LENGTH - len(string_ico)

        if length_insufficient:  # zeros will be added before ico up to required length
            string_ico = length_insufficient * "0" + string_ico

        response = requests.get(AresManager.ARES_REQUEST_URL + string_ico)  # actually retrieving the data

        if response.status_code != 200:
            # if request is not successfull, None is returned
            return

        data = response.json()  # ARES gives data in JSON format. Using .json() results in a dictionary of values
        return data

    @staticmethod
    def get_subject_formal_description(ico):
        """Returns subject data in a way expected in a formal human written communication

        Looks up the subject by its ICO IN ARES register
        Returns some of its data that are considered to be descriptive enough
        These are given by the Czech laws (based on circumstances) or simply by a common conventions
        If subject is not successfully found, None is returned

        Args:
            ico (string or int): the unique ID number used to look up the subject in the ARES register

        Returns:
            string or None

        """
        data = AresManager.get_subject_by_ico(ico)  # retrieving all the data of the subject as a dictionary
        if data:    # if succesfully retrieved, use only some of them
            return f'{data["obchodniJmeno"]}, IČO {data["ico"]}, sídlem {data["sidlo"]["textovaAdresa"]}'
