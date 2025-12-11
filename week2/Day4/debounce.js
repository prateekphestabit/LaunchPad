const api = (text) => {
    console.log("suggesting words similar to", text);
}

const debounce = (fun, delay) => {
    let timer;
    return function(...args) {
        clearTimeout(timer);
        timer = setTimeout(() => {
            fun.apply(this, args);
        }, delay);
    }
}

const debouncedApi = debounce(api, 1000);

