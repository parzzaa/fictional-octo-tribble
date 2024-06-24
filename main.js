document.getElementById('fetch-users').addEventListener('click', async () => {
    const response = await fetch('/api/users');
    const users = await response.json();
    const usersList = document.getElementById('users-list');
    usersList.innerHTML = '';
    users.forEach(user => {
        const listItem = document.createElement('li');
        listItem.textContent = `${user.username} (ID: ${user.telegram_id})`;
        usersList.appendChild(listItem);
    });
});
