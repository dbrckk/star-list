'use strict';
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const crypto = require('node:crypto');
const {spawn, spawnSync} = require('node:child_process');
const ROOT = process.env.FREEBUFF_MOBILE_HOME || path.join(os.homedir(), '.freebuff-mobile');
const PROJECTS = path.join(ROOT, 'projects');
const PUBLIC = path.join(__dirname, 'www');
const PORT = Number(process.env.FREEBUFF_MOBILE_PORT || 8765);
const SERVER_ORIGIN = `http://127.0.0.1:${PORT}`;
fs.mkdirSync(PROJECTS,{recursive:true,mode:0o700});
fs.chmodSync(ROOT,0o700);
const tokenPath = path.join(ROOT,'token');
if (!fs.existsSync(tokenPath)) fs.writeFileSync(tokenPath, crypto.randomBytes(32).toString('hex'),{mode:0o600,flag:'wx'});
const AUTH = fs.readFileSync(tokenPath,'utf8').trim();
let PIN = String(crypto.randomInt(100000,999999));
let expires = Date.now()+20*60*1000;
let pairFailures=0;
const tasks = new Map();
// Checking `freebuff --version` on every dashboard poll can trigger the
// Android wrapper's network/update path. Test executable presence instead.
const has = c => (process.env.PATH||'').split(path.delimiter).some(dir => {
  if(!dir)return false;
  try{const file=path.join(dir,c);const st=fs.statSync(file);return st.isFile()&&Boolean(st.mode&0o111)}catch{return false}
});
const output = (command,args,opts={})=>{
  const r=spawnSync(command,args,{encoding:'utf8',timeout:opts.timeout||8000,maxBuffer:1024*1024,...opts});
  return {ok:r.status===0, stdout:(r.stdout||'').slice(-22000),stderr:(r.stderr||'').slice(-3000),code:r.status};
};
const safeRepo = r => typeof r==='string' && r.length<150 && /^(?!\.{1,2}\/)[a-z0-9][a-z0-9._-]{0,38}\/(?!\.{1,2}$)[a-z0-9][a-z0-9._-]{0,99}$/i.test(r);
const idFor=r=>r.replace('/','__');
const safeId=id=>typeof id==='string' && /^[a-z0-9._-]+__[a-z0-9._-]+$/i.test(id)&&!id.includes('..');
const projectDir=id=>{if(!safeId(id))throw Error('Identifiant de projet invalide'); return path.join(PROJECTS,id);};
const session=id=>'fb-'+crypto.createHash('sha256').update(id).digest('hex').slice(0,16);
const response=(res,status,data)=>{const content=JSON.stringify(data);res.writeHead(status,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});res.end(content)};
const listProjects=()=>fs.readdirSync(PROJECTS,{withFileTypes:true}).filter(d=>d.isDirectory()&&safeId(d.name)).map(d=>{let id=d.name, running=output('tmux',['has-session','-t',session(id)],{timeout:1500}).ok;return {id,name:id.replace('__','/'),running};});
const tasksFor=()=>Array.from(tasks.entries()).map(([id,t])=>({id,state:t.state,detail:t.detail}));
async function readBody(req){return new Promise((resolve,reject)=>{let bytes=0,chunks=[];req.on('data',c=>{bytes+=c.length;if(bytes>16384){reject(Error('Requête trop volumineuse'));req.destroy();}else chunks.push(c)});req.on('end',()=>{try{resolve(JSON.parse(Buffer.concat(chunks).toString('utf8')||'{}'))}catch(e){reject(Error('JSON invalide'))}});req.on('error',reject);});}
const files = {'/':'index.html','/index.html':'index.html','/app.js':'app.js','/style.css':'style.css','/manifest.webmanifest':'manifest.webmanifest','/icon.svg':'icon.svg'};
const types={'.html':'text/html','.js':'text/javascript','.css':'text/css','.webmanifest':'application/manifest+json','.svg':'image/svg+xml'};
function staticFile(res,pathname){const file=files[pathname];if(!file){res.writeHead(404);return res.end('Introuvable')};let content=fs.readFileSync(path.join(PUBLIC,file));res.writeHead(200,{'Content-Type':types[path.extname(file)]+'; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Content-Security-Policy':"default-src 'self'; connect-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; base-uri 'none'; object-src 'none'; frame-ancestors 'none'",'Referrer-Policy':'no-referrer'});res.end(content)}
function createClone(repo){let id=idFor(repo),target=projectDir(id);if(fs.existsSync(target))throw Error('Ce dépôt est déjà présent');const task={state:'cloning',detail:'Clonage en cours'};tasks.set(id,task);
 const proc=spawn('git',['clone','--depth','1',`https://github.com/${repo}.git`,target],{stdio:['ignore','pipe','pipe'],env:{...process.env,GIT_TERMINAL_PROMPT:'0'}});
 let error='';proc.stderr.on('data',d=>error=(error+d).slice(-1500));proc.on('error',e=>{task.state='error';task.detail=e.message;});proc.on('close',code=>{if(code===0){task.state='done';task.detail='Projet prêt';}else {task.state='error';task.detail=(error||'Clonage impossible').slice(-300); if(fs.existsSync(target))fs.rmSync(target,{recursive:true,force:true});}});return {id,state:task.state};}
