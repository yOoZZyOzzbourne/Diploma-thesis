from dash import Input, Output, State, callback, no_update, ctx
from flask import session

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "parking2024"


def register():

    # Open modal — only triggered by login-open-btn (visitor-only component)
    @callback(
        Output("modal-open", "data"),
        Output("login-error", "children", allow_duplicate=True),
        Input("login-open-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def open_modal(n_clicks):
        if (n_clicks or 0) > 0:
            return True, ""
        return no_update, no_update

    # Close modal — triggered by cancel or successful submit (both always in DOM inside modal)
    @callback(
        Output("modal-open", "data", allow_duplicate=True),
        Input("login-cancel-btn", "n_clicks"),
        Input("login-submit-btn", "n_clicks"),
        State("login-username", "value"),
        State("login-password", "value"),
        prevent_initial_call=True,
    )
    def close_modal(cancel_clicks, submit_clicks, username, password):
        trigger = ctx.triggered_id
        if trigger == "login-cancel-btn" and (cancel_clicks or 0) > 0:
            return False
        if trigger == "login-submit-btn" and (submit_clicks or 0) > 0:
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                return False
        return no_update

    # Handle login submit — updates auth-store and error message
    @callback(
        Output("auth-store", "data"),
        Output("login-error", "children"),
        Input("login-submit-btn", "n_clicks"),
        State("login-username", "value"),
        State("login-password", "value"),
        prevent_initial_call=True,
    )
    def handle_login(n_clicks, username, password):
        if not n_clicks:
            return no_update, no_update
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["role"] = "admin"
            return {"role": "admin"}, ""
        return no_update, "Nesprávné přihlašovací údaje."

    # Handle logout — separate callback, logout-btn only exists when admin
    @callback(
        Output("auth-store", "data", allow_duplicate=True),
        Input("logout-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def handle_logout(n_clicks):
        if not n_clicks:
            return no_update
        session.pop("role", None)
        return {"role": "visitor"}

    # Modal visibility driven purely by store
    @callback(
        Output("login-modal", "style"),
        Input("modal-open", "data"),
    )
    def set_modal_visibility(is_open):
        return {"display": "flex"} if is_open else {"display": "none"}
