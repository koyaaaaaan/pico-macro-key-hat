# True:use lock pin 
# False:lock screen skipped
uselock = True

# lock pin(array) 
# (Should be Upper Letters)
lockpin = ["A","B","X","Y"]

# Key board Layout Type
# en:US key layout 
# jp:Japanese key layout
layoutType = "jp"

# data > Displayand key config (array 4 fixed)
#  > Display
#   value > String value it send to PC when it pressed 
keymap = [
           { # Stick Center
             "data": [
               { "label": "Custom CA", "value": "Key Input C valueA" },
               { "label": "Custom CB", "value": "Key Input C valueB" },
               { "label": "Custom CX", "value": "Key Input C valueX" },
               { "label": "Custom CY", "value": "Key Input C valueY" }	
             ]
           },
           { # Stick Up 
             "data": [
               { "label": "Custom UA", "value": "Key Input U valueA" },
               { "label": "Custom UB", "value": "Key Input U valueB" },
               { "label": "Custom UX", "value": "Key Input U valueX" },
               { "label": "Custom UY", "value": "Key Input U valueY" }		
             ]
           },
           { # Stick Down
             "data": [
               { "label": "Custom DA", "value": "Key Input D valueA" },
               { "label": "Custom DB", "value": "Key Input D valueB" },
               { "label": "Custom DX", "value": "Key Input D valueX" },
               { "label": "Custom DY", "value": "Key Input D valueY" }
             ]
           },
           { # Stick Left
             "data": [
               { "label": "Custom LA", "value": "Key Input L valueA" },
               { "label": "Custom LB", "value": "Key Input L valueB" },
               { "label": "Custom LX", "value": "Key Input L valueX" },
               { "label": "Custom LY", "value": "Key Input L valueY" }	
             ]
           },
           { # Stick Right
             "data": [
               { "label": "Custom RA", "value": "Key Input R valueA" },
               { "label": "Custom RB", "value": "Key Input R valueB" },
               { "label": "Custom RX", "value": "Key Input R valueX" },
               { "label": "Custom RY", "value": "Key Input R valueY" }	
             ]
           }
]

