import xbmcgui # type: ignore
import xbmcaddon # type: ignore

my_addon = xbmcaddon.Addon()


def dialog_handler(setting_key, 
                   prompt_text, 
                   notification_title) -> str:

    dialog = xbmcgui.Dialog()
    prompt = dialog.input(prompt_text, type=xbmcgui.INPUT_ALPHANUM)
    if prompt:
        my_addon.setSetting(setting_key, prompt)
        dialog.notification(f'{notification_title} Saved', f'Your {notification_title} has been saved successfully!', xbmcgui.NOTIFICATION_INFO, 5000)
    else:
        dialog.notification(f'No {notification_title} Entered', f'{notification_title} was not saved.', xbmcgui.NOTIFICATION_ERROR, 5000)

    return prompt    

def dialog_notify(notification_title,
                  code):
    
    dialog = xbmcgui.Dialog()
    dialog.notification(f'The {notification_title} was successfully retrieved.', f'Your {notification_title} is {code}', xbmcgui.NOTIFICATION_INFO, 5000)