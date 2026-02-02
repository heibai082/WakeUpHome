import sqlite3, datetime, os, shutil, httpx
from fastapi import FastAPI, Body, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(); db_path = '/opt/WakeUpHome/db/data.db'
L_DIR = '/opt/WakeUpHome/logs'; S_LOG = f"{L_DIR}/success.log"; E_LOG = f"{L_DIR}/error.log"
os.makedirs('/opt/WakeUpHome/static/avatars', exist_ok=True)
app.mount("/static", StaticFiles(directory="/opt/WakeUpHome/static"), name="static")

def init_db():
    conn = sqlite3.connect(db_path); c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS config (key TEXT PRIMARY KEY, val TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS barcodes (code TEXT PRIMARY KEY, name TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, parent_id INTEGER DEFAULT 0)')
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT, avatar_url TEXT)')
    c.execute('INSERT OR IGNORE INTO users (username, password, role) VALUES ("admin", "admin", "super_admin")')
    conn.commit(); conn.close()
init_db()

def write_log(msg, is_err=False):
    os.makedirs(L_DIR, exist_ok=True); p = E_LOG if is_err else S_LOG
    with open(p, 'a', encoding='utf-8') as f: f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")

@app.get('/api/barcode/{code}')
async def get_bc(code: str):
    db = sqlite3.connect(db_path); r = db.execute("SELECT name FROM barcodes WHERE code=?", (code,)).fetchone(); db.close()
    return {"name": r[0] if r else ""}

@app.post('/api/add_item')
async def add_i(d: dict = Body(...)):
    db = sqlite3.connect(db_path); now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if d.get('bc') and d['name']: db.execute("INSERT OR REPLACE INTO barcodes VALUES (?,?)", (d['bc'], d['name']))
    db.execute('INSERT INTO items (category_id, name, qty, expire_date, prod_date, notify_lead_days, created_at) VALUES (?,?,?,?,?,?,?)', 
               (d['cat_id'], d['name'], d['qty'], d['expire'], d.get('prod',''), d.get('lead',3), now))
    db.commit(); db.close(); write_log(f"【入库】{d['name']} {d['qty']}个"); return {'ok': True}

@app.post('/api/items/manage')
async def m_item(d: dict = Body(...)):
    db = sqlite3.connect(db_path); now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if d['act'] == 'edit':
        db.execute('UPDATE items SET name=?, qty=?, prod_date=?, expire_date=?, notify_lead_days=?, created_at=? WHERE id=?', (d['name'], d['qty'], d['prod'], d['expire'], d['lead'], now, d['id']))
        write_log(f"【修改】物资ID:{d['id']} -> {d['name']}")
    elif d['act'] == 'reduce': db.execute('UPDATE items SET qty = MAX(0, qty - 1), created_at=? WHERE id=?', (now, d['id']))
    elif d['act'] == 'del': db.execute('DELETE FROM items WHERE id=?', (d['id'],))
    db.commit(); db.close(); return {'ok': True}

@app.get('/api/logs')
async def g_logs():
    s = "".join(open(S_LOG, 'r', encoding='utf-8').readlines()[-15:]) if os.path.exists(S_LOG) else "无记录"
    e = "".join(open(E_LOG, 'r', encoding='utf-8').readlines()[-15:]) if os.path.exists(E_LOG) else "无异常"
    return {"success": s, "error": e}

@app.get('/api/recap/test')
async def recap_test():
    db = sqlite3.connect(db_path); db.row_factory = sqlite3.Row; today = datetime.date.today()
    app_n = db.execute("SELECT val FROM config WHERE key='app_name'").fetchone()[0]
    items = db.execute("SELECT name, expire_date, notify_lead_days FROM items").fetchall()
    added = db.execute("SELECT name, qty FROM items WHERE created_at LIKE ?", (f"{(today - datetime.timedelta(days=1)).isoformat()}%",)).fetchall()
    exps = [f"⚠ {i['name']} ({ (datetime.date.fromisoformat(i['expire_date']) - today).days }天过期)" for i in items if 0 <= (datetime.date.fromisoformat(i['expire_date']) - today).days <= int(i['notify_lead_days'])]
    db.close(); msg = f"【入库明细】\n" + ("\n".join([f"· {r[0]}({r[1]}个)" for r in added]) if added else "昨日无入库")
    msg += f"\n\n【精准预警】\n" + ("\n".join(exps) if exps else "运行平稳"); return {"msg": msg, "app_name": app_n}

@app.get('/api/config')
async def g_cf():
    db=sqlite3.connect(db_path); r=db.execute("SELECT key, val FROM config").fetchall(); db.close(); return {x[0]:x[1] for x in r}
@app.post('/api/config')
async def s_cf(d:dict=Body(...)):
    db=sqlite3.connect(db_path); db.execute("INSERT OR REPLACE INTO config (key,val) VALUES (?,?)",(d['key'],d['val'])); db.commit(); db.close(); return {"ok":True}
@app.get('/api/items')
async def g_its(cat_id: int):
    db=sqlite3.connect(db_path); db.row_factory=sqlite3.Row; ids=[cat_id]; subs=db.execute('SELECT id FROM categories WHERE parent_id=?',(cat_id,)).fetchall()
    for s in subs: ids.append(s[0])
    res=db.execute(f"SELECT * FROM items WHERE category_id IN ({','.join(['?']*len(ids))}) ORDER BY name ASC",ids).fetchall(); db.close(); return [dict(r) for r in res]
@app.get('/api/categories')
async def g_cats():
    db=sqlite3.connect(db_path); db.row_factory=sqlite3.Row; r=db.execute('SELECT * FROM categories').fetchall(); db.close(); return [dict(x) for x in r]
@app.post('/api/categories/manage')
async def m_cat(d:dict=Body(...)):
    db=sqlite3.connect(db_path); act=d['act']
    if act=='add': db.execute('INSERT INTO categories (name,parent_id) VALUES (?,?)',(d['name'],d.get('p_id',0)))
    elif act=='del':
        ids=[d['id']]; subs=db.execute('SELECT id FROM categories WHERE parent_id=?',(d['id'],)).fetchall()
        for s in subs: ids.append(s[0])
        for cid in ids: db.execute('DELETE FROM items WHERE category_id=?',(cid,))
        db.execute(f"DELETE FROM categories WHERE id IN ({','.join(['?']*len(ids))})",ids)
    db.commit(); db.close(); return {'ok':True}
@app.get('/api/users')
async def l_us():
    db=sqlite3.connect(db_path); db.row_factory=sqlite3.Row; r=db.execute("SELECT id,username,role,avatar_url FROM users").fetchall(); db.close(); return [dict(x) for x in r]
@app.post('/api/users/manage')
async def m_u(d:dict=Body(...)):
    db=sqlite3.connect(db_path); c=db.cursor(); act=d['act']
    if act=='add': c.execute("INSERT INTO users (username,password,role) VALUES (?,'admin','member')",(d['username'],))
    elif act=='del': c.execute("DELETE FROM users WHERE id=?",(d['id'],))
    db.commit(); db.close(); return {"ok":True}
@app.get('/')
async def idx(): return HTMLResponse(open('/opt/WakeUpHome/index.html').read())
