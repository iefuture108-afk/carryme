// Meta Webhook Verification Endpoint
app.get('/webhook', (req, res) => {
    const VERIFY_TOKEN = "MY_CARRYME_SECRET_TOKEN_123";
    
    // Parse the query params
    let mode = req.query['hub.mode'];
    let token = req.query['hub.verify_token'];
    let challenge = req.query['hub.challenge'];

    // Checks if a token and mode is in the query string of the request
    if (mode && token) {
        if (mode === 'subscribe' && token === VERIFY_TOKEN) {
            console.log('WEBHOOK_VERIFIED');
            res.status(200).send(challenge);
        } else {
            res.sendStatus(403);
        }
    }
});

// Post endpoint to receive events (Leads/Messages)
app.post('/webhook', (req, res) => {
    let body = req.body;
    console.log('Received Event:', JSON.stringify(body, null, 2));
    res.status(200).send('EVENT_RECEIVED');
});
