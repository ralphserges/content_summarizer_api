from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from custom_exceptions import InvalidArgumentError, MissingArgumentError
from summary_util import SummaryUtil

import yaml
import logging
from logging.config import dictConfig


with open('./logs/log_config.yaml', 'r') as log_config_file:
    log_config = yaml.safe_load(log_config_file)
    dictConfig(log_config)

logger = logging.getLogger(__name__)

lza_summarizer_app = Flask(__name__)
api = Api(lza_summarizer_app)

class LzaSummarizer(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
                          
        self.reqparse.add_argument('content',
                                    type=str,
                                    location='json')

        super(LzaSummarizer, self).__init__()
    

    # if user perform a get request to this endpoint
    def post(self):

        logger.info('server has received a rest api request from client.')
        args = self.reqparse.parse_args() 
        
        if args['content'] is None:
            logger.error('no json argument found.')
            raise MissingArgumentError(description='Field missing in Json Body. Check documentation for required JSON.')

        else:
            
            received_content = args['content']
            if len(received_content) < 280:

                logger.error('content received is too short for summary.')
                raise InvalidArgumentError(description='content received is too short for summary. Must be greater than 280 char.')

            else:
                logger.info('prepare to start summarization')
                summarizer = SummaryUtil()
                
                final_summary = summarizer.start_summarization(received_content,0.15)
                logger.info('summarizing....')

                logger.info('content has been summarized and responded to client.')
                return jsonify(summarized_content=final_summary)
           


api.add_resource(LzaSummarizer,'/lza-projects/summaries')


if __name__ == '__main__':
    logger.info('application is started.')
    lza_summarizer_app.run()
