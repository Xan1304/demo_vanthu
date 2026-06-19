const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const axios = require('axios');
require('dotenv').config();

const app = express();
app.use(express.json());

const PORT = 3000;
const FLASK_URL = process.env.FLASK_URL || 'http://localhost:5000';

let isConnected = false;
// message_id -> doc_id
const messageMap = new Map();
// phone_number -> last_doc_id (để dễ map reply nếu người dùng không quote)
const lastDocMap = new Map();

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

client.on('qr', (qr) => {
    console.log('Quét mã QR để đăng nhập WhatsApp:');
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('✅ WhatsApp đã kết nối');
    isConnected = true;
});

client.on('disconnected', (reason) => {
    console.log('❌ WhatsApp đã ngắt kết nối:', reason);
    isConnected = false;
});

client.on('message_create', async msg => {
    const text = msg.body.trim().toUpperCase();
    
    // Bỏ qua tất cả tin nhắn không phải lệnh của hệ thống để tránh loop
    if (!text.startsWith('OK ') && !text.startsWith('SỬA ') && text !== 'BỎ') {
        return; 
    }

    let doc_id = null;

    // Tìm doc_id từ tin nhắn bị quote hoặc tin nhắn cuối cùng gửi cho sđt này
    if (msg.hasQuotedMsg) {
        const quotedMsg = await msg.getQuotedMessage();
        if (quotedMsg && quotedMsg.id && quotedMsg.id._serialized) {
            doc_id = messageMap.get(quotedMsg.id._serialized);
        }
    }
    
    if (!doc_id) {
        // Fallback: Nếu tự nhắn tin cho chính mình (To == From) thì lấy sđt của mình
        const targetPhone = msg.to === msg.from ? msg.to : msg.from;
        doc_id = lastDocMap.get(targetPhone);
    }

    if (!doc_id) {
        return; // Không biết là reply cho thư nào
    }

    let action = '';
    let mau_index = -1;
    let ten = '';

    if (text.startsWith('OK ')) {
        const num = parseInt(text.split(' ')[1]);
        if (!isNaN(num) && num >= 1 && num <= 5) {
            action = 'confirm';
            mau_index = num - 1;
        }
    } else if (text.startsWith('SỬA CT ')) {
        action = 'change_ct';
        ten = msg.body.trim().substring(7);
    } else if (text.startsWith('SỬA PH ')) {
        action = 'change_ph';
        ten = msg.body.trim().substring(7);
    } else if (text === 'BỎ') {
        action = 'skip';
    }

    if (action) {
        try {
            await axios.post(`${FLASK_URL}/confirm`, {
                doc_id: doc_id,
                action: action,
                mau_index: mau_index,
                ten: ten
            });
        } catch (error) {
            console.error('Lỗi khi gửi confirm lên Flask:', error.message);
            msg.reply('❌ Có lỗi kết nối đến hệ thống chính.');
        }
    } else {
        msg.reply('❓ Không hiểu. Vui lòng reply: OK [số], SỬA CT [tên], SỬA PH [tên], hoặc BỎ');
    }
});

client.initialize();

app.post('/send', async (req, res) => {
    if (!isConnected) {
        return res.status(500).json({ success: false, error: 'WhatsApp chưa kết nối' });
    }

    const { phone, message, doc_id } = req.body;
    if (!phone || !message || !doc_id) {
        return res.status(400).json({ success: false, error: 'Thiếu tham số' });
    }

    try {
        let cleanPhone = phone.startsWith('+') ? phone.substring(1) : phone;
        const chatId = cleanPhone.includes('@c.us') ? cleanPhone : `${cleanPhone}@c.us`;
        const response = await client.sendMessage(chatId, message);
        const message_id = response.id._serialized;
        
        messageMap.set(message_id, doc_id);
        lastDocMap.set(chatId, doc_id);
        
        res.json({ success: true, message_id });
    } catch (error) {
        console.error('Lỗi gửi tin nhắn WA:', error.stack || error);
        res.status(500).json({ success: false, error: error.message || error });
    }
});

app.get('/status', (req, res) => {
    res.json({ connected: isConnected });
});

app.listen(PORT, () => {
    console.log(`WhatsApp Server đang chạy trên port ${PORT}`);
});
