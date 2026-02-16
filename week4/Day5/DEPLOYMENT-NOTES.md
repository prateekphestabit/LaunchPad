## Run this before using pm2
# docker run -itd -p 6379:6379 --name="redis" redis

1. npm run dev 
- connects to redis
- connects api
- starts the app on port 5000

2. using post man create jobs 

3. start and initlize number of workers using node worker.js



## Production
using pm2 start the app in production

1. Run: cd /home/prateek/Prateek/LaunchPad/week4/Day5/src/prod
2. Run: pm2 start
3. generate jobs using postman
4. see execution in error.log

# pm2 start
# pm2 stop all
# pms delete all
# pm2 ls 