const express = require('express');
const pool = require('../db');
const { PythonShell } = require('python-shell');
const router = express.Router();

// Existing route to fetch users
router.get('/users', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM users');
        res.json(result.rows);
    } catch (err) {
        console.error(err.message);
        res.status(500).send('Server Error');
    }
});

// New route to insert a user
router.post('/users', async (req, res) => {
    const { username, telegram_id } = req.body;
    try {
        const result = await pool.query(
            'INSERT INTO users (username, telegram_id) VALUES ($1, $2) RETURNING *',
            [username, telegram_id]
        );
        res.json(result.rows[0]);
    } catch (err) {
        console.error(err.message);
        res.status(500).send('Server Error');
    }
});

// New route to run a bot
router.post('/run-bot', (req, res) => {
    PythonShell.run('path/to/your/bot.py', null, (err, results) => {
        if (err) {
            console.error(err.message);
            return res.status(500).send('Error running bot');
        }
        res.send(results.join('\n'));
    });
});

module.exports = router;
