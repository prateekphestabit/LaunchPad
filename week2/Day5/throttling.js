const throttle = (fn, delay) => {
  let timerId = null;

  return function (...args) {
    if (timerId) return;

    fn.apply(this, args);

    timerId = setTimeout(() => {
      timerId = null;
    }, delay);
  };
};

module.exports = throttle;