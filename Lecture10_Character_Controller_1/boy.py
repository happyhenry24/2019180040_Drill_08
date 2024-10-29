from pico2d import load_image, get_time, SDLK_LEFT, SDLK_RIGHT
from state_machine import StateMachine, space_down, time_out, right_down, left_down, left_up, right_up, a_key_down

class Idle:
    @staticmethod
    def enter(boy):
        boy.start_time = get_time()
        boy.dir = 0
        boy.action = 3

    @staticmethod
    def exit(boy):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, 300, 100, 100, boy.x, boy.y)

class Sleep:
    @staticmethod
    def enter(boy):
        pass

    @staticmethod
    def exit(boy):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(
            boy.frame * 100, 300, 100, 100,
            3.141592 / 2, '',
            boy.x - 25, boy.y - 25, 100, 100
        )

class Run:
    @staticmethod
    def enter(boy):
        boy.action = 1 if boy.dir == 1 else 0
        boy.frame = 0

    @staticmethod
    def exit(boy):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 5

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_draw(boy.frame * 100, 0, 100, 100, boy.x, boy.y)

class AutoRun:
    @staticmethod
    def enter(boy):
        boy.start_time = get_time()
        boy.last_input_time = get_time()
        boy.dir = 1
        boy.action = 1
        boy.frame = 0
        boy.scale = 2.0

    @staticmethod
    def exit(boy):
        boy.scale = 1.0

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 10
        if boy.x > 800 or boy.x < 0:
            boy.dir *= -1
            boy.action = 1 if boy.dir == 1 else 0
        # 5초 동안 입력이 없으면 Idle 상태로 전환
        if get_time() - boy.last_input_time > 5.0:
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(
                boy.frame * 100, boy.action * 100, 100, 100,
                boy.x, boy.y, 100 * boy.scale, 100 * boy.scale
            )
        else:
            boy.image.clip_draw(
                boy.frame * 100, 0, 100, 100,
                boy.x, boy.y, 100 * boy.scale, 100 * boy.scale
            )

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.scale = 1.0
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, a_key_down: AutoRun},
                Run: {right_up: Idle, left_up: Idle},
                AutoRun: {time_out: Idle, right_down: Run, left_down: Run, right_up: Run, left_up: Run},
                Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        if self.state_machine.cur_state == AutoRun:
            self.last_input_time = get_time()
        if event.key == SDLK_LEFT:
            self.dir = -1
        elif event.key == SDLK_RIGHT:
            self.dir = 1
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
