document.addEventListener('DOMContentLoaded', () => {
    const addUserForm = document.getElementById('add-user-form');
    const fetchUsersButton = document.getElementById('fetch-users');
    const runBotButton = document.getElementById('run-bot');
    const usersList = document.getElementById('users-list');
    const botResults = document.getElementById('bot-results');

    // Add User
    addUserForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const telegram_id = document.getElementById('telegram_id').value;

        try {
            const response = await fetch('/api/users', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, telegram_id })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const newUser = await response.json();
            const listItem = document.createElement('li');
            listItem.textContent = `${newUser.username} (ID: ${newUser.telegram_id})`;
            usersList.appendChild(listItem);

            addUserForm.reset();
        } catch (error) {
            console.error('Error:', error);
        }
    });

    // Fetch Users
    fetchUsersButton.addEventListener('click', async () => {
        try {
            const response = await fetch('/api/users');
            const users = await response.json();

            usersList.innerHTML = '';
            users.forEach(user => {
                const listItem = document.createElement('li');
                listItem.textContent = `${user.username} (ID: ${user.telegram_id})`;
                usersList.appendChild(listItem);
            });
        } catch (error) {
            console.error('Error:', error);
        }
    });

    // Run Bot
    runBotButton.addEventListener('click', async () => {
        try {
            const response = await fetch('/api/run-bot', { method: 'POST' });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const result = await response.text();
            botResults.textContent = result;
        } catch (error) {
            console.error('Error:', error);
        }
    });
});
