1. install mkcert
    creates public + private key for certificate


2. generate certificate for server's (patrick.dev, localhost)
    using "mkcert patrick.dev localhost 127.0.0.1"

    this generates 
    public + private + certifiacte for these servers

3. save this certificate + (private and public key on the nginx)

4. nginx -> certificate + pubilc key -> signature matching -> secured session key -> build ssl connection