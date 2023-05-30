const express = require('express')
const { Configuration, OpenAIApi } = require("openai");
const configuration = new Configuration({
  apiKey: "your_openai_api_key",
});
const openai = new OpenAIApi(configuration);
const app = express()
const port = 3000
const bodyParser = require('body-parser');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false}));
app.use(express.static("static"));

app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
app.engine('html', require('ejs').renderFile);

app.get('/', (req, res) => {
  res.render('index.html');
})

app.post('/completion', (req, res) => {
    var q = req.body.prompt;
    console.log(q)
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Connection', 'keep-alive');
    res.flushHeaders();

    const response = openai.createCompletion({
        model: "text-davinci-003",
        prompt: q,
        max_tokens: 1000,
        temperature: 0.5, // 1에 가까울수록 답변의 창의성이 증가
        stream: true,
    }, { responseType: 'stream' });

    response.then(resp => {
        resp.data.on('data', data => {
            const lines = data.toString().split('\n').filter(line => line.trim() !== '');
            for (const line of lines) {
                const message = line.replace(/^data: /, '');
                if (message === '[DONE]') {
                    res.end();
                    return
                }
                const parsed = JSON.parse(message);
                console.log(parsed.choices[0].text);
                res.write(parsed.choices[0].text);
            }
        });
    })
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})