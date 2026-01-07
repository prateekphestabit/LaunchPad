module.exports = {
  apps: [
    {
      name: "week4-api",
      cwd: "/home/prateek/Prateek/LaunchPad/week4/Day5/src",
      script: "server.js",
      instances: 1,
      exec_mode: "fork",
      autorestart: true,
      watch: false,
      out_file: "/home/prateek/Prateek/LaunchPad/week4/Day5/logs/server-out.log",
      error_file: "/home/prateek/Prateek/LaunchPad/week4/Day5/logs/server-error.log",
      log_date_format: "YYYY-MM-DD HH:mm:ss Z",
      merge_logs: true,
      env: {
        NODE_ENV: "development",
        PORT: 5000
      },
      env_production: {
        NODE_ENV: "production",
        PORT: 5000
      }
    },
    {
      name: "email-worker",
      cwd: "/home/prateek/Prateek/LaunchPad/week4/Day5/src",
      script: "worker.js",
      instances: 1,
      exec_mode: "fork",
      autorestart: true,
      watch: false,
      out_file: "/home/prateek/Prateek/LaunchPad/week4/Day5/logs/worker-out.log",
      error_file: "/home/prateek/Prateek/LaunchPad/week4/Day5/logs/worker-error.log",
      log_date_format: "YYYY-MM-DD HH:mm:ss Z",
      merge_logs: true
    }
  ]
};