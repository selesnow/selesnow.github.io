// Stand-in for OpenRouter during local checks: node test/mock-openrouter.mjs  (port 8799).
// Streams a fixed answer in the OpenAI chunk format and prints what the worker sent.
// A question containing "429" or "500" gets that HTTP status instead.
import http from 'node:http';

const ANSWER = 'Установите AcpGram **одной командой**:\n\n```sh\nnpm install -g acpgram\n```\n\n1. Создайте бота в `@BotFather`.\n2. Запустите `acpgram`.\n\nПодробнее: [Установка](#install), [Нет такого раздела](#no-such-section).';

http.createServer((req, res) => {
  let body = '';
  req.on('data', (chunk) => { body += chunk; });
  req.on('end', async () => {
    const payload = JSON.parse(body || '{}');
    const messages = payload.messages || [];
    const question = messages[messages.length - 1]?.content || '';
    console.log(JSON.stringify({
      path: req.url, auth: req.headers.authorization, model: payload.model, max_tokens: payload.max_tokens,
      roles: messages.map((m) => m.role), systemChars: messages[0]?.content.length, systemStart: messages[0]?.content.slice(0, 60),
      hasDocs: /\{#install\}/.test(messages[0]?.content || ''), question,
    }));
    const status = question.match(/\b(429|500)\b/)?.[1];
    if (status) { res.writeHead(Number(status), { 'content-type': 'application/json' }); res.end('{"error":{"message":"mock"}}'); return; }
    res.writeHead(200, { 'content-type': 'text/event-stream' });
    res.write(': OPENROUTER PROCESSING\n\n');
    for (const piece of ANSWER.match(/[\s\S]{1,9}/g)) {
      res.write(`data: ${JSON.stringify({ choices: [{ delta: { content: piece } }] })}\n\n`);
      await new Promise((r) => setTimeout(r, 25));
    }
    res.end('data: [DONE]\n\n');
  });
}).listen(8799, () => console.log('mock OpenRouter: http://127.0.0.1:8799'));
