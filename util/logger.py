import datetime

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def colorise(color, text):
        
        """
        Colors/styles a given text in a given color.
        """

        return color + text + colors.ENDC

class Logger:

    """
    Used to log events of a type at a location with a message. <br>
    Colorcodes different logs for easy readability.
    """

    @staticmethod
    def __construct_log(logtype:str, location:str, message:str):
        current_time = datetime.datetime.now()
        date = current_time.date()
        time = f"{current_time.hour}:{current_time.minute if current_time.minute >9 else f"0{current_time.minute}"}"
        print(f"{date}|{time} - {logtype} @ {location}: {message}")

    def load(location:str, message:str):
        __class__.__construct_log(colorise(colors.OKBLUE, "LOADING"), location=location, message=message)

    def success(location:str, message:str):
        __class__.__construct_log(colorise(colors.OKGREEN, "SUCCESS"), location=location, message=message)

    def error(location:str, message:str, error_message:str=""):
        __class__.__construct_log(colorise(colors.FAIL, "ERROR"), location=location, message=(message + "\n" + (f" => {error_message}" if error_message!="" else "")))

    def failure(location:str, message:str):
        __class__.__construct_log(colorise(colors.WARNING, "FAILURE"), location=location, message=message)

    def request(location:str, message:str, reqtype:str=""):
        __class__.__construct_log(colorise(colors.HEADER, "REQUEST") + (f" => {reqtype}" if reqtype!="" else ""), location=location, message=message)

    def log(location:str, message:str):
        __class__.__construct_log("INFO", location=location, message=message)