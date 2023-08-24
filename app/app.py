
import snowflake.connector
import pandas as pd
import sys

def handler(event, context):
    print('Hello from AWS Lambda using Python' + sys.version + '!')
    #return 'Hello from AWS Lambda using Python' + sys.version + '!'
    return