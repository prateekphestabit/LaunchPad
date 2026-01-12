                day2__Network
                 A     A    A
                /      |     \
               /       |      \
              /        |       \
             /         |        \
            /          |         \
           v           v          v
DB container   serve_Container  client_Container(exposed PORT 3000)
                                                               A
                                                               |
                                                               |
                                                               |
 ______________________________________________________________v_________
|local machine sending request on - - - - - - - - - - - -localHost:3000  |
|                            next js App                                 | 
|________________________________________________________________________|
            