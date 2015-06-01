__author__ = 'Unknown'
import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton

class plug:

    def On_PluginInit(self):
        Server.Broadcast("running!")
        self.def_time = 3
        self.min_time = 1
        self.max_time = 10
        self.check = 0
        timer = Plugin.CreateTimer("testTimer", 10000)
        timer.start
        Server.Broadcast("Timer created");
    def CanUseDoor(self):
       while(self.check == 1):
            if Pluton.DoorCodeEvent.IsCorrect():
                timer = Plugin.CreateTimer("testTimer", 1)
                timer.start
                Server.Broadcast("Timer created1");
    def testTimerCallback(self, timer):
        Server.Broadcast("PluginInit was called 10 seconds ago")
        timer.Kill()



    #def time(self):
        #timer = Plugin.CreateTimer("testTimer", 10)
        #timer.start
        #Player.Message("Timer created");

    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.args
        command = cmd.cmd
        if command == "addisable":
            Server.Broadcast("ad is disabled")

            self.check = 0
        elif command == "ad":
            Server.Broadcast("My ad is enabled")
            if args < self.max_time and args > self.min_time:
                self.client_time = args
                Server.Broadcast(self.client_time)
