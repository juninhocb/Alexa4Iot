import logging
import ask_sdk_core.utils as ask_utils
import requests
import json

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Bem vindo a skill AIOTI FOR ROME, por aqui você pode ligar, desligar dispositivos, então no que posso te ajudar? "

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class TriggerDeviceIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        
        return ask_utils.is_intent_name("TriggerDeviceIntent")(handler_input)

    def handle(self, handler_input):
        
        url = "<your_public_address>"
        url2 = "<your_public_address>"
        slots = handler_input.request_envelope.request.intent.slots
        device = slots['deviceType'].resolutions.resolutions_per_authority[0].values[0].value.name
        identity = slots['noDevice'].value
        stats = requests.get(url2 +device+""+identity)
        if (stats.status_code == 200):
            estado = stats.json()['Estado']
            conn = stats.json()['Conexão']
            print(stats.json())
            
            if (estado == True):
                speak_output = "Dispositivo " + device + identity + "já está conectado!!!"
            
            else:
                try: 
                    requests.post(url+device+""+identity)
                    speak_output = "Acionando dispositivo " + device+identity
                except: 
                    print("deu ruim")
                    speak_output = "Falha de comunicação com os servidores"
        else:
            speak_output = "Dispositivo " + device + identity + " está desconectado"
            
                    
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class DeactivateDeviceIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        
        return ask_utils.is_intent_name("DeactivateDeviceIntent")(handler_input)

    def handle(self, handler_input):
        
        url = "<your_public_address>"
        url2 = "<your_public_address>"
        slots = handler_input.request_envelope.request.intent.slots
        device = slots['deviceName'].resolutions.resolutions_per_authority[0].values[0].value.name
        identity = slots['noDevice'].value
        stats = requests.get(url2 +device+""+identity)
        if (stats.status_code == 200):
            estado = stats.json()['Estado']
            conn = stats.json()['Conexão']
            print(stats.json())
            
            if (estado == False):
                speak_output = "Dispositivo " + device + identity + "já está desligado!!!"
            
            else:
                try: 
                    requests.post(url+device+""+identity)
                    speak_output = "Desligando dispositivo " + device+identity
                except: 
                    print("deu ruim")
                    speak_output = "Falha de comunicação com os servidores"
        else:
            speak_output = "Dispositivo " + device + identity + " está desconectado"
            
                    
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "você pode acionar um dispositivo, dizendo acionar ou desligar dizendo desligar"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Adeus!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Não entendi o que disse, você pode acionar, desligar ou pedir ajuda!"
        reprompt = "Não entendi o que disse, como posso te ajudar?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "Voçe acionou a intenet " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Tive um problema tentando fazer o que me disse, talvez seja falha de conexão!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(TriggerDeviceIntentHandler())
sb.add_request_handler(DeactivateDeviceIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()