import requests
import string


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
        Usually, the whole name, IČO and full address are required to identify the subject reliably

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
        """Subjects the ico to a series of test. Modifies the ico, if needed, to be suited for ARES API

        Returns: string ico (or None if any of the test fails)
        """
        tests = [AresApiClient._force_string,       # Parses ico to a string, if not already
                 AresApiClient._check_if_is_digit,  # str.isdigit() alone won't do - we need ico returned, not boolean
                 AresApiClient._check_exceeding_allowed_length,  # not allow anything beyond 8-digit long
                 AresApiClient._force_full_length,]  # not allow anything below 8-digit, add zeros before if needed

        for test in tests:  # let's run the tests
            ico = test(ico)  # we allow ico to be repeatedly tested and modified until we are satisfied with it
            if not ico:  # should any of the tests fail,
                return  # None is returned immediately

        return ico  # in case all test passed, the (potentially modified) ico is returned

    @staticmethod
    def _force_string(ico):
        """Parses ico to a string, if not already

        Returns ico as string (or None if the string conversion fails)
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

        Returns: ico as string
        """
        #  The IČO is always eight-digit long and ARES API strictly requires it to be, otherwise it won't work.
        #  However, a lot of state institutions in the Czech Republic have IČO starting with several zeros
        #  If ico parameter is acquired by a user input, it would be cumbersome for user to write them all manually
        #  So we want to allow the user to skip those zeros, writing only the positive numbers that follow

        length_insufficient = AresApiClient.ICO_LENGTH - len(ico)

        if length_insufficient:
            ico = length_insufficient * "0" + ico

        return ico

    @staticmethod
    def _check_if_is_digit(ico):
        """Checks whether passed ico is made up purely form digits characters.
        This increases the security and typo prevention.

        Return:
            intact ico (or None if isdigit() test fails
        """
        if ico.isdigit():
            return ico

    @staticmethod
    def _check_exceeding_allowed_length(ico):
        """Checks whether passed ico exceeds the allowed length

        Return:
            intact ico (or None if allowed length is exceeded)
        """
        if len(ico) <= AresApiClient.ICO_LENGTH:
            return ico


class AresApiClientManager:
    """Serves for user interaction with the AresApiClient class

    AresApiClient class itself can be used to retrieve the data about the economic subject from ARES public register.
    It does not need any user interaction for this, if IČO parameter is passed by other parts of your program.
    However, with this manager, AresApiClient can be used to interact with the user through CLI
    """

    @staticmethod
    def interact():
        """Prompts user to enter IČO. Returns the formal description of a subject based on ARES data.

        Method works in cycle, so as many consecutive IČO can be entered as needed.
        This is useful if you are iterating through a long list of subjects.
        Imagine the insolvency administrator preparing a draft of distribution table for payments to creditors
        """

        print('\nWelcome to the interactive mode of AresApiClient!\n')
        print(("Fill in the IČO of any economic subject in the Czech Republic.\n"
               "(or keep blank and press ENTER to quit)\n"))

        quit_by = {"", "q", 0, "quit", "quit()", "exit", "exit()", "abort", "abort()", }
        prompt = "\nfill in the IČO: "  # IČO may be a string or an integer, both is accepted
        user_input = True  # default input is True to start the cycle

        while user_input:

            # acquiring the input
            user_input = input(prompt)
            user_input = ''.join(char for char in user_input if char not in string.whitespace)  # removing whitespaces
            # user_input = user_input.replace(" ", "")

            # if user wants to quit
            if user_input.lower() in quit_by:  # any of the quiting phrase
                print('\nGoodbye!\n')
                break  # will end the cycle immediately

            arg_ico = user_input
            result = AresApiClient.get_subject_formal_description(arg_ico)

            if result:
                print(result)  # and print it
            else:
                print(f'Request to retrieve data from ARES based on IČO: {arg_ico} was not succesful.')
                print("Please double-check typos in IČO and your internet connection.")


if __name__ == "__main__":
    AresApiClientManager.interact()
