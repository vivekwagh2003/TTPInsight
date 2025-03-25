from nltk.parse.corenlp import CoreNLPServer
from pycorenlp import StanfordCoreNLP
import requests, os

class StanfordServer():
    def __init__(self, JAVA_HOME, DOWNLOAD_HOME, STANFORD_HOME, STANFORD_SERVER):
        """
        Initializes paths for Java, download location, Stanford CoreNLP directory, and the server URL.
        """
        self.JAVA_HOME = JAVA_HOME
        self.DOWNLOAD_HOME = DOWNLOAD_HOME
        self.STANFORD_HOME = STANFORD_HOME
        self.STANFORD_SERVER = STANFORD_SERVER

    def start_core_nlp_server(self):
        """
        Starts the Stanford CoreNLP server if it's not running.
        """
        os.environ['JAVAHOME'] = self.JAVA_HOME # Set Java environment variable
        HOMEDIR = os.path.expanduser("~") # Get the home directory
        DOWNLOAD_HOME = os.path.join(HOMEDIR, self.DOWNLOAD_HOME) # Path to downloaded CoreNLP files
        STANFORD_HOME = os.path.join(DOWNLOAD_HOME, self.STANFORD_HOME) # Path to CoreNLP folder

        print('Stanford_Directory: ', STANFORD_HOME)

        # # The server needs to know the location of the following files:
        # #   - stanford-corenlp-X.X.X.jar
        # #   - stanford-corenlp-X.X.X-models.jar
        # # Create the server
        server = CoreNLPServer(
            os.path.join(STANFORD_HOME, "stanford-corenlp-3.9.2-models.jar"), # Models jar file
            os.path.join(STANFORD_HOME, "stanford-corenlp-3.9.2.jar"), # Main CoreNLP jar file
            os.path.join(STANFORD_HOME, "stanford-english-corenlp-2018-10-05-models.jar"), # English models
        )
        # # Start the server in the background
        server.start()
        print("Server Started")

    def startServer(self):
        """
        Checks if the CoreNLP server is running; if not, starts it.
        Returns an instance of the StanfordCoreNLP client.
        """
        try:
            response = requests.get(self.STANFORD_SERVER) # Try connecting to the server
        except requests.exceptions.ConnectionError:
            print('ConnectionError') # If server isn't running, start it
            self.start_core_nlp_server()
        return StanfordCoreNLP(self.STANFORD_SERVER)  # Return the CoreNLP client


if __name__=='__main__':
     # Set paths based on OS type (Windows or Linux)
    if os.name == 'nt':
        JAVA_HOME = 'C:\\Program Files\\Java\\jdk1.8.0_201\\bin\\java.exe'
        DOWNLOAD_HOME = 'Downloads'
        STANFORD_HOME = 'stanford-corenlp-full-2018-10-05'
    else:
        JAVA_HOME = '/usr/lib/jvm/java-8-oracle/'
        DOWNLOAD_HOME = 'ttp_sense_python'
        STANFORD_HOME = 'lib'
    STANFORD_SERVER = 'http://localhost:9000' # CoreNLP server URL
    # Initialize and start the Stanford NLP server
    model_STANFORD = StanfordServer(JAVA_HOME, DOWNLOAD_HOME, STANFORD_HOME, STANFORD_SERVER).startServer()