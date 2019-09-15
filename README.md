# Understanding Nginx + Tornado Concurrency + Redis


prerequsites 

`sudo apt-get install apache2-utils`

#### The apache bench test below simulates the 
```bash
2019/09/15 19:46:18 [error] 1510#1510: *699 no live upstreams while connecting to upstream, client: 10.0.2.2, server: _, request: "GET /backend HTTP/1.1", upstream: "http://backend/", host: "localhost:8080"
```

```bash
ab -n 100 -c 100 http://localhost:8080/backend
This is ApacheBench, Version 2.3 <$Revision: 1807734 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient).....done


Server Software:        nginx/1.14.0
Server Hostname:        localhost
Server Port:            8080

Document Path:          /backend
Document Length:        182 bytes

Concurrency Level:      100
Time taken for tests:   60.120 seconds
Complete requests:      100
Failed requests:        90
   (Connect: 0, Receive: 0, Length: 90, Exceptions: 0)
Non-2xx responses:      10
Total transferred:      24760 bytes
HTML transferred:       3710 bytes
Requests per second:    1.66 [#/sec] (mean)
Time per request:       60119.613 [ms] (mean)
Time per request:       601.196 [ms] (mean, across all concurrent requests)
Transfer rate:          0.40 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        4  547 513.5   1027    1030
Processing:   418 31199 18887.4  30087   59086
Waiting:      418 31198 18887.4  30087   59086
Total:       1446 31746 19156.9  30092   60114

Percentage of the requests served within a certain time (ms)
  50%  30092
  66%  40091
  75%  50096
  80%  50100
  90%  60108
  95%  60110
  98%  60114
  99%  60114
 100%  60114 (longest request)
 ```
