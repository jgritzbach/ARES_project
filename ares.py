import requests


class AresApiClient:
    """Class retrieves and manipulates data from the Czech Republic's ARES register

    Request are based on a unique ID number called "IČO" that each company in the Czech republic has.
    The word "IČO" contains czech diacritics. In the code, diacritics are ignored, naming variables "ICO" or "ico"

    This class relies on the ARES server REST Api settings to not change over time.
    If these were to change in the future, the class might not work correctly
    """

    # "constants"
    ICO_LENGTH = 8  # ICO in the Czech Republic is always eight-digit long
    ARES_REQUEST_URL = "https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/"  # ARES API endpoint

    @staticmethod
    def get_subject_by_ico(ico):
        """Returns subject data as dictionary from ARES register

        Looks up subject by its ICO IN ARES register REST Api endpoint
        Returns subject data as dictionary (with some nested dictionaries)

        Args:
            ico (string or int): the unique ID number used to look up the subject in the ARES register
        Returns:
            dictionary of subject data (or None If request is not successful)
        """
        ico = AresApiClient.validate_ico(ico)
        if not ico:  # if ico did not passed validation process
            return  # None is returned

        response = requests.get(AresApiClient.ARES_REQUEST_URL + ico)  # actually retrieving the data

        if response.status_code != 200:  # if request is not successful,
            return  # None is returned

        data = response.json()  # ARES returns data in JSON format. Using .json() results in a dictionary of values
        return data

    @staticmethod
    def get_subject_formal_description(ico):
        """Returns subject data from ARES formatted as string in a way expected in a formal human written communication

        Sometimes the Czech laws (or simply common conventions) require proper identification of the subject
        Usually the whole name, IČO and full address is required to identify subject reliably

        Args:
            ico (string or int): the unique ID number used to look up the subject in the ARES register

        Returns:
            string (or None If subject is not successfully found)
        """
        data = AresApiClient.get_subject_by_ico(ico)  # retrieving all the data of the subject as a dictionary
        if data:  # if retrieved successfully, use only some of them
            return f'{data["obchodniJmeno"]}, IČO {data["ico"]}, sídlem {data["sidlo"]["textovaAdresa"]}'

    @staticmethod
    def validate_ico(ico):
        """Mutates the ico to be suited for ARES API

        Returns: string (or None if string conversion fails)
        """
        ico = AresApiClient._force_string(ico)  # Parses ico to a string, if not already
        if not ico:  # if the string conversion failed
            return  # return None

        # ARES API requires 8-digit long parameter
        ico = AresApiClient._force_full_length(ico)  # add zeros before ico up to full length

        return ico

    @staticmethod
    def _force_string(ico):
        """Parses ico to a string, if not already

        Returns string (or None if the string conversion fails)
        """
        try:
            ico = str(ico)  # we force ico argument to be string even if it was passed as a number
        except TypeError as e:
            print(f'string conversion failed on {ico}:\n{e}')
            return

        return ico

    @staticmethod
    def _force_full_length(ico):
        """Adds zeros before ico up to full 8-digit length, if not already

        Returns: string
        """
        #  The IČO is always eight-digit long and ARES API strictly requires it to be.
        #  However, a lot of state institutions in the Czech Republic have IČO starting with several zeros
        #  If ico parameter is acquired by a user input, it would be cumbersome for user to write them all manually
        #  So we want to allow the user to skip those zeros, writing only the positive numbers that follow

        length_insufficient = AresApiClient.ICO_LENGTH - len(ico)

        if length_insufficient:
            ico = length_insufficient * "0" + ico

        return ico
