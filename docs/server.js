const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const port = process.env.PORT || 4000;

app.use(
    '/api/v1/run',
    createProxyMiddleware({
        target: 'https://cheese-agent.onrender.com:10000',
        changeOrigin: true,
        pathRewrite: {
            '^/api/v1/run': '/api/v1/run'
        },
    })
);

app.use(express.static(__dirname));

app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(port, () => {
    console.log(`🟢 Server listening on port ${port}`);
});
