document.addEventListener('DOMContentLoaded', () => {
    // Initialize Socket.IO connection
    const socket = io.connect(window.location.origin);

    // DOM elements
    const loginModal = document.getElementById('login-modal');
    const lobbySection = document.getElementById('lobby');
    const gameTableSection = document.getElementById('game-table');
    const newGameButton = document.getElementById('new-game');
    const loginForm = document.getElementById('login-form');
    const loginError = document.getElementById('login-error');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const cancelLoginButton = document.getElementById('cancel-login');
    const hitButton = document.getElementById('hit-btn');
    const standButton = document.getElementById('stand-btn');
    const doubleButton = document.getElementById('double-btn');

    // Toggle Login Display
    function toggleLoginModal(show) {
        loginModal.style.display = show ? 'flex' : 'none';
        loginError.classList.add('hidden');
    }

    // Process Login Form Submission
    function processLogin(event) {
        event.preventDefault();
        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();

        fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === 'Logged in successfully') {
                console.log('Login successful:', data);
                toggleLoginModal(false);
                lobbySection.classList.remove('hidden'); // Show the lobby
            } else {
                throw new Error(data.message || 'Login failed');
            }
        })
        .catch(errorMessage => {
            loginError.textContent = errorMessage;
            loginError.classList.remove('hidden');
        });
    }

    // Create New Game Room in Lobby
    function addGameRoom(roomName) {
        const liveGamesContainer = document.getElementById('live-games');
        const roomDiv = document.createElement('div');
        roomDiv.className = 'game-room';
        roomDiv.innerHTML = `
            <span class="room-name">${roomName}</span>
            <button class="join-room">Join Game</button>
        `;
        liveGamesContainer.appendChild(roomDiv);
    }

    // Display Cards
    function displayCards(playerId, cards) {
        const cardsContainer = document.getElementById(`${playerId}-cards`);
        cardsContainer.innerHTML = ''; // Clear current cards
        cards.forEach(card => {
            const cardDiv = document.createElement('div');
            cardDiv.classList.add('card');
            cardDiv.classList.add('dealt'); // Trigger dealing animation
            cardDiv.textContent = `${card.rank} of ${card.suit}`;
            cardsContainer.appendChild(cardDiv);
        });
    }

    // Update Game State UI
    function updateGameState(gameState) {
        // Update dealer's cards
        displayCards('dealer', gameState.dealer_cards);
        // Update player's cards
        displayCards('player', gameState.player_cards);
        // Additional UI updates can be added here
    }

    // Event Listeners for Lobby Interactions
    newGameButton.addEventListener('click', () => {
        socket.emit('new_game');
        lobbySection.classList.add('hidden');
        gameTableSection.classList.remove('hidden');
    });

    // Event Listeners for Game Actions
    hitButton.addEventListener('click', () => {
        socket.emit('player_action', { action: 'hit' });
    });

    standButton.addEventListener('click', () => {
        socket.emit('player_action', { action: 'stand' });
    });

    doubleButton.addEventListener('click', () => {
        socket.emit('player_action', { action: 'double_down' });
    });

    // Socket Event Listeners
    socket.on('game_created', data => {
        // Logic for handling a new game creation
    });

    socket.on('game_state', data => {
        updateGameState(data);
    });

    socket.on('new_game_created', data => {
        addGameRoom(data.roomName);
    });

    socket.on('game_update', data => {
        updateGameState(data);
    });

    // Login Form Submission
    loginForm.addEventListener('submit', processLogin);

    // Cancel Login and Hide Modal
    cancelLoginButton.addEventListener('click', () => toggleLoginModal(false));

    // Initially Show Login Modal
    toggleLoginModal(true);
});

