const { exec } = require("child_process");

// Host name
exec("hostname", (err, stdout) => {
    if(!err) console.log("HostName: " + stdout);
    else console.out("err");
});


// Disk space
exec("df -h --total --output=size | tail -1", (err, stdout) => {
    if (!err) {
        console.log("Total diskSpace: " + stdout);
    }
});

exec("df -h --output=avail / | tail -n 1", (err, stdout) => {
    if (!err) {
        console.log("available diskSpace: " + stdout);
    }
});

// Open ports (Linux safe version)
exec("ss -tuln | head -6", (err, stdout) => {
    if (!err) {
        console.log("Five Open Ports:");
        console.log(stdout || "No open ports found");
    }
});

// Default gateway
exec("ip route | grep default | awk '{print $3}'", (err, stdout) => {
    if (!err) {
        console.log("Default Gateway:", stdout.trim());
    }
});

// Number of logged-in users
exec("who | wc -l", (err, stdout) => {
    if (!err) {
        console.log("Users Logged In:", stdout.trim());
    }
});
