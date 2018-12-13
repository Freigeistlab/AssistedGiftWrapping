from statemachine import StateMachine, State, exceptions
import time
from threading import Thread

from LightPad import LightPad
from SizeCalculator import SizeCalculator


class Orchestrator(StateMachine):
    print("Started orchestrator")

    # states
    idle = State('Idle', initial=True)
    start = State('Start')
    sizeCalculated = State('SizeCalculated')
    paperPrepared = State('PaperPrepared')
    paperLaidOut = State('PaperLaidOut')
    giftPlaced = State('GiftProjected')
    giftWrapped = State('GiftWrapped')

    # actions
    lightpad1_darkened = idle.to(start) # when gift was placed on lightpad 1 (in the corner)
    lightpad1_lightened_up = start.to(idle) # when gift was removed from corner
    finished_size_calc = start.to(sizeCalculated) # when size was calculated continue with preparing paper
    finished_paper_prep = sizeCalculated.to(paperPrepared) | paperLaidOut.to(paperPrepared) # paper is prepared. now project the paper on the table
    lightpad2_darkened_little = paperPrepared.to(paperLaidOut) | giftPlaced.to(paperLaidOut) # paper is laid out (lightpad2 is semi-bright). now project the gift on top of the paper
    lightpad2_darkened_completely = paperLaidOut.to(giftPlaced) # paper is laid out. now project the gift on top of the paper

    def __init__(self):
        super().__init__()
        # bluetooth_handler = BluetoothHandler()
        # ws = WebSocket(self.)
        lightpad1 = LightPad(self.handle_lightpad_change, 1)
        lightpad2 = LightPad(self.handle_lightpad_change, 2)
        lightpad1.start()
        lightpad2.start()
        # motorDriver = MotorDriver()
        self.sizeCalculator = SizeCalculator(self.finished_size_calc)
        #obj = OrchestratorState(state="idle")

    def on_enter_start(self):
        print('Measuring distance now! bsss bssss ')
        self.sizeCalculator.start()

    def on_enter_idle(self):
        print('Object was removed from top left corner')

    def on_enter_sizeCalculated(self):
        print('Size calculated')
        # sleep for 3 s again

        # self.motorDriver.give_paper(self.width, self.height, self.depth)
        #self.finished_paper_prep()

    def on_enter_paperPrepared(self):
        print('Finished paper prep!')
        # project paper onto the table now
        # send message to ws to render paper projection

    def on_enter_paperLaidOut(self):
        print('Project the gift onto the paper')
        # project gift onto the paper now
        # send message to ws to render gift projection

    def on_enter_giftPlaced(self):
        print('Project the arrows onto the paper')
        # project arrows onto the paper now
        # send message to ws to render arrow projection

    def on_enter_giftWrapped(self):
        print('gift was placed')
        # project arrows onto the paper now
        # send message to ws to render arrow projection

    def handle_lightpad_change(self, id, value):
        try:
            if value < 5:
                if id == 1:
                    self.lightpad1_darkened()
                elif id == 2:
                    self.lightpad2_darkened_completely()
            elif 5 <= value < 25:
                if id == 2:
                    self.lightpad2_darkened_little()
            else:
                if id == 1:
                    self.lightpad1_lightened_up()
                elif id == 2:
                    self.finished_paper_prep()
        except exceptions.TransitionNotAllowed:
            print("Transition not allowed")
            print(self.current_state)

orchestrator = Orchestrator()