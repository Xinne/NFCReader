

from __future__ import print_function
from time import sleep
from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver

from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.System import readers
from smartcard.scard import SCARD_CTL_CODE, SCARD_SHARE_DIRECT, SCARD_SHARE_SHARED
from smartcard.util import toHexString
import copy
import sys
import logging


import NFCReader.readers as red

from smartcard.Exceptions import NoCardException, CardConnectionException
COMMAND = [0xFF, 0xCA, 0x00, 0x00, 0x00] #handshake cmd needed to initiate data transfer
KEY_A = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF ]
LOAD_KEY_A_MSG =  [0xFF, 0x82, 0x00, 0x00, 0x06]
# get all the available readers

reader = None
def init(callback, cb2):
    global reader

    reader = NFCreader(callback, cb2)
    return reader
    #atexit.register(reader.killObserver)




class NFCCard():
    def __init__(self, card):
        self.card = card
        self.__uid = None;
        
    def getUID(self):
        if not self.__uid:
            response, sw1, sw2 = self.card.connection.transmit([0xFF, 0xCA, 0x00, 0x00, 0x04]) 
            self.__uid = response
        return int(toHexString(self.__uid).replace(" ", ""), 16)
    
    def disconnect(self):
        return self.card.connection.disconnect()
             
class NFCreader():  
    def __init__(self, callback, cb2):
        self.reader = red.getReader()

        #make it beep!
        #answ = self.reader.control(SCARD_CTL_CODE(3500), [0xFF, 0x00, 0x40, 0xC3, 0x04, 0x04, 0x06, 0x01, 0x01])
        
        #turn off default beep is card is scanned
        #answ = self.reader.control(SCARD_CTL_CODE(3500), [0xFF, 0x00, 0x52, 0x00, 0x00])
        
        #turn off autopolling
        #answ = self.reader.control(SCARD_CTL_CODE(3500), [0xFF, 0x00, 0x51, 0x43, 0x00])
        #workaround to turn it back on
        #answ = self.reader.control(SCARD_CTL_CODE(3500), [0xFF, 0x00, 0x51, 0xC3, 0x00])
        
        #send direct command to tun on internal polling
        #answ = self.reader.control(SCARD_CTL_CODE(3500), [0xFF, 0x00, 0x00, 0x00, 0x05, 0xD4, 0x60, 0xFF, 0x02, 0x00])
        #print(answ)
        
        #answ = self.reader.control(SCARD_CTL_CODE(3500), [0xE0, 0x00, 0x00, 0x20, 0x01, 0x1F])
        
        

        self.cardmonitor = CardMonitor()
        self.cardobserver = self.PrintObserver(callback, cb2)
        self.cardmonitor.addObserver(self.cardobserver)      
    
    def killObserver(self):
        self.cardmonitor.deleteObserver(self.cardobserver)

    class PrintObserver(CardObserver):
        """A simple card observer that is notified
        when cards are inserted/removed from the system and
        prints the list of cards
        """
        def __init__(self, incallback, outcallback):
            CardObserver.__init__(self)
            self.InCallback = incallback
            self.outCallback = outcallback 
            self.observer = ConsoleCardConnectionObserver()  
            
        def update(self, observable, actions):
            (addedcards, removedcards) = actions
            #for card in removedcards:
                #print(card)
            for card in addedcards:
                card.connection = card.createConnection()

                try:
                    card.connection.connect()
                except NoCardException as e:
                    continue
                except CardConnectionException as e:
                    print(e)
                    #todo implement error show
                    continue
                ncard = NFCCard(card)
                ncard.getUID()
                #card.connection.addObserver(self.observer)
                self.InCallback(ncard)

                #print(toHexString(card.connection.getATR()))
                #card.connection.disconnect()
            for card in removedcards:
                self.outCallback(card)
                #print("-Removed: ", toHexString(card.atr))


                    
           
