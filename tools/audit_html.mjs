import fs from 'node:fs';
import vm from 'node:vm';
const file=new URL('../REALITY_BRIDGE_ALIEN_CONDUCTOR_III_SOUND_FIXED.html',import.meta.url);
const html=fs.readFileSync(file,'utf8');
const ids=[...html.matchAll(/\bid=["']([^"']+)["']/g)].map(m=>m[1]);
const dup=[...new Set(ids.filter((x,i)=>ids.indexOf(x)!==i))];
if(dup.length) throw new Error('duplicate ids: '+dup.join(', '));
if(/\sonclick\s*=/.test(html)) throw new Error('inline onclick handlers found');
const lookups=[...html.matchAll(/\$\(['"]([^'"]+)['"]\)/g)].map(m=>m[1]);
const missing=[...new Set(lookups.filter(x=>!ids.includes(x)))];
if(missing.length) throw new Error('missing literal DOM ids: '+missing.join(', '));
const scripts=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)].map(m=>m[1]);
for(const [i,js] of scripts.entries()){if(js.trim())new vm.Script(js,{filename:`inline-${i}.js`});}
console.log(JSON.stringify({file:file.pathname,ids:ids.length,duplicateIds:dup.length,literalLookups:lookups.length,missingLookups:missing.length,scripts:scripts.length},null,2));
