__author__ = 'Xpd'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Pluton")
clr.AddReferenceByPartialName("Assembly-CSharp")
import sys
import Pluton
import BasePlayer
import BaseEntity

path = Util.GetPublicFolder()
sys.path.append(path + "\\Plugins\\Clans")
sys.path.append(path + "\\Plugins\\AdminCommands")

class bounty:

    def On_PluginInit(self):
        Server.BroadcastFrom("Bounty","Bounty is running")
        self.BountyConfig()

    def BountyConfig(self):
        if not Plugin.IniExists("BountyInfo"):
            ini = Plugin.CreateIni("BountyInfo")
            ini.AddSetting("BountyInfo", "Clans enabled", "0")
            ini.AddSetting("BountyInfo", "Friends enabled", "0")
            ini.AddSetting("BountyInfo", "List mode", "0")
            ini.AddSetting("BountyInfo", "Top", "10")
            ini.Save()
        return Plugin.GetIni("BountyInfo")

    def HasClan(self, ID):
        ini = Plugin.GetIni(path + "\\Plugins\\Clans\\Clans")
        if ini.ContainsSetting("ClanMembers", ID) or ini.ContainsSetting("ClanOfficers", ID) or \
                ini.ContainsSetting("ClanOwners", ID) or ini.ContainsSetting("ClanCoOwners", ID):
            return True
        else:
            return False
    def GetClanOfPlayer(self, ID):
        ini = Plugin.GetIni(path + "\\Plugins\\Clans\\Clans")
        if ini.ContainsSetting("ClanMembers", ID):
            return ini.GetSetting("ClanMembers", ID)
        elif ini.ContainsSetting("ClanOfficers", ID):
            return ini.GetSetting("ClanOfficers", ID)
        elif ini.ContainsSetting("ClanOwners", ID):
            return ini.GetSetting("ClanOwners", ID)
        elif ini.ContainsSetting("ClanCoOwners", ID):
            return ini.GetSetting("ClanCoOwners", ID)
        return None

    def FriendOF(self, ofid, id):
        ini = Plugin.GetIni(path + "\\Plugins\\AdminCommands\\Friends")
        if ini.GetSetting(ofid, id) and ini.GetSetting(ofid, id) is not None:
            return True
        return False

    def GetKeysAndValues(self, Table):
        names = {}
        for id in DataStore.Keys(Table):
            g = DataStore.Get(Table, id)
            names.update({id: g})
        return names

    def GetKeyByValue(self, Dict, Value):
        for n, v in Dict.iteritems():
            if v == Value:
                 return n

    def On_PlayerDied(self, playerdeathevent):
        ini = self.BountyConfig()
        ClanCheck = int(ini.GetSetting("BountyInfo", "Clans enabled"))
        FriendsCheck = int(ini.GetSetting("BountyInfo", "Friends enabled"))

        if DataStore.ContainsKey("Bounty", playerdeathevent.Victim.SteamID):
            if playerdeathevent.Attacker is None:
                return
            attacker = playerdeathevent.Attacker.ToPlayer()
            if attacker is None:
                return
            if ClanCheck == 1:
                if self.HasClan(playerdeathevent.Victim.SteamID) and self.HasClan(playerdeathevent.Attacker.SteamID):
                    ca = self.GetClanOfPlayer(playerdeathevent.Attacker.SteamID)
                    cv = self.GetClanOfPlayer(playerdeathevent.Victim.SteamID)
                    if ca == cv:
                        return
                else:
                    head = float(DataStore.Get("Bounty", playerdeathevent.Victim.SteamID))
                    DataStore.Add("iConomy", playerdeathevent.Attacker.SteamID, float(DataStore.Get("iConomy", playerdeathevent.Attacker.SteamID)) + head)
                    DataStore.Remove("Bounty", playerdeathevent.Victim.SteamID )
                    Server.BroadcastFrom("Bounty", "Bounty has been claimed for " + playerdeathevent.Victim.Name)
                    return
            if FriendsCheck == 1:
                if self.FriendOF(playerdeathevent.Victim.SteamID, playerdeathevent.Attacker.SteamID):
                    return

            head = float(DataStore.Get("Bounty", playerdeathevent.Victim.SteamID))
            DataStore.Add("iConomy", playerdeathevent.Attacker.SteamID, float(DataStore.Get("iConomy", playerdeathevent.Attacker.SteamID)) + head)
            DataStore.Remove("Bounty", playerdeathevent.Victim.SteamID )
            Server.BroadcastFrom("Bounty", "Bounty has been claimed for " + playerdeathevent.Victim.Name)

    def On_Command(self,cmd):
        Player = cmd.User
        args = cmd.quotedArgs
        command = cmd.cmd

        monies = (DataStore.Get("iConomy", Player.SteamID))
        if command == "bt":
            if len(args) <= 1:
                Player.MessageFrom("Bounty", "Usage: /bt 'target_name' 'amount' ")
                return
            amount = args[1]
            target = Server.FindPlayer(args[0])
            if not amount.isnumeric():
                Player.MessageFrom("Bounty", "Usage: /bt 'target_name' 'amount' ")
                return
            amount = abs(float(amount))
            if monies < amount:
                Player.MessageFrom("Bounty", "Not enough credits")
                return

            if target is  None:
                Player.MessageFrom("Bounty","That is not a valid player")
                return
            else:
                if DataStore.ContainsKey("Bounty", target.SteamID):
                    DataStore.Add("Bounty", target.SteamID, float(DataStore.Get("Bounty", target.SteamID))+ amount)
                    Server.BroadcastFrom("Bounty","Bounty has been set on "+ str(target.Name)+" for "+str(amount))
                    return
                else:
                    DataStore.Add("iConomy", Player.SteamID, float(DataStore.Get("iConomy", Player.SteamID)) - amount)
                    DataStore.Add("Bounty", target.SteamID, amount)
                    Server.BroadcastFrom("Bounty","Bounty has been set on "+ str(target.Name)+" for "+str(amount))
                    return

        elif command == "btreset":
            if not Player.Owner:
                Player.MessageFrom("Bounty","You are not admin")
                return
            DataStore.Flush("Bounty")
            Server.BroadcastFrom("Bounty", "Data has been reset")
        elif command == "btp":
            if len(args)== 0:
                Player.MessageFrom("Bounty", "Usage: /btp 'target_name'")
                return
            if args[0].isnumeric():
                Player.MessageFrom("Bounty", "Usage: /btp 'target_name'")
                return
            target = Server.FindPlayer(args[0])
            if target is None:
                Player.MessageFrom("Bounty","That is not a valid player")
            if DataStore.ContainsKey("Bounty", target.SteamID):
                head = str(DataStore.Get("Bounty", target.SteamID))
                Player.MessageFrom("Bounty","Bounty on "+target.Name+" is "+ head)
                return
            Server.BroadcastFrom("Bounty", "No bounty on his head")
        elif command == "btlist":
            ini = self.BountyConfig()
            mod = int(ini.GetSetting("BountyInfo", "List mode"))
            if mod == 0:
                for player in Server.ActivePlayers:
                    head = str(DataStore.Get("Bounty", player.SteamID))
                    Player.MessageFrom("Bounty",player.Name+": " + head )
                    continue
            if mod == 1:
                y = int(ini.GetSetting("BountyInfo", "Top"))
                x = 0
                tel = self.GetKeysAndValues("Bounty")
                for key in tel.keys():
                    # srted = GetKeyByValue(tel,Values)
                    value = tel[key]
                    name = Server.FindPlayer(key)
                    if name is None:
                        continue
                    Player.MessageFrom("Bounty",str(name.Name) +": "+ str(value))
                    x+= 1
                    if x == y:
                        x = 0
                        return