function ensureSession(id){const dir=projectDir(id);if(!fs.existsSync(path.join(dir,'.git')))throw Error('Projet incomplet ou absent'); if(!has('tmux'))throw Error('tmux absent');if(!has('freebuff'))throw Error('Moteur Freebuff absent. Installe-le depuis Termux.');let name=session(id);if(!output('tmux',['has-session','-t',name]).ok){let r=output('tmux',['new-session','-d','-s',name,'-c',dir,'freebuff']);if(!r.ok)throw Error(r.stderr||'Impossible de démarrer Freebuff');}return {id,session:name}}
function terminalOutput(id){let name=session(id); if(!output('tmux',['has-session','-t',name]).ok)return {running:false,screen:'La session est arrêtée.'};let r=output('tmux',['capture-pane','-p','-J','-S','-180','-t',name]);return {running:true,screen:r.stdout.replace(/\x1b\[[0-?]*[ -/]*[@-~]/g,'').replace(/\x1b\][^\x07]*(?:\x07|\x1b\\)/g,'').slice(-18000)};}
function sendKeys(id,text,key){let name=session(id);if(!output('tmux',['has-session','-t',name]).ok)throw Error('Session inactive');if(text!==undefined){if(typeof text!=='string'||text.length>4000||text.includes('\u0000'))throw Error('Message invalide');const r=output('tmux',['send-keys','-l','-t',name,'--',text]);if(!r.ok)throw Error(r.stderr||'Envoi impossible');output('tmux',['send-keys','-t',name,'Enter']);}
else {const allowed=new Set(['Enter','Escape','Up','Down','Left','Right','Tab','BSpace','C-c','Space','y','n']);if(!allowed.has(key))throw Error('Touche invalide'); const r=output('tmux',['send-keys','-t',name,key]);if(!r.ok)throw Error('Touche non envoyée');}return {ok:true};}
const app = http.createServer(async(req,res)=>{
 try{const url=new URL(req.url,SERVER_ORIGIN);if(!['127.0.0.1','localhost'].includes((req.headers.host||'').split(':')[0]))return response(res,403,{error:'Hôte invalide'});
 if(req.headers.origin && req.headers.origin!==SERVER_ORIGIN)return response(res,403,{error:'Origine non autorisée'});
 if(req.method==='GET' && !url.pathname.startsWith('/api/'))return staticFile(res,url.pathname);
 if(url.pathname==='/api/pair' && req.method==='POST'){const body=await readBody(req);if(pairFailures>=8||Date.now()>expires)return response(res,429,{error:'Code expiré ou tentatives dépassées. Redémarre le serveur.'});if(typeof body.code!=='string'||body.code!==PIN){pairFailures++;return response(res,401,{error:'Code incorrect'});}PIN='';expires=0;return response(res,200,{token:AUTH});}
 const bearer=req.headers.authorization||'';const token=bearer.startsWith('Bearer ')?bearer.slice(7):'';if(token.length!==AUTH.length||!crypto.timingSafeEqual(Buffer.from(token),Buffer.from(AUTH)))return response(res,401,{error:'Appairage requis'});
 const body=req.method==='POST'?await readBody(req):{};
 let result;
 switch(`${req.method} ${url.pathname}`){
 case 'GET /api/status':result={node:process.version,git:has('git'),tmux:has('tmux'),freebuff:has('freebuff'),version:'',projects:listProjects(),tasks:tasksFor()};break;
 case 'POST /api/projects':if(!safeRepo(body.repo))throw Error('Format attendu : propriétaire/dépôt');result=createClone(body.repo);break;
 case 'POST /api/open':result=ensureSession(body.id);break;
 case 'GET /api/screen':result=terminalOutput(url.searchParams.get('id'));break;
 case 'POST /api/input':result=sendKeys(body.id,body.text,undefined);break;
 case 'POST /api/key':result=sendKeys(body.id,undefined,body.key);break;
 case 'POST /api/stop':if(!safeId(body.id))throw Error('Projet invalide');result={ok:output('tmux',['kill-session','-t',session(body.id)]).ok};break;
 default:return response(res,404,{error:'Route inconnue'});
 }
 response(res,200,result);
 }catch(e){response(res,400,{error:e.message||'Erreur interne'});}
});
if(require.main===module){app.listen(PORT,'127.0.0.1',()=>{console.log(`Freebuff Mobile : ${SERVER_ORIGIN}`);if(PIN)console.log(`CODE D'APPAIRAGE (20 minutes) : ${PIN}`);console.log('Aucune écoute réseau externe. Aucune télémétrie.');});}
module.exports={app,safeRepo,safeId,idFor,session,PROJECTS};
