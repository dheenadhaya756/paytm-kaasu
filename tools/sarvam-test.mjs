// One Sarvam chat call to prove the key works. Run: node --env-file=.env tools/sarvam-test.mjs
import { SarvamAIClient } from "sarvamai";

const client = new SarvamAIClient({ apiSubscriptionKey: process.env.SARVAM_API_KEY });
const response = await client.chat.completionsV2({
  model: "sarvam-105b-conversations",
  messages: [{ role: "user", content: "Say hello to a kirana shopkeeper in Chennai in one short Tamil sentence." }],
  max_tokens: 400,   // small cap so the test costs almost nothing
});
console.log(response.choices[0].message.content);
console.log("tokens used:", JSON.stringify(response.usage ?? {}));
