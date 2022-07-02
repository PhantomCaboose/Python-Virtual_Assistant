###########################################################
#------------------------ IMPORTS ------------------------#
###########################################################
import wolframalpha

###########################################################
#----------------------- FUNCTIONS -----------------------#
###########################################################
def get_wolfram(query):
    app_ID = "WGQ4LW-L393U87VW5"
    client = wolframalpha.Client(app_ID)
    request = client.query(query)
    try:
        response = next(request.results).text
        return response
    except:
        return"I am unable to find the answer."

def calculate(query):
    query = query.replace('calculate ', '')

    if "plus" in query:
        total = query.replace('plus', '+')
    elif "minus" in query:
        total = query.replace('minus', '-')
    elif "multiply" in query and "by" in query:
        total = query.split('multiply ')[1].rstrip().replace('by', '*')
    elif "multiply" in query and "times" in query:
        total = query.split('multiply ')[1].rstrip().replace('times', '*')
    elif "multiplied by" in query:
        total = query.replace('multiplied by', '*')
    elif "times" in query:
        total = query.replace('times', '*')
    elif "divide" in query and "by" in query and "divided by" not in query:
        total = query.split('divide ')[1].rstrip().replace('by', '/')
    elif "divided by" in query:
        total = query.replace('divided by ', '/')
    elif "/" in query:
        total = query
    elif "*" in query:
        total = query
    elif "+" in query:
        total = query
    elif "-" in query:
        total = query

    try:
        result = get_wolfram(total)
        if '/' in query:
            query = query.replace('/', 'divided by ')
        elif '*' in query:
            query = query.replace('*', 'multiplied by')
        elif '+' in query:
            query = query.replace('+', 'plus')
        elif '-' in query:
            query = query.replace('-', 'minus')
        elif "multiply" in query:
            query = query.replace('multiply', 'multiplying')
        elif "divide" in query and "divided by" not in query:
            query = query.replace('divide', 'divided by ')
        elif "divided by" in query:
            query = query
        return f"The result of {query} is {result}"
    except:
        return "I am unable to calculate the result."
