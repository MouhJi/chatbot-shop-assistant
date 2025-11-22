const express = require('express');
const axios = require('axios');
const router = express.Router();

const RAG_SERVER_URL = process.env.RAG_SERVER_URL || 'http://localhost:8000';

router.post('/', async (req, res) => {
    try {
        const { question } = req.body;
        
        if (!question) {
            return res.status(400).json({ error: 'Question is required' });
        }

        // Forward to RAG server
        const response = await axios.post(`${RAG_SERVER_URL}/rag/query`, {
            question
        });

        res.json(response.data);
    } catch (error) {
        console.error('Error forwarding to RAG server:', error.message);
        if (error.response) {
            res.status(error.response.status).json(error.response.data);
        } else {
            res.status(500).json({ error: 'Internal Server Error' });
        }
    }
});

module.exports = router;
