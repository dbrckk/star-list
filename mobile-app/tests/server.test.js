'use strict';
const {test,after}=require('node:test');
const assert=require('node:assert/strict');
const {spawn} = require('node:child_process');
const fs=require('node:fs');const os=require('node:os');const path=require('node:path');const net=require('node:net');
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'freebuff-mobile-test-'));
process.env.FREEBUFF_MOBILE_HOME=path.join(temp,'profile');
const {safeRepo,safeId,idFor,session} = require('../server');
let serverProcess;let port;let pin;let token;
const base=()=>`http://127.0.0.1:${port}`;
const req=async(uri,opts={})=>fetch(base()+uri,opts);
async function waitFor(text,proc){return new Promise((resolve,reject)=>{let buf='';let timeout=setTimeout(()=>reject(Error('Démarrage expiré : '+buf)),6000);const onData=chunk=>{buf+=chunk.toString();const found=buf.match(/CODE D'APPAIRAGE \(20 minutes\) : (\d{6})/);if(found){clearTimeout(timeout);proc.stdout.off('data',onData);resolve(found[1])}};proc.stdout.on('data',onData);proc.once('exit',code=>reject(Error('Serveur terminé : '+code)));})}
async function getPort(){let s=net.createServer();await new Promise(r=>s.listen(0,'127.0.0.1',r));let p=s.address().port;await new Promise(r=>s.close(r));return p;}
after(()=>{if(serverProcess)serverProcess.kill();fs.rmSync(temp,{recursive:true,force:true});});
test('Validation des identifiants GitHub et absence de traversée',()=>{
 for(let val of ['alice/project','dbrckk/star-list','A-B/name_1'])assert(safeRepo(val),val);
 for(let val of ['../etc','a/../../etc','https://github.com/a/b','a/.','a/..','a/b/c','-a/b','x;y/z','a/🤖'])assert(!safeRepo(val),val);
 assert.equal(idFor('alice/project'),'alice__project');assert.equal(safeId('alice__project'),true);assert.equal(safeId('../etc'),false);assert.equal(session('a__b'),session('a__b'));assert.notEqual(session('a__b'),session('b__a'));
});
test('Serveur local : appairage, API auth, validation et protection origine',async()=>{
 port=await getPort();serverProcess=spawn(process.execPath,[path.join(__dirname,'../server.js')],{env:{...process.env,FREEBUFF_MOBILE_PORT:String(port)},stdio:['ignore','pipe','pipe']});pin=await waitFor('PIN',serverProcess);
 let page=await req('/');assert.equal(page.status,200);assert.match(await page.text(),/Freebuff Mobile/);
 let manifest=await req('/manifest.webmanifest');assert.equal(manifest.status,200);
 let unauthorized=await req('/api/status');assert.equal(unauthorized.status,401);
 let forbidden=await req('/api/pair',{method:'POST',headers:{origin:'https://evil.example','content-type':'application/json'},body:JSON.stringify({code:pin})});assert.equal(forbidden.status,403);
 let bad=await req('/api/pair',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({code:'123450'})});assert.equal(bad.status,401);
 let pair=await req('/api/pair',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({code:pin})});assert.equal(pair.status,200);token=(await pair.json()).token;assert.equal(token.length,64);
 let replay=await req('/api/pair',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({code:pin})});assert.equal(replay.status,429);
 let status=await req('/api/status',{headers:{Authorization:'Bearer '+token}});assert.equal(status.status,200);let info=await status.json();assert(Array.isArray(info.projects));
 let inj=await req('/api/projects',{method:'POST',headers:{Authorization:'Bearer '+token,'content-type':'application/json'},body:JSON.stringify({repo:'a/../../../etc'})});assert.equal(inj.status,400);
 let invalid=await req('/api/open',{method:'POST',headers:{Authorization:'Bearer '+token,'content-type':'application/json'},body:JSON.stringify({id:'../../tmp'})});assert.equal(invalid.status,400);
 let secret=await req('/token');assert.equal(secret.status,404);
 assert.equal(fs.statSync(path.join(temp,'profile','token')).mode&0o777,0o600);
});
