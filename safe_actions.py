def dprint(str_to_print, priority_level=1, preprint="", hashtag_display=True):
    from configuration import APP_CONFIG
    if APP_CONFIG.DEBUG and APP_CONFIG.PRIORITY_DEBUG_LEVEL >= priority_level:
        str_ident = "".join("-" for _ in range(priority_level))
        if hashtag_display:
            print(f"{preprint}#{str_ident} {str_to_print}")
        else:
            print(f"{preprint}{str_to_print}")