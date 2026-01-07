class AppLoader {
    async loadApp(app, PORT) {
        app.listen(PORT, () => {
            console.log(`Server is running at http://localhost:${PORT} with ${process.pid}\n`);
        });
    }
}

module.exports = new AppLoader();