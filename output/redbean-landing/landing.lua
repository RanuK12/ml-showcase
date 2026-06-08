-- /.init.lua — Redbean landing page server
-- Landing page con formulario de contacto + SQLite para guardar leads
-- Uso: zip redbean.com index.html style.css /.init.lua launch.lua
--      ./redbean.com

-- ============================================================
-- CONFIG
-- ============================================================
-- El puerto se configura con ./redbean.com -p 8080
-- (Redbean lee el puerto por flag, no por variable Lua)
local DB_NAME = "leads.db"

-- ============================================================
-- DATABASE — SQLite para persistir leads
-- ============================================================
function init_db()
    db = sqlite3.open(DB_NAME)
    db:exec([[
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now'))
        );
    ]])
end

function save_lead(name, email, message)
    local stmt = db:prepare(
        "INSERT INTO leads (name, email, message) VALUES (?, ?, ?)"
    )
    stmt:bind_values(name, email, message)
    stmt:step()
    stmt:finalize()
end

function get_leads()
    local leads = {}
    for row in db:nrows("SELECT * FROM leads ORDER BY id DESC LIMIT 50") do
        table.insert(leads, row)
    end
    return leads
end

-- ============================================================
-- ROUTES
-- ============================================================
function OnHttpRequest()
    local path = GetPath()
    local method = GetMethod()

    -- Inicializar DB en primer request
    if not db then init_db() end

    -- Ruta: formulario de contacto (POST)
    if path == "/api/contact" and method == "POST" then
        local body = ReadBody()
        local params = {}
        for k, v in body:gmatch("([^&=]+)=([^&]*)") do
            -- URL decode básico
            v = v:gsub("%%2B", "+"):gsub("%%20", "+"):gsub("%%40", "@")
            params[k] = v
        end

        local name = params.name or ""
        local email = params.email or ""
        local message = params.message or ""

        if name ~= "" and email ~= "" and email:match("@") then
            save_lead(name, email, message)
            SetHeader("Content-Type", "text/html")
            Write([[
<!DOCTYPE html><html><head>
<link rel="stylesheet" href="/style.css">
</head><body>
<div class="container success">
  <h1>✅ ¡Gracias, ]] .. EscapeHtml(name) .. [[!</h1>
  <p>Tu mensaje fue enviado. Te contactaremos pronto.</p>
  <a href="/" class="btn">← Volver</a>
</div>
</body></html>
            ]])
        else
            SetHeader("Content-Type", "text/html")
            Write([[
<!DOCTYPE html><html><head>
<link rel="stylesheet" href="/style.css">
</head><body>
<div class="container error">
  <h1>❌ Error</h1>
  <p>Nombre y email válido son requeridos.</p>
  <a href="/" class="btn">← Intentar de nuevo</a>
</div>
</body></html>
            ]])
        end
        return
    end

    -- Ruta: dashboard de leads (solo local)
    if path == "/leads" then
        local client_ip = GetRemoteAddr()
        -- Permitir solo desde localhost
        if client_ip ~= "127.0.0.1" and client_ip ~= "::1" then
            SetStatus(403, "Forbidden")
            Write("Solo acceso local")
            return
        end

        local leads = get_leads()
        SetHeader("Content-Type", "text/html")
        Write([[<!DOCTYPE html><html><head>
<link rel="stylesheet" href="/style.css">
<title>Leads Dashboard</title>
</head><body>
<div class="container">
  <h1>📋 Leads Capturados (]] .. #leads .. [[)</h1>
  <table class="leads-table">
    <tr><th>#</th><th>Nombre</th><th>Email</th><th>Mensaje</th><th>Fecha</th></tr>]])
        for i, lead in ipairs(leads) do
            Write("<tr><td>" .. i .. "</td><td>" .. EscapeHtml(lead.name) ..
                  "</td><td>" .. EscapeHtml(lead.email) ..
                  "</td><td>" .. EscapeHtml(lead.message or "") ..
                  "</td><td>" .. (lead.created_at or "") .. "</td></tr>")
        end
        Write("</table><br><a href='/' class='btn'>← Landing</a></div></body></html>")
        return
    end

    -- Ruta raíz: servir landing page
    if path == "/" then
        ServeFile("/index.html")
        return
    end

    -- Cualquier otro archivo estático
    ServeAsset()
end

-- ============================================================
-- STARTUP — se ejecuta al cargar .init.lua
-- ============================================================
Log("🚀 Landing server listo. Rutas:")
Log("   → http://localhost:8080/          (landing)")
Log("   → http://localhost:8080/leads     (dashboard, solo local)")
Log("   → POST /api/contact               (formulario)")
Log("   Puerto: cambiar con ./redbean.com -p <puerto>")
