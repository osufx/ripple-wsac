"""Packets sent by the client"""
cli_identify			= "identify"
cli_subscribe			= "subscribe_scores"
cli_subscribe_mp		= "subscribe_mp_complete_match"
cli_show_restrict		= "set_restricted_visibility"
cli_ping				= "ping"



"""Packets recieved from the server"""
srv_connected			= "connected"
srv_identify			= "identified"
srv_subscribe			= "subscribed_to_scores"
srv_subscribe_mp		= "subscribed_mp_complete_match"
srv_new_match			= "new_completed_match"
srv_show_restrict		= "restricted_visibility_set"
srv_score				= "new_score"
srv_pong				= "pong"
# Errors
srv_invalid_type		= "invalid_message_type",
srv_error				= "unexpected_error",
srv_not_found			= "not_found"