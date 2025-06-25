import cv2

class VirtualButtons:
    def __init__(self, frame, landmarks=None, button_configs=None):
        self.frame = frame
        self.landmarks = landmarks or []
        self.buttons = []
        
        default_configs = [
            {'pos': (100, 100), 'label': 'Button 1', 'radius': 30, 'action': lambda: print("Button 1 pressed")},
            {'pos': (300, 100), 'label': 'Button 2', 'radius': 30, 'action': lambda: print("Button 2 pressed")}
        ]
        
        self.button_configs = button_configs or default_configs
        self.setup_buttons()
        
    def setup_buttons(self):
        for config in self.button_configs:
            self.buttons.append({
                'pos': config['pos'],
                'label': config['label'],
                'radius': config.get('radius', 30),
                'color': (0, 255, 0),
                'active_color': (255, 0, 0),
                'action': config.get('action', lambda: None),
                'pressed': False
            })
    
    def draw_buttons(self):
        for button in self.buttons:
            cv2.circle(self.frame, button['pos'], button['radius'], button['color'], -1)
            cv2.putText(self.frame, button['label'], 
                       (button['pos'][0] - len(button['label'])*5, button['pos'][1] + 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        return self.frame
    
    def check_button_presses(self, finger_tip_index=8):
        if not self.landmarks or len(self.landmarks) <= finger_tip_index:
            return False
        
        finger_x, finger_y = self.landmarks[finger_tip_index]
        any_pressed = False
        
        for button in self.buttons:
            btn_x, btn_y = button['pos']
            distance = ((finger_x - btn_x)**2 + (finger_y - btn_y)**2)**0.5
            
            if distance < button['radius']:
                button['color'] = button['active_color']
                if not button['pressed']:
                    button['action']()
                    button['pressed'] = True
                any_pressed = True
            else:
                button['color'] = (0, 255, 0)
                button['pressed'] = False
                
        return any_pressed
    
    def add_button(self, pos, label, action=None, radius=30):
        self.buttons.append({
            'pos': pos,
            'label': label,
            'radius': radius,
            'color': (0, 255, 0),
            'active_color': (255, 0, 0),
            'action': action or (lambda: print(f"{label} pressed")),
            'pressed': False
        })
    
    def clear_buttons(self):
        self.buttons = []