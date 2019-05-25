# Embedded file name: /storage/emulated/0/BombSquad/id.py
import bs
import bsInternal
from bsUI import *
import bsUI
from bsGame import *
import bsGame
bs.screenMessage("#OSUM")
class DamnPartyWindow(PartyWindow):
    def _onPartyMemberPress(self, clientID, isHost, widget):
        if bsInternal._getForegroundHostSession() is not None:
            kickStr = bs.Lstr(resource='kickText')
        else:
            # kick-votes appeared in build 14248
            if bsInternal._getConnectionToHostInfo().get('buildNumber', 0) < 14248:
                return
            kickStr = bs.Lstr(resource='kickVoteText')
            for rst in self._roster:
                cid = rst['clientID']
                if cid == clientID:
                    bs.screenMessage(rst['displayString'])
                    break
        p = PopupMenuWindow(position=widget.getScreenSpaceCenter(),
                            scale=2.3 if gSmallUI else 1.65 if gMedUI else 1.23,
                            choices=['kick','adminKick'],
                            choicesDisplay=[kickStr,r"Kick"],
                            currentChoice='kick',
                            delegate=self).getRootWidget()
        self._popupType='partyMemberPress'
        self._popupPartyMemberClientID = clientID
        self._popupPartyMemberIsHost = isHost
def adminKick(self,popupWindow,choice):
    
    def getIndex():
        for i in bsInternal._getGameRoster():
            if i["clientID"] == self._popupPartyMemberClientID:
                return bsInternal._getGameRoster().index(i)

    if choice == "kick":
        if self._popupPartyMemberIsHost:
            bs.playSound(bs.getSound('error'))
            bs.screenMessage(bs.Lstr(resource='internal.cantKickHostError'),color=(1,0,0))
        else:
            print self._popupPartyMemberClientID
            result = bsInternal._disconnectClient(self._popupPartyMemberClientID)
            if not result:
                bs.playSound(bs.getSound('error'))
                bs.screenMessage(bs.Lstr(resource='getTicketsWindow.unavailableText'),color=(1,0,0))
    else:
    	f = open(bs.getEnvironment()['userScriptsDirectory'] + "/ban.txt",'a')
    	for i in bsInternal._getGameRoster():
            cid = i['clientID']
            if cid == self._popupPartyMemberClientID:
            	bsInternal._chatMessage("/kick " + str(cid))
            	f.write(i['players'][0]['nameFull'] + '  -  ' + eval(bsInternal._getGameRoster()[getIndex()]["specString"])["n"] + '\n')
        bs.textWidget(edit=self._textField,text='')
bsUI.PartyWindow = DamnPartyWindow
bsUI.PartyWindow.popupMenuSelectedChoice = adminKick

###Adding Kick Command###

def kickBoi(self):
        """
        Called once the previous bs.Activity has finished transitioning out.
        At this point the activity's initial players and teams are filled in
        and it should begin its actual game logic.
        """
        self._calledActivityOnBegin = True
        if len(bsInternal._getGameRoster())<2:
            bsInternal._chatMessage("#OSUM")

        bs.gameTimer(100,call=self._checkChat,repeat=True)
bsGame.Activity.onBegin = kickBoi
