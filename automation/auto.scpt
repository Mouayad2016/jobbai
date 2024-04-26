tell application "System Events"
    keystroke "G" using {shift down, command down}  -- Open the 'Go to Folder' dialog
    delay 1  -- Wait for the dialog to appear
    keystroke "/Users/mouayadmouayad/Documents/"  -- Type the path to the directory
    delay 1  -- Allow time for the path to be typed
    keystroke return  -- Navigate to the directory
    delay 1  -- Wait for navigation
    keystroke "Arbetsgivarintyg.pdf"  -- Type the name of the file
    delay 1  -- Allow time for the filename to be typed
    keystroke return  -- Open or select the file
end tell
