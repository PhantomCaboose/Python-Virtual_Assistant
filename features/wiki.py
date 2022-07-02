###########################################################
#------------------------ IMPORTS ------------------------#
###########################################################
import wikipedia
import warnings

warnings.catch_warnings()
warnings.simplefilter("ignore")
###########################################################
#----------------------- FUNCTIONS -----------------------#
###########################################################
def search_wikipedia(query):
    try:
        if "what is a" in query:
            query = query.replace("what is a", "")
        elif "what is" in query:
            query = query.replace("what is", "")
        elif "what are" in query:
            query = query.replace("what are", "")
        elif "who is" in query:
            query = query.replace("who is", "")
        elif "who was" in query:
            query = query.replace("who was", "")
        result = wikipedia.summary(query, sentences = 2)
        return result
    except wikipedia.WikipediaException:
        return "No records found."
