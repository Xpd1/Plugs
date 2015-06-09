__author__ = 'Unknown'
import clr

clr.AddReferenceByPartialName("Pluton")
clr.AddReferenceByPartialName("Assembly-CSharp")
import Pluton
import BasePlayer
import BaseEntity


class autodoor:
    def On_PluginInit(self):
        Server.Broadcast("Auto door is running!")
        ini = self.AutoDoorConfig()
        DataStore.Flush("DoorClose")
        self.DoorCheck = 0
        self.adm = int(ini.GetSetting("AutoDoorInfo","Admin mode"))


    def AutoDoorConfig(self):
        if not Plugin.IniExists("AutoDoorInfo"):
            ini = Plugin.CreateIni("AutoDoorInfo")
            ini.AddSetting("AutoDoorInfo", "Min time", "3")
            ini.AddSetting("AutoDoorInfo", "Max time", "10")
            ini.AddSetting("AutoDoorInfo", "Admin mode", "0")
            ini.Save()
        return Plugin.GetIni("AutoDoorInfo")

    def On_DoorUse(self, DoorUseEvent):
        ini = self.AutoDoorConfig()
        dict = Plugin.CreateDict()

        dict['Door'] = DoorUseEvent.Door
        if self.adm == 0:
            if DataStore.ContainsKey("DoorClose", DoorUseEvent.Player.SteamID):
                time = DataStore.Get("DoorClose", DoorUseEvent.Player.SteamID)
                Plugin.CreateParallelTimer("DoorClose", int(time) * 1000, dict).Start()
                return
        elif self.adm == 1:
            Plugin.CreateParallelTimer("DoorClose", self.client_time*1000, dict).Start()
            return
        else:
            return
    def DoorCloseCallback(self, timer):
        timer.Kill()

        dict = timer.Args

        ent = dict['Door']

        door = ent.baseEntity

        door.SetFlag(BaseEntity.Flags.Open, False)

        door.Invoke("UpdateLayer", 0)
        door.SendNetworkUpdate(BasePlayer.NetworkQueue.Update)

    def On_PlayerDisconnected(self, player):
        if DataStore.ContainsKey("DoorClose", player.SteamID):
            DataStore.Remove("DoorClose", player.SteamID)

    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.args
        command = cmd.cmd
        ini = self.AutoDoorConfig()
        minv = int(ini.GetSetting("AutoDoorInfo", "Min time"))
        maxv = int(ini.GetSetting("AutoDoorInfo", "Max time"))

        if self.adm == 0:
            if command == "adcdisable":
                DataStore.Remove("DoorClose", Player.SteamID)
                Player.Message("Auto door is disabled")


            elif command == "adc":
                if len(args) == 0:
                    Player.Message("Enter argument")
                    return
                else:
                    numb = args[0]

                if not numb.isnumeric():
                    Player.MessageFrom("AutoDoor","Enter a number")
                    return
                else:
                    number = int(numb)
                    if minv <= number <= maxv:
                        DataStore.Add("DoorClose", Player.SteamID, number)
                        Player.MessageFrom("AutoDoorCloser", "AutoDoor timer is now set to: " + str(number) + " !")
                    else:
                        Player.MessageFrom("AutoDoor","Value is between " + str(minv) + " and " + str(maxv))
        elif self.adm == 1:
            if not Player.Owner:
                Player.MessageFrom("Bounty","You are not admin")
                return

            elif command == "adcdisable":
                self.DoorCheck = 0
                Player.MessageFrom("AutoDoor","Auto door is disabled")
                return

            elif command == "adc":
                if len(args) == 0:
                    Player.MessageFrom("AutoDoor","Enter argument")
                    return
                else:
                    numb = args[0]

                if not numb.isnumeric():
                    Player.MessageFrom("AutoDoor","Enter a number")
                    return
                else:
                    numb = int(numb)
                    if minv <= numb <= maxv:
                        self.DoorCheck = 1
                        self.client_time = numb
                        Server.Broadcast("AutoDoor timer is now set to: " + str(numb) + " !")
                    else:
                        Player.MessageFrom("AutoDoor","Value is between "+ str(minv) + " and " + str(maxv))
        else:
            if command == "adc":
                Player.MessageFrom("AutoDoor", "Wrong mode, check AutoDoorInfo.ini")
                return



