import sys, getopt

from statemachine import StateMachine, State, exceptions

from DeviceServer import DeviceServer
from GiftSizeCalculator import GiftSizeCalculator
from OrderHandler import OrderHandler
from PaperLengthController import PaperLengthController
from WebSocket import WebSocket
from AutoConnector import AutoConnector

class Orchestrator(StateMachine):
    print("Started orchestrator")
    fakeorder = False
    testprojections = False
    optlist, _ = getopt.getopt(sys.argv[1:], "", ["fakeorder=", "testprojections="])
    print(optlist)
    for o,a in optlist:
        if o in ["--fakeorder"]:
            fakeorder = True
        elif o in ["--testprojections"]:
            testprojections = True
        else:
            assert False, "unhandled option " + o

    devices = {}

    # states
    idle = State('Idle', initial=True)
    waitingForGift = State('WaitingForGift')
    start = State('Start')
    sizeCalculated = State('SizeCalculated')
    paperPrepared = State('PaperPrepared')
    paperLaidOut = State('PaperLaidOut')
    giftPlaced = State('GiftProjected')
    giftWrapped = State('GiftWrapped')
    firstFold = State('FirstFold')
    secondFold = State('SecondFold')

    # actions
    new_order = idle.to(waitingForGift)
    lightpad1_darkened = waitingForGift.to(start) # when gift was placed on lightpad 1 (in the corner)
    lightpad1_lightened_up = start.to(idle) # when gift was removed from corner
    finished_size_calc = start.to(sizeCalculated) # when size was calculated continue with preparing paper
    finished_paper_prep = sizeCalculated.to(paperPrepared) # paper is prepared. now project the paper on the table
    lightpad2_darkened_little = paperPrepared.to(paperLaidOut) | giftPlaced.to(paperLaidOut) # paper is laid out (lightpad2 is semi-bright). now project the gift on top of the paper
    lightpad2_lightened_up = paperLaidOut.to(paperPrepared)
    lightpad2_darkened_completely = paperLaidOut.to(giftPlaced) # paper is laid out. now project the gift on top of the paper
    finish = giftPlaced.to(idle)
    next_order = giftPlaced.to(waitingForGift)
    tape_teared = giftPlaced.to(firstFold) | firstFold.to(secondFold)

    test_projection = idle.to(paperPrepared)

    def __init__(self):
        super().__init__()
        self.autoConnector = AutoConnector()
        # blocking call
        devices = self.autoConnector.find_all_devices()

        # bluetooth_handler = BluetoothHandler()
        self.webSocket = WebSocket(self)
        self.webSocket.start()
        self.paperLengthWatcher = PaperLengthController(self.on_paper_teared)
        self.sizeCalculator = GiftSizeCalculator(self.finished_size_calc)


        #lightpad1 = LightPad(self.handle_lightpad_change, 1)
        #lightpad2 = LightPad(self.handle_lightpad_change, 2)
        #lightpad1.start()
        #lightpad2.start()
        #self.motorDriver = MotorDriver(self.finished_paper_prep)
        self.deviceServer = DeviceServer(self)
        self.deviceServer.start()

        if not self.fakeorder:
            self.orderHandler = OrderHandler(self.new_order)
            self.orderHandler.get_open_orders()
        else:
            if self.testprojections:
                self.sizeCalculator.generate_mock_values()
                self.test_projection()
            else:
                self.new_order()


    def on_enter_start(self):
        print('Measuring distance now! bsss bssss ')
        self.sizeCalculator.start()

    def on_enter_idle(self):
        print('Object was removed from top left corner')

    def on_enter_sizeCalculated(self):
        print('Size calculated - watching the paper now')
        #self.motorDriver.set_paper_length(self.sizeCalculator.paper_width)
        #self.motorDriver.start()
        self.paperLengthWatcher.set_paper_dimensions(self.sizeCalculator.paper_width,self.sizeCalculator.paper_height)

    def on_enter_paperPrepared(self):
        print('Finished paper prep!')
        # project paper onto the table now
        # send message to ws to render paper projection
        self.webSocket.send_current_state()

    def on_enter_paperLaidOut(self):
        print('Project the gift onto the paper')
        # project gift onto the paper now
        # send message to ws to render gift projection
        self.webSocket.send_current_state()

    def on_enter_giftPlaced(self):
        print('Project the arrows onto the paper')
        # project arrows onto the paper now
        # send message to ws to render arrow projection
        self.webSocket.send_current_state()

    def on_enter_giftWrapped(self):
        print('gift was placed')
        # project arrows onto the paper now
        # send message to ws to render arrow projection
        self.webSocket.send_current_state()

    def on_enter_firstFold(self):
        print("first fold done")
        self.webSocket.send_current_state()

    def on_enter_secondFold(self):
        print("second fold done")
        self.webSocket.send_current_state()


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
                    self.lightpad2_lightened_up()
        except exceptions.TransitionNotAllowed:
            #print("Transition not allowed")
            print(self.current_state)

    def on_paper_teared(self, paper_length):
        self.finished_paper_prep()

    def get_current_message(self):

        state_id = self.current_state.identifier
        if hasattr(self, 'orderHandler'):
            current_order = self.orderHandler.current_order_items
        else:
            current_order = {}
        message = {
            "state": state_id,
            "gift_width": self.sizeCalculator.gift_width,
            "gift_height": self.sizeCalculator.gift_height,
            "gift_depth": self.sizeCalculator.gift_depth,
            "paper_width": self.sizeCalculator.paper_width,
            "paper_height": self.sizeCalculator.paper_height,
            "current_order": current_order
        }
        return str(message).replace("'",'"')


if __name__ == "__main__":
    orchestrator = Orchestrator()



