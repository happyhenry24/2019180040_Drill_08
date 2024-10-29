from sdl2 import SDLK_SPACE, SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'

def a_key_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

class StateMachine:
    def __init__(self, o):
        self.o = o
        self.event_q = []

    def update(self):
        self.cur_state.do(self.o)
        if self.event_q:
            e = self.event_q.pop(0)
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e):
                    self.cur_state.exit(self.o)
                    print(f'EXIT from {self.cur_state}')
                    self.cur_state = next_state
                    self.cur_state.enter(self.o)
                    print(f'ENTER into {next_state}')
                    return

    def start(self, start_state):
        self.cur_state = start_state
        self.cur_state.enter(self.o)
        print(f'ENTER into {self.cur_state}')

    def draw(self):
        self.cur_state.draw(self.o)

    def set_transitions(self, transitions):
        self.transitions = transitions

    def add_event(self, e):
        self.event_q.append(e)
        print(f'    DEBUG: new event {e} is added')
