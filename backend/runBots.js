const { PythonShell } = require('python-shell');
const path = require('path');

const runBot = (botPath, options = {}) => {
    return new Promise((resolve, reject) => {
        PythonShell.run(path.join(__dirname, 'bots', botPath), options, (err, results) => {
            if (err) reject(err);
            resolve(results);
        });
    });
};

// Example usage
runBot('service_comment_bot.py', { args: ['arg1', 'arg2'] })
    .then(results => console.log(results))
    .catch(err => console.error(err));
