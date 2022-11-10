import sys
import os
sys.path.append(os.path.realpath(os.getcwd()))
import predefined
from fsm import State, TransitionError, MealyMachine

VALID_TCP_EVENTS = (
    predefined.TIMEOUT,
    predefined.SDATA,
    predefined.RDATA,
    predefined.FIN,
    predefined.ACK,
    predefined.SYNACK,
    predefined.CLOSE,
    predefined.SYN,
    predefined.ACTIVE,
    predefined.PASSIVE,
)

# Setup FSM
state_closed      = State(predefined.CLOSED, initial=True)
state_listen      = State(predefined.LISTEN)
state_syn_sent    = State(predefined.SYN_SENT)
state_syn_rcvd    = State(predefined.SYN_RCVD)
state_established = State(predefined.ESTABLISHED)
state_fin_wait_1  = State(predefined.FIN_WAIT_1)
state_fin_wait_2  = State(predefined.FIN_WAIT_2)
state_closing     = State(predefined.CLOSING)
state_time_wait   = State(predefined.TIME_WAIT)
state_close_wait  = State(predefined.CLOSE_WAIT)
state_last_ack    = State(predefined.LAST_ACK)

state_established.received_count = 0
state_established.sent_count     = 0

sent_counter = 0
recv_counter = 0


# Transitions
# <state name>[(<input>, <output>)] = <next state>
state_closed[(predefined.PASSIVE,    predefined.NONE)]    = state_listen
state_closed[(predefined.ACTIVE,     predefined.syn)]     = state_syn_sent
state_listen[(predefined.SYN,        predefined.syn_ack)] = state_syn_rcvd
state_listen[(predefined.CLOSE,      predefined.NONE)]    = state_closed
state_syn_sent[(predefined.CLOSE,    predefined.NONE)]    = state_closed
state_syn_sent[(predefined.SYN,      predefined.syn_ack)] = state_syn_rcvd
state_syn_sent[(predefined.SYNACK,   predefined.ack)]     = state_established
state_syn_rcvd[(predefined.ACK,      predefined.NONE)]    = state_established
state_syn_rcvd[(predefined.CLOSE,    predefined.fin)]     = state_fin_wait_1
state_established[(predefined.CLOSE, predefined.fin)]     = state_fin_wait_1
state_established[(predefined.FIN,   predefined.ack)]     = state_close_wait
state_established[(predefined.RDATA, predefined.n_out)]   = state_established
state_established[(predefined.SDATA, predefined.n_out)]   = state_established
state_fin_wait_1[(predefined.FIN,    predefined.ack)]     = state_closing
state_fin_wait_1[(predefined.ACK,    predefined.NONE)]    = state_fin_wait_2
state_fin_wait_2[(predefined.FIN,    predefined.ack)]     = state_time_wait
state_closing[(predefined.ACK,       predefined.NONE)]    = state_time_wait
state_time_wait[(predefined.TIMEOUT, predefined.NONE)]    = state_closed
state_close_wait[(predefined.CLOSE,  predefined.fin)]     = state_last_ack
state_last_ack[(predefined.ACK,      predefined.NONE)]    = state_closed

errorcount = 0
transitionErrorCount = 0

class TCPMachine(MealyMachine):
    
    def __init__(self, name, start_state):
        self.current_state = self.init_state = start_state

    def transition(self, event):
        if self.current_state is None:
            raise TransitionError('Current State is not yet set.')

        destination_state = self.current_state.get(
            event, self.current_state.default_transition)

        if destination_state:
            self.current_state = destination_state
        else:
            raise TransitionError('Transition cannot happen from State "%s"'
                                  ' on Event "%s"' % (self.current_state.name,
                                                      event))

        if event == predefined.RDATA:
            assert self.current_state.name == predefined.ESTABLISHED
            #recv_counter+=1
            self.current_state.received_count += 1
        if event == predefined.SDATA:
            assert self.current_state.name == predefined.ESTABLISHED
            #sent_counter+=1
            self.current_state.sent_count += 1
        if event == predefined.TIMEOUT:
            pass
    

    
    def validateEvent(self,event):
        if event in VALID_TCP_EVENTS:
            print("Valid event")
        else:
            print("Uncaught Event")
        
def initialize_tcp_fsm():
    return TCPMachine(name="DCN TCP FSM",start_state=state_closed)

def main():
    tcp_fsm = initialize_tcp_fsm()
    while True:
        try:
            event = sys.stdin.readline()
            if event in ("\n",""):
                #print(f"Count of Unexpected Event : {errorcount}, Count of errors in transition : {transitionErrorCount}")
                break

            event = event.strip()

            if event == "SEND" and tcp_fsm.current_state.name == predefined.LISTEN:
                continue
            elif event not in VALID_TCP_EVENTS:
                print(f"Error: unexpected Event: {event}")
                #errorcount += 1
            else:
                tcp_fsm.transition(event)
                if tcp_fsm.current_state.name == predefined.ESTABLISHED:
                    if event == predefined.SDATA:
                        print(f"DATA Sent {tcp_fsm.current_state.sent_count}")
                    if event == predefined.RDATA:
                        print(f"DATA Received {tcp_fsm.current_state.received_count}")
                if event not in(predefined.SDATA, predefined.RDATA):
                    print(f"Event {event} received, current State is {tcp_fsm.current_state.name}")
        except TransitionError as e:
            #transitionErrorCount += 1
            print('TransitionError is as follows: %s' % (str(e)))

if __name__ == '__main__':
    main()
