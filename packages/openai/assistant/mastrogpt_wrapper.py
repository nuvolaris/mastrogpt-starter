
def Response(of_bot: str, with_title: str = "", custom_display_data: dict = {}, with_state: dict = {}):
    return {"body": {
        "output": of_bot,
        "title": with_title,
        **custom_display_data,
        "state": with_state
    }}




    

