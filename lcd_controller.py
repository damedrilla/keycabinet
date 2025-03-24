import I2C_LCD_driver
import time
mylcd = I2C_LCD_driver.lcd()

defaultState = True
displayMainMenu = False
displaySelectKey = False
displayNeedHDMI = False
displayScanID = False
def lcdScreenController():
    while True:
        if defaultState:
            mylcd.lcd_clear()
            mylcd.lcd_display_string("CCS KeyCabinet", 1)
            mylcd.lcd_display_string("Press 1 to use", 2)
        elif displayMainMenu:
            mylcd.lcd_clear()
            mylcd.lcd_display_string("1. Borrow", 1)
            
            mylcd.lcd_display_string("2. Return", 2)
        elif displaySelectKey:
            mylcd.lcd_clear()
            mylcd.lcd_display_string("Type the number", 1)
            
            mylcd.lcd_display_string("of the key", 2)
        elif displayScanID:
            mylcd.lcd_clear()
            mylcd.lcd_display_string("Scan your ID", 1)
            
            mylcd.lcd_display_string("to continue...", 2)
        elif displayNeedHDMI:
            mylcd.lcd_clear()
            mylcd.lcd_display_string("Need HDMI?", 1)
            
            mylcd.lcd_display_string("1. Yes   2. No", 2)
        time.sleep(.7)
            
def set_active_state(active_state):
    """
    Sets all state variables to False except the specified active state.
    
    Args:
        active_state (str): The name of the state variable to set to True.
    """
    global defaultState, displayMainMenu, displaySelectKey, displayNeedHDMI, displayScanID
    
    # Reset all states to False
    defaultState = False
    displayMainMenu = False
    displaySelectKey = False
    displayNeedHDMI = False
    displayScanID = False
    
    # Set the specified state to True
    if active_state == "defaultState":
        defaultState = True
    elif active_state == "displayMainMenu":
        displayMainMenu = True
    elif active_state == "displaySelectKey":
        displaySelectKey = True
    elif active_state == "displayNeedHDMI":
        displayNeedHDMI = True
    elif active_state == "displayScanID":
        displayScanID = True
    else:
        raise ValueError(f"Invalid state: {active_state}")