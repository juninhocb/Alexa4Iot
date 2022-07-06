# -*- coding: utf-8 -*-

######################################################################################################################################
import logging
import ask_sdk_core.utils as ask_utils                                                                                               
from ask_sdk_core.skill_builder import SkillBuilder                                                                                  
from ask_sdk_core.dispatch_components import AbstractRequestHandler                                                                  
from ask_sdk_core.dispatch_components import AbstractExceptionHandler                                                                
from ask_sdk_core.handler_input import HandlerInput                                                                                  
from ask_sdk_model import Response
from constants import *
from components import helper 

logger = logging.getLogger(__name__)                                                                                                 
logger.setLevel(logging.INFO)
                                                                                                                                                                                                                                                         #
######################################################################################################################################



class LaunchRequestHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = WELCOME

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class ConnectDeviceIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ConnectDeviceIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = helper.connect(handler_input)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class ListConnectedIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ListConnectedIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = helper.listConnected()

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class DisconnectDeviceIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("DisconnectDeviceIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = helper.disconnect(handler_input)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FeedIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("FeedIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = helper.feed(handler_input)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = HELP

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speak_output = GOODBYE

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In FallbackIntentHandler")
        speech = DONT_UNDERSTAND
        reprompt = DONT_UNDERSTAND_REPROMPT

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = TRIGGER + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = ERROR

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

###############################################################################################################################################
sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ConnectDeviceIntentHandler())
sb.add_request_handler(ListConnectedIntentHandler())
sb.add_request_handler(DisconnectDeviceIntentHandler())
sb.add_request_handler(FeedIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())
###############################################################################################################################################

lambda_handler = sb.lambda_handler()