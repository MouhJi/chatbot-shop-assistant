const express = require('express');
const app = express();
const port = 3000;

require('dotenv').config();

const bodyParser = require('body-parser');
const cookiesParser = require('cookie-parser');
const cors = require('cors');
const path = require('path');

app.use(cors({ origin: process.env.CLIENT_URL, credentials: true }));

const connectDB = require('./config/connect');
const routes = require('./routes/index');
const chatRouter = require('./routes/chat');

app.use(express.static(path.join(__dirname, '../src')));
app.use(cookiesParser());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.use('/api/chat', chatRouter);

routes(app);

connectDB();

app.use((err, req, res, next) => {
    const statusCode = err.statusCode || 500;
    res.status(statusCode).json({
        success: false,
        message: err.message || 'Lỗi server',
    });
});

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`);
});
