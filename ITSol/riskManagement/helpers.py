import logging

logger = logging.getLogger("logger")

def log_info(request, message):
    user_id = request.session["id"]
    privileges = request.session["privileges"]
    logger.info(f"USER_INFO : [ id: {user_id}, privileges: {privileges} ] - {message}")
