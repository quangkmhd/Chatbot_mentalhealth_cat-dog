document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const contextPanel = document.getElementById('context-panel');
    const closeContext = document.getElementById('close-context');
    const contextContent = document.getElementById('context-content');
    const historyList = document.getElementById('history-list');
    const welcomeContainer = document.getElementById('welcome-container');
    const newChatBtn = document.getElementById('new-chat-btn');
    const renameChat = document.getElementById('rename-chat');
    const deleteChat = document.getElementById('delete-chat');
    const renameModal = document.getElementById('rename-modal');
    const saveChatName = document.getElementById('save-chat-name');
    const chatNameInput = document.getElementById('chat-name-input');
    const examplePrompts = document.querySelectorAll('.example-prompt');
    const modelChoice = document.getElementById('model-choice');
    const currentModelIndicator = document.getElementById('current-model-indicator');
    const stars = document.querySelectorAll('.star');
    const ratingAverage = document.getElementById('rating-average');
    const ratingCount = document.getElementById('rating-count');
    
    let chatHistory = [];
    let conversations = [];
    let currentConversationId = null;
    let userHasRated = false; // Để theo dõi người dùng đã đánh giá chưa
    
    // Tải thông tin đánh giá từ server khi trang được tải
    function loadRating() {
        fetch('/rating')
            .then(response => response.json())
            .then(data => {
                updateRatingDisplay(data.average, data.count);
            })
            .catch(error => {
                console.error('Error loading rating:', error);
            });
    }
    
    // Cập nhật hiển thị đánh giá
    function updateRatingDisplay(average, count) {
        // Hiển thị điểm trung bình (làm tròn 1 chữ số thập phân)
        ratingAverage.textContent = average.toFixed(1);
        ratingCount.textContent = count;
        
        // Làm đầy sao dựa trên điểm trung bình
        const fullStars = Math.floor(average);
        const partialStar = average - fullStars;
        
        stars.forEach((star, index) => {
            // Reset trạng thái sao
            star.classList.remove('filled', 'fas');
            star.classList.add('far');
            
            // Điền đầy các sao hoàn chỉnh
            if (index < fullStars) {
                star.classList.remove('far');
                star.classList.add('fas', 'filled');
            } 
            // Nếu có phần sao (sử dụng sao nửa nếu cần)
            else if (index === fullStars && partialStar > 0) {
                // Đối với phần thập phân > 0.7, hiển thị sao đầy
                // Đối với phần thập phân < 0.3, giữ nguyên sao rỗng
                // Đối với 0.3-0.7, có thể thêm sao nửa nếu bạn có icon
                if (partialStar >= 0.7) {
                    star.classList.remove('far');
                    star.classList.add('fas', 'filled');
                } else if (partialStar >= 0.3) {
                    // Nếu bạn có icon sao nửa, sử dụng nó ở đây
                    // Hiện tại chỉ sử dụng sao đầy
                    star.classList.remove('far');
                    star.classList.add('fas', 'filled');
                }
            }
        });
    }
    
    // Gửi đánh giá đến server
    function submitRating(rating) {
        // Ngăn người dùng đánh giá nhiều lần
        if (userHasRated) {
            return;
        }
        
        fetch('/rate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                rating: rating
            })
        })
        .then(response => response.json())
        .then(data => {
            updateRatingDisplay(data.average, data.count);
            userHasRated = true; // Đánh dấu người dùng đã đánh giá
            
            // Thông báo cảm ơn
            const thankMessage = document.createElement('div');
            thankMessage.className = 'rating-thanks';
            thankMessage.textContent = 'Cảm ơn bạn đã đánh giá!';
            document.querySelector('.rating-container').appendChild(thankMessage);
            
            // Xóa thông báo sau 3 giây
            setTimeout(() => {
                thankMessage.remove();
            }, 3000);
        })
        .catch(error => {
            console.error('Error submitting rating:', error);
        });
    }
    
    // Xử lý sự kiện khi người dùng nhấp vào sao để đánh giá
    stars.forEach(star => {
        // Hiệu ứng hover
        star.addEventListener('mouseover', function() {
            const value = parseInt(this.getAttribute('data-value'));
            
            stars.forEach((s, index) => {
                // Reset tất cả sao trước
                s.classList.remove('hover', 'fas');
                s.classList.add('far');
                
                // Điền các sao đến vị trí con trỏ
                if (index < value) {
                    s.classList.remove('far');
                    s.classList.add('fas', 'hover');
                }
            });
        });
        
        // Khi con trỏ rời khỏi khu vực sao
        star.addEventListener('mouseout', function() {
            stars.forEach(s => {
                s.classList.remove('hover', 'fas');
                s.classList.add('far');
            });
            
            // Khôi phục trạng thái hiển thị đánh giá
            loadRating();
        });
        
        // Khi người dùng nhấp để đánh giá
        star.addEventListener('click', function() {
            const rating = parseInt(this.getAttribute('data-value'));
            submitRating(rating);
        });
    });
    
    // Auto-resize textarea
    chatInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        if (this.scrollHeight > 200) {
            this.style.height = '200px';
            this.style.overflowY = 'auto';
        }
    });
    
    // Model selection change
    modelChoice.addEventListener('change', function() {
        const selectedModel = this.value;
        
        // Update the model indicator
        if (selectedModel === 'groq') {
            currentModelIndicator.innerHTML = '<i class="fas fa-bolt"></i> Đang sử dụng: Llama-3.3-70b (Nhanh)';
        } else {
            currentModelIndicator.innerHTML = '<i class="fas fa-dollar-sign"></i> Đang sử dụng: DeepSeek Chat (Miễn phí)';
        }
        
        // Send the model choice to the server
        fetch('/set_model', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model_choice: selectedModel
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log('Model changed to:', data.model);
            } else {
                console.error('Error changing model:', data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
    
    // Load conversations from localStorage
    function loadConversations() {
        const savedConversations = localStorage.getItem('pet_chatbot_conversations');
        if (savedConversations) {
            conversations = JSON.parse(savedConversations);
            renderConversationsList();
        }
    }
    
    // Save conversations to localStorage
    function saveConversations() {
        localStorage.setItem('pet_chatbot_conversations', JSON.stringify(conversations));
    }
    
    // Render conversations list in sidebar
    function renderConversationsList() {
        historyList.innerHTML = '';
        
        conversations.forEach(conv => {
            const convItem = document.createElement('div');
            convItem.className = 'history-item';
            if (conv.id === currentConversationId) {
                convItem.classList.add('active');
            }
            
            convItem.innerHTML = `
                <i class="fas fa-comment-dots"></i>
                <span>${conv.name}</span>
            `;
            
            convItem.addEventListener('click', () => loadConversation(conv.id));
            historyList.appendChild(convItem);
        });
    }
    
    // Create a new conversation
    function createNewConversation() {
        const timestamp = new Date().toLocaleString();
        const newConv = {
            id: Date.now().toString(),
            name: `Cuộc trò chuyện ${conversations.length + 1}`,
            timestamp: timestamp,
            messages: []
        };
        
        conversations.unshift(newConv);
        saveConversations();
        
        // Clear chat messages
        chatMessages.innerHTML = '';
        
        // Add welcome container
        const welcomeContainerHTML = `
            <div class="welcome-container" id="welcome-container">
                <div class="welcome-logo">
                    <img src="/static/images/bot-avatar.png" alt="Pet Chatbot Logo">
                </div>
                <h1>Pet Chatbot</h1>
                <p>Hỏi đáp về thú cưng, sức khỏe và chăm sóc thú cưng của bạn</p>
                
                <div class="example-prompts">
                    <div class="example-prompt" data-prompt="Chó con của tôi bị ho, tôi nên làm gì?">
                        <i class="fas fa-comment"></i>
                        <p>Chó con của tôi bị ho, tôi nên làm gì?</p>
                    </div>
                    <div class="example-prompt" data-prompt="Làm thế nào để huấn luyện mèo đi vệ sinh đúng chỗ?">
                        <i class="fas fa-comment"></i>
                        <p>Làm thế nào để huấn luyện mèo đi vệ sinh đúng chỗ?</p>
                    </div>
                    <div class="example-prompt" data-prompt="Thức ăn nào tốt cho chó Poodle?">
                        <i class="fas fa-comment"></i>
                        <p>Thức ăn nào tốt cho chó Poodle?</p>
                    </div>
                    <div class="example-prompt" data-prompt="Dấu hiệu nhận biết mèo bị bệnh?">
                        <i class="fas fa-comment"></i>
                        <p>Dấu hiệu nhận biết mèo bị bệnh?</p>
                    </div>
                </div>
            </div>
        `;
        chatMessages.innerHTML = welcomeContainerHTML;
        
        // Make sure the welcome container is visible
        document.getElementById('welcome-container').style.display = 'flex';
        
        // Re-attach event listeners to example prompts
        document.querySelectorAll('.example-prompt').forEach(prompt => {
            prompt.addEventListener('click', function() {
                const promptText = this.getAttribute('data-prompt');
                chatInput.value = promptText;
                chatInput.focus();
            });
        });
        
        // Set current conversation
        currentConversationId = newConv.id;
        chatHistory = [];
        
        renderConversationsList();
    }
    
    // Load a specific conversation
    function loadConversation(conversationId) {
        const conversation = conversations.find(c => c.id === conversationId);
        if (!conversation) return;
        
        currentConversationId = conversationId;
        chatHistory = [...conversation.messages];
        
        // Clear chat messages and add welcome container back if needed
        chatMessages.innerHTML = '';
        
        // Add welcome container if it doesn't exist
        if (!document.getElementById('welcome-container')) {
            const welcomeContainerHTML = `
                <div class="welcome-container" id="welcome-container">
                    <div class="welcome-logo">
                        <img src="/static/images/bot-avatar.png" alt="Pet Chatbot Logo">
                    </div>
                    <h1>Pet Chatbot</h1>
                    <p>Hỏi đáp về thú cưng, sức khỏe và chăm sóc thú cưng của bạn</p>
                    
                    <div class="example-prompts">
                        <div class="example-prompt" data-prompt="Chó con của tôi bị ho, tôi nên làm gì?">
                            <i class="fas fa-comment"></i>
                            <p>Chó con của tôi bị ho, tôi nên làm gì?</p>
                        </div>
                        <div class="example-prompt" data-prompt="Làm thế nào để huấn luyện mèo đi vệ sinh đúng chỗ?">
                            <i class="fas fa-comment"></i>
                            <p>Làm thế nào để huấn luyện mèo đi vệ sinh đúng chỗ?</p>
                        </div>
                        <div class="example-prompt" data-prompt="Thức ăn nào tốt cho chó Poodle?">
                            <i class="fas fa-comment"></i>
                            <p>Thức ăn nào tốt cho chó Poodle?</p>
                        </div>
                        <div class="example-prompt" data-prompt="Dấu hiệu nhận biết mèo bị bệnh?">
                            <i class="fas fa-comment"></i>
                            <p>Dấu hiệu nhận biết mèo bị bệnh?</p>
                        </div>
                    </div>
                </div>
            `;
            chatMessages.innerHTML = welcomeContainerHTML;
            
            // Re-attach event listeners to example prompts
            document.querySelectorAll('.example-prompt').forEach(prompt => {
                prompt.addEventListener('click', function() {
                    const promptText = this.getAttribute('data-prompt');
                    chatInput.value = promptText;
                    chatInput.focus();
                });
            });
        }
        
        // Show welcome container if there are no messages
        const welcomeContainer = document.getElementById('welcome-container');
        if (chatHistory.length === 0) {
            welcomeContainer.style.display = 'flex';
        } else {
            welcomeContainer.style.display = 'none';
            
            // Display messages
            chatHistory.forEach(message => {
                addMessageToUI(message.content, message.role === 'user');
            });
        }
        
        renderConversationsList();
    }
    
    // Rename current conversation
    function renameCurrentConversation(newName) {
        if (!currentConversationId) return;
        
        const conversation = conversations.find(c => c.id === currentConversationId);
        if (conversation) {
            conversation.name = newName;
            saveConversations();
            renderConversationsList();
        }
    }
    
    // Delete current conversation
    function deleteCurrentConversation() {
        if (!currentConversationId) return;
        
        conversations = conversations.filter(c => c.id !== currentConversationId);
        saveConversations();
        
        if (conversations.length > 0) {
            loadConversation(conversations[0].id);
        } else {
            currentConversationId = null;
            chatHistory = [];
            chatMessages.innerHTML = '';
            welcomeContainer.style.display = 'flex';
            renderConversationsList();
        }
    }
    
    // Function to display context
    function displayContext(context) {
        if (!context || context.trim() === '') {
            contextContent.innerHTML = '<p class="context-empty">Không có thông tin tham khảo cho câu hỏi này.</p>';
            return;
        }
        
        contextContent.innerHTML = '';
        
        const contextChunks = context.split('\n\n');
        contextChunks.forEach(chunk => {
            const parts = chunk.split('\n');
            const text = parts[0];
            
            const chunkDiv = document.createElement('div');
            chunkDiv.className = 'context-chunk';
            
            const contentP = document.createElement('p');
            contentP.textContent = text;
            chunkDiv.appendChild(contentP);
            
            if (parts.length > 1) {
                const metadataDiv = document.createElement('div');
                metadataDiv.className = 'context-metadata';
                
                for (let i = 1; i < parts.length; i++) {
                    if (parts[i].includes(': ')) {
                        const [key, value] = parts[i].split(': ', 2);
                        const metaP = document.createElement('p');
                        metaP.innerHTML = `<strong>${key}:</strong> ${value}`;
                        metadataDiv.appendChild(metaP);
                    }
                }
                
                chunkDiv.appendChild(metadataDiv);
            }
            
            contextContent.appendChild(chunkDiv);
        });
        
        // Show context panel
        contextPanel.classList.add('show');
    }
    
    // Function to add message to UI only (without updating history)
    function addMessageToUI(message, isUser = false) {
        // Make sure the welcome container is hidden when adding messages
        const welcomeContainer = document.getElementById('welcome-container');
        if (welcomeContainer) {
            welcomeContainer.style.display = 'none';
        }
        
        const messageDiv = document.createElement('div');
        messageDiv.className = isUser ? 'message user-message' : 'message bot-message';
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        
        const avatarImg = document.createElement('img');
        avatarImg.src = isUser 
            ? "/static/images/user-avatar.png" 
            : "/static/images/bot-avatar.png";
        avatarImg.alt = isUser ? 'User Avatar' : 'Bot Avatar';
        
        avatarDiv.appendChild(avatarImg);
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const paragraph = document.createElement('p');
        paragraph.innerHTML = message.replace(/\n/g, '<br>');
        
        contentDiv.appendChild(paragraph);
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to add message to chat (UI and history)
    function addMessage(message, isUser = false) {
        // Add to UI
        addMessageToUI(message, isUser);
        
        // Add to chat history
        chatHistory.push({
            role: isUser ? 'user' : 'assistant',
            content: message
        });
        
        // Update conversation in storage
        if (currentConversationId) {
            const conversation = conversations.find(c => c.id === currentConversationId);
            if (conversation) {
                conversation.messages = chatHistory;
                saveConversations();
            }
        }
    }
    
    // Function to send message
    function sendMessage() {
        const message = chatInput.value.trim();
        if (message === '') return;
        
        // Create new conversation if none exists
        if (!currentConversationId) {
            createNewConversation();
        }
        
        // Add user message to chat
        addMessage(message, true);
        
        // Clear input and reset height
        chatInput.value = '';
        chatInput.style.height = 'auto';
        
        // Add loading message
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message bot-message loading';
        
        const loadingAvatar = document.createElement('div');
        loadingAvatar.className = 'message-avatar';
        
        const loadingAvatarImg = document.createElement('img');
        loadingAvatarImg.src = "/static/images/bot-avatar.png";
        loadingAvatarImg.alt = 'Bot Avatar';
        
        loadingAvatar.appendChild(loadingAvatarImg);
        
        const loadingContent = document.createElement('div');
        loadingContent.className = 'message-content';
        
        const loadingDots = document.createElement('div');
        loadingDots.className = 'loading-dots';
        loadingDots.innerHTML = '<span></span><span></span><span></span>';
        
        loadingContent.appendChild(loadingDots);
        loadingDiv.appendChild(loadingAvatar);
        loadingDiv.appendChild(loadingContent);
        
        chatMessages.appendChild(loadingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Send request to server
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                history: chatHistory
            })
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading message
            chatMessages.removeChild(loadingDiv);
            
            // Add bot message to chat
            addMessage(data.response);
            
            // Display context
            displayContext(data.context);
            
            // Update conversation name if it's the first message
            const conversation = conversations.find(c => c.id === currentConversationId);
            if (conversation && conversation.messages.length <= 2) {
                // Use first few words of user's first message as the conversation name
                const firstWords = message.split(' ').slice(0, 4).join(' ');
                conversation.name = firstWords + (message.length > firstWords.length ? '...' : '');
                saveConversations();
                renderConversationsList();
            }
        })
        .catch(error => {
            // Remove loading message
            chatMessages.removeChild(loadingDiv);
            
            // Add error message
            addMessage('Đã xảy ra lỗi khi xử lý yêu cầu của bạn. Vui lòng thử lại sau.');
            console.error('Error:', error);
        });
    }
    
    // Event Listeners
    
    // Send message on button click
    sendButton.addEventListener('click', sendMessage);
    
    // Send message on Enter key (but allow Shift+Enter for new line)
    chatInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Close context panel
    closeContext.addEventListener('click', function() {
        contextPanel.classList.remove('show');
    });
    
    // New chat button
    newChatBtn.addEventListener('click', function() {
        createNewConversation();
    });
    
    // Rename chat
    renameChat.addEventListener('click', function() {
        if (!currentConversationId) return;
        
        const conversation = conversations.find(c => c.id === currentConversationId);
        if (conversation) {
            chatNameInput.value = conversation.name;
            renameModal.style.display = 'block';
        }
    });
    
    // Save chat name
    saveChatName.addEventListener('click', function() {
        const newName = chatNameInput.value.trim();
        if (newName) {
            renameCurrentConversation(newName);
            renameModal.style.display = 'none';
        }
    });
    
    // Delete chat
    deleteChat.addEventListener('click', function() {
        if (confirm('Bạn có chắc chắn muốn xóa cuộc trò chuyện này?')) {
            deleteCurrentConversation();
        }
    });
    
    // Close modal when clicking on X or outside the modal
    document.querySelectorAll('.close-modal, .cancel-btn').forEach(element => {
        element.addEventListener('click', function() {
            renameModal.style.display = 'none';
        });
    });
    
    window.addEventListener('click', function(event) {
        if (event.target === renameModal) {
            renameModal.style.display = 'none';
        }
    });
    
    // Example prompts
    examplePrompts.forEach(prompt => {
        prompt.addEventListener('click', function() {
            const promptText = this.getAttribute('data-prompt');
            chatInput.value = promptText;
            chatInput.focus();
        });
    });
    
    // Initialize
    loadConversations();
    
    // Add the welcome container back to the DOM if it was removed
    if (!document.getElementById('welcome-container')) {
        const welcomeContainerHTML = `
            <div class="welcome-container" id="welcome-container">
                <div class="welcome-logo">
                    <img src="/static/images/bot-avatar.png" alt="Pet Chatbot Logo">
                </div>
                <h1>Pet Chatbot</h1>
                <p>Hỏi đáp về thú cưng, sức khỏe và chăm sóc thú cưng của bạn</p>
                
                <div class="example-prompts">
                    <div class="example-prompt" data-prompt="Chó con của tôi bị ho, tôi nên làm gì?">
                        <i class="fas fa-comment"></i>
                        <p>Chó con của tôi bị ho, tôi nên làm gì?</p>
                    </div>
                    <div class="example-prompt" data-prompt="Làm thế nào để huấn luyện mèo đi vệ sinh đúng chỗ?">
                        <i class="fas fa-comment"></i>
                        <p>Làm thế nào để huấn luyện mèo đi vệ sinh đúng chỗ?</p>
                    </div>
                    <div class="example-prompt" data-prompt="Thức ăn nào tốt cho chó Poodle?">
                        <i class="fas fa-comment"></i>
                        <p>Thức ăn nào tốt cho chó Poodle?</p>
                    </div>
                    <div class="example-prompt" data-prompt="Dấu hiệu nhận biết mèo bị bệnh?">
                        <i class="fas fa-comment"></i>
                        <p>Dấu hiệu nhận biết mèo bị bệnh?</p>
                    </div>
                </div>
            </div>
        `;
        chatMessages.innerHTML = welcomeContainerHTML;
        
        // Re-attach event listeners to example prompts
        document.querySelectorAll('.example-prompt').forEach(prompt => {
            prompt.addEventListener('click', function() {
                const promptText = this.getAttribute('data-prompt');
                chatInput.value = promptText;
                chatInput.focus();
            });
        });
    }
    
    // Clear any existing messages and show welcome screen if no conversation is selected
    if (conversations.length === 0 || !currentConversationId) {
        currentConversationId = null;
        chatHistory = [];
        document.getElementById('welcome-container').style.display = 'flex';
    } else {
        // Load the most recent conversation
        const mostRecentConversation = conversations[0];
        loadConversation(mostRecentConversation.id);
        
        // If the loaded conversation has no messages, show the welcome screen
        if (mostRecentConversation.messages.length === 0) {
            document.getElementById('welcome-container').style.display = 'flex';
        }
    }
    
    // Thêm tải đánh giá vào quá trình khởi tạo
    loadRating();
});