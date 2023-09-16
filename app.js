class Chatbox {
    constructor() {
        this.args = {
            chatBox: document.querySelector('.isi_chatbox'),
            sendButton: document.querySelector('.button_send'),
        }

        this.state = false;
        this.messages = [];
    }

    display() {
        const { chatBox, sendButton } = this.args;

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener('keyup', ({ key }) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    async onSendButton(chatbox) {
        const { sendButton } = this.args;

        var textField = chatbox.querySelector('input')
        let text1 = textField.value
        if (text1 === '') {
            return
        }

        const postToken = btoa(this.generateToken())

        let msg1 = { name: 'User', message: text1 }
        this.messages.push(msg1)
        
        sendButton.classList.add('wait')
        
        await fetch('search.php', {
            method: 'POST',
            body: JSON.stringify({ 
                message: text1,
                token: postToken
            }),
            mode: 'cors',
            headers: { 'Content-Type': 'application/json' }
        })
            .then(r => r.json())
            .then(r => {
                console.log(r)
                if (r.code === 200) {
                    let msg2 = { name: 'Tasiah', message: r.message }
                    this.messages.push(msg2)
                    this.updateChatText(chatbox)
                    textField.value = ''
                } else {
                    alert(r.message)
                }
            }).catch(err => {
                console.error('Error: ', err)
                this.updateChatText(chatbox)
                textField.value = ''
            });
        
        sendButton.classList.remove('wait')
    }

    updateChatText(chatbox) {
        var html = ''
        this.messages.slice().reverse().forEach(function (item) {
            if (item.name === 'Tasiah') {
                html += '<div class="item_messages item_messages_visitor">' + item.message + '</div>'
            } else {
                html += '<div class="item_messages item_messages_operator">' + item.message + '</div>'
            }
        })

        const chatMessage = chatbox.querySelector('.messages_chatbox')
        chatMessage.innerHTML = html
    }

    generateToken() {
        let result = '';
        const tasiahKey = ['t','a','s','i','a','h'];
        const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        const charactersLength = characters.length;
        let counter = 0;
        while (counter < 6) {
            result += characters.charAt(Math.floor(Math.random() * charactersLength));
            result += characters.charAt(Math.floor(Math.random() * charactersLength));
            result += tasiahKey[counter]
            counter += 1;
        }
        return result;
    }
}

const chatbox = new Chatbox()
chatbox.display()