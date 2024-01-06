import requests


class AresManager:
    """Retrieves and manipulates data from Czech Republics ARES register

    The retrievement is based on unique ID number each company in Czech republic has called "IČO"
    ICO is used to return subjects data from the register.
    These data can be further

    Methods:
        get_subject_by_ico: This is the core method of the whole class. It returns subject data based on a given ICO
        get_subject_formal_description: Retu
    """

    def __init__(self):
        self.ICO_LENGTH = 8  # ICO in the Czech Republic is always eight-digit
        self.ARES_REQUEST_URL = "https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/"

    def get_subject_by_ico(self, ico):
        """Returns subject data as dictionary from ARES register

        Looks up subject by its unique ID number (IČO) IN ARES register REST Api endpoint
        Returns subject data as dictionary (with some nested dictionaries)

        The ICO is always eight-digit. If less digits are passed, zeros are added before
        This is because lot of state institutions have ICO starting with several zeros
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
            string_ico = str(ico)  # we force ico argument to be string even if passed as number
        except TypeError as e:
            print(f'string conversion failed on {ico}: {e}')
            return

        # if less than 8 digits were passed, the length is insufficient
        length_insufficient = self.ICO_LENGTH - len(string_ico)

        if length_insufficient:  # zeros will be added before ico up to required length
            string_ico = length_insufficient * "0" + string_ico  # this allows

        response = requests.get(self.ARES_REQUEST_URL + string_ico)

        if response.status_code != 200:
            # if request is not successfull, None is returned.
            return

        data = response.json()
        return data

    def get_subject_formal_description(self, ico):
        """Returns subject data in a way expected in formal human communication

        Looks up subject by its unique ID number (IČO) IN ARES register
        Returns some of its data that are considered to be descriptive enough
        These are given by a Czech laws (based on circumstances) or simply by common conventions
        If subject is not successfully found, None is returned

        Args:
            ico (string or int): the unique ID number used to look up the subject in the ARES register

        Returns:
            string or None

        """
        data = self.get_subject_by_ico(ico)
        if data:
            return f'{data["obchodniJmeno"]}, IČO {data["ico"]}, sídlem {data["sidlo"]["textovaAdresa"]}'



ares_manager = AresManager()
print(ares_manager.get_subject_formal_description('kuřecí'))