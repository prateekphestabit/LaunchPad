nginx will divide the load on both the servers uing round robin 

test using postman: <http://localhost:8080


http://localhost:8080  ===>>>> nginx container exposing port 8080 ======>>>>>> day3 network
                            (round robin load balancing default)                    /\
                                                                                   /  \
                                                                                  /    \
                                                                                 /      \
                                                                            isolated     isolated 
                                                                            server1      server2