try:
    import pygame # using this for audio
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=1024) # buffer must be power of 2, higher means less choppy audio but a longer time to start
    initiallised = True
except Exception:
    initiallised = False
muted = False

def setMute(val):
    muted = val

if initiallised:
    sounds = {
              'select'     : pygame.mixer.Sound(file='sounds/rollover.wav'),
              'add'        : pygame.mixer.Sound(file='sounds/increment.wav'),
              'config'     : pygame.mixer.Sound(file='sounds/reconfig.wav'),
              'subtract'   : pygame.mixer.Sound(file='sounds/decrement.wav'),
              'connect'    : pygame.mixer.Sound(file='sounds/connection_made.wav'),
              'disconnect' : pygame.mixer.Sound(file='sounds/connection_destroyed.wav'),
              'expand'     : pygame.mixer.Sound(file='sounds/extrude.wav'),
              'delete'     : pygame.mixer.Sound(file='sounds/collapse.wav'),
              'error'     : pygame.mixer.Sound(file='sounds/error.wav'),
              'contract'   : pygame.mixer.Sound(file='sounds/carve.wav'),
              'raise_1'   : pygame.mixer.Sound(file='sounds/panel_raise_01.wav'),
              'raise_2'   : pygame.mixer.Sound(file='sounds/panel_raise_02.wav'),
              'raise_3'   : pygame.mixer.Sound(file='sounds/panel_raise_03.wav'),
              'lower_1'   : pygame.mixer.Sound(file='sounds/panel_lower_01.wav'),
              'lower_2'   : pygame.mixer.Sound(file='sounds/panel_lower_02.wav'),
              'lower_3'   : pygame.mixer.Sound(file='sounds/panel_lower_03.wav'),
              'move'      : pygame.mixer.Sound(file='sounds/reconfig.wav'),
              'swap'      : pygame.mixer.Sound(file='sounds/extrude.wav'),
             }
         
    def fx(name, e=None):
        """Play a sound effect stored in the sounds{} dict."""
        # If we ever want to use a different library for sounds, just edit this, all sound calls should route through here.
        if not muted and name in sounds:
            sounds[name].play()
else:
    def fx(name, e=None):
        '''Pygame has failed to initialise, we just won't play any sounds!'''
        pass