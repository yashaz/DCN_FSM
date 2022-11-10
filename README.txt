FSM - Finite State Machine

The file: tcpFSM_main.py is the starter file (contains the main function).

The program coded has ACTIVE (client) and PASSIVE (server) sides. Using Mealy State machine, the states and transitions are pre-defined, with events handled from standard input. All events are processed in uppercase letters only. 

For the Actions on the ESTABLISHED/(R|S)DATA Transitions:
The program displays: “DATA received n” when the event is RDATA 
The program displays: "DATA sent n" when the event is SDATA.  
In receiving RDATA or SDATA, the counter is incremented accordingly. 

For all Transitions EXCEPT those caused by the (R|S)DATA Events, the message: "Event eee received, current State is sss" where eee is the Event and sss is the current State is displayed

ANY String read from standard input that is NOT one of the events defined raises an exception and the program continues as if the “bad” input did not occur. 
It displays: "Error: unexpected Event: xxx" where xxx is the invalid event.
On encountering invalid transitions, an exception is raised to highlight the message that for the event received, transition cannot take place with respect to the current state of machine. 
On detecting the end of input stream or standard input, the program exits.


To run the program: python tcpFSM_main.py

To execute the test cases: python -m pytest unit_test.py -v