__author__ = 'Unknown'
import clr

clr.AddReferenceByPartialName("Pluton")
clr.AddReferenceByPartialName("Assembly-CSharp")
import Pluton
import BasePlayer
import BaseEntity

class plug:

    def On_PluginInit(self):
        Server.Broadcast("It's running!")
        self.check = 0
        self.minv = 1
        self.maxv = 10
    def On_DoorUse(self, DoorUseEvent):
            if self.check == 1:
                dict = Plugin.CreateDict()
                Server.Broadcast("1")
                dict['Door'] = DoorUseEvent.Door
                Server.Broadcast("2")
                Plugin.CreateParallelTimer("DoorClose", self.client_time*1000, dict).Start()
                Server.Broadcast("3")

    def DoorCloseCallback(self, timer):
            timer.Kill()
            Server.Broadcast("4")
            dict = timer.Args
            Server.Broadcast("5")
            ent = dict['Door']
            Server.Broadcast("6")
            door = ent.baseEntity
            Server.Broadcast("7")
            door.SetFlag(BaseEntity.Flags.Open, False)
            Server.Broadcast("8")
            door.Invoke("UpdateLayer", 0)
            door.SendNetworkUpdate(BasePlayer.NetworkQueue.Update)


    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.args
        command = cmd.cmd

        if command == "addisable":
            self.check = 0
            Server.Broadcast("ad is disabled")

        elif command == "ad":
            Server.Broadcast("My ad is enabled")
            if len(args) == 0:
                Server.Broadcast("Enter argument")
            else:
                numb = args[0]

            if not numb.isnumeric():
                Server.Broadcast("Enter a number")
            else:
                numb = int(numb)
                if self.minv <= numb <= self.maxv:
                    self.check = 1
                    self.client_time = numb
                else:
                    Server.Broadcast("Value is between "+ str(self.minv) + " and " + str(self.maxv))
