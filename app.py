# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
app.secret_key = "sgm-municipalidad-guatemala-2026"


# ── Datos en memoria (persisten durante la sesión del servidor) ────────────────
USERS = {
    "ciudadano@gmail.com":  {"password":"1234","role":"ciudadano",  "name":"María González",      "dpi":"2456789012345","activo":True},
    "funcionario@muni.gt":  {"password":"1234","role":"funcionario","name":"Lic. Pedro Cifuentes", "depto":"Urbanismo",  "activo":True},
    "admin@muni.gt":        {"password":"1234","role":"admin",      "name":"Ing. Carlos Méndez",  "depto":"Sistemas",   "activo":True},
    "director@muni.gt":     {"password":"1234","role":"director",   "name":"Lic. Roberto Álvarez","depto":"Alcaldía",   "activo":True},
}

TRAMITES_TIPOS = [
    {"id":1,"nombre":"Licencia de Construcción", "costo":850.00, "dias":15,"icono":"🏗️"},
    {"id":2,"nombre":"Constancia de Vecindad",   "costo":25.00,  "dias":2, "icono":"📄"},
    {"id":3,"nombre":"Permiso de Operación",     "costo":500.00, "dias":10,"icono":"🏪"},
    {"id":4,"nombre":"Certificación Catastral",  "costo":150.00, "dias":5, "icono":"🗺️"},
    {"id":5,"nombre":"Licencia de Anuncio",      "costo":300.00, "dias":7, "icono":"📢"},
    {"id":6,"nombre":"Desmembración de Terreno", "costo":1200.00,"dias":20,"icono":"📐"},
]

SOLICITUDES = [
    {"id":"EXP-2026-001","tipo":"Licencia de Construcción","ciudadano":"María González",  "email":"ciudadano@gmail.com","estado":"En Revisión","fecha":"02/06/2026","monto":850.00, "pagado":False,"resolucion":""},
    {"id":"EXP-2026-002","tipo":"Constancia de Vecindad",  "ciudadano":"María González",  "email":"ciudadano@gmail.com","estado":"Aprobado",   "fecha":"01/06/2026","monto":25.00,  "pagado":True, "resolucion":"Documentación completa y en orden."},
    {"id":"EXP-2026-003","tipo":"Permiso de Operación",    "ciudadano":"Ana López",        "email":"otro@gmail.com",     "estado":"Pendiente",  "fecha":"03/06/2026","monto":500.00, "pagado":False,"resolucion":""},
    {"id":"EXP-2026-004","tipo":"Certificación Catastral", "ciudadano":"Pedro Castillo",   "email":"otro2@gmail.com",    "estado":"Rechazado",  "fecha":"30/05/2026","monto":150.00, "pagado":False,"resolucion":"Plano de ubicación ilegible. Reingrese con documento claro."},
    {"id":"EXP-2026-005","tipo":"Licencia de Anuncio",     "ciudadano":"Roberto Lima",     "email":"otro3@gmail.com",    "estado":"Aprobado",   "fecha":"29/05/2026","monto":300.00, "pagado":True, "resolucion":"Aprobado conforme a reglamento."},
    {"id":"EXP-2026-006","tipo":"Desmembración de Terreno","ciudadano":"Sofía Morales",    "email":"otro4@gmail.com",    "estado":"En Revisión","fecha":"04/06/2026","monto":1200.00,"pagado":False,"resolucion":""},
    {"id":"EXP-2026-007","tipo":"Licencia de Construcción","ciudadano":"Carlos Vásquez",   "email":"otro5@gmail.com",    "estado":"Pendiente",  "fecha":"05/06/2026","monto":850.00, "pagado":False,"resolucion":""},
    {"id":"EXP-2026-008","tipo":"Constancia de Vecindad",  "ciudadano":"Luisa Hernández",  "email":"otro6@gmail.com",    "estado":"Aprobado",   "fecha":"28/05/2026","monto":25.00,  "pagado":True, "resolucion":"Vecindad confirmada."},
]

KPI = {
    "tramites_hoy":24,"tramites_mes":312,"ingresos_mes":187450.00,
    "tiempo_promedio":4.2,"satisfaccion":84.6,"pendientes":47,
    "aprobados_mes":198,"rechazados_mes":23,
}

PRESUPUESTO = [
    {"partida":"1.1 Servicios Personales",    "asignado":450000,"ejecutado":387000,"pct":86},
    {"partida":"1.2 Servicios No Personales", "asignado":120000,"ejecutado":54000, "pct":45},
    {"partida":"2.1 Materiales y Suministros","asignado":85000, "ejecutado":61000, "pct":72},
    {"partida":"3.1 Infraestructura",         "asignado":200000,"ejecutado":95000, "pct":48},
    {"partida":"4.1 Transferencias",          "asignado":50000, "ejecutado":12000, "pct":24},
    {"partida":"5.1 Activos Fijos",           "asignado":95000, "ejecutado":78000, "pct":82},
]

AUDITORIA = [
    {"id":1,"usuario":"admin@muni.gt",       "accion":"Creación de usuario",       "tabla":"usuario",   "fecha":"09/06/2026 08:14","ip":"192.168.1.10"},
    {"id":2,"usuario":"funcionario@muni.gt", "accion":"Aprobación de expediente",  "tabla":"expediente","fecha":"09/06/2026 09:32","ip":"192.168.1.25"},
    {"id":3,"usuario":"admin@muni.gt",       "accion":"Modificación de rol",        "tabla":"usuario",   "fecha":"09/06/2026 10:05","ip":"192.168.1.10"},
    {"id":4,"usuario":"ciudadano@gmail.com", "accion":"Pago procesado",             "tabla":"pago",      "fecha":"09/06/2026 10:47","ip":"190.100.22.50"},
    {"id":5,"usuario":"funcionario@muni.gt", "accion":"Rechazo de expediente",      "tabla":"expediente","fecha":"09/06/2026 11:20","ip":"192.168.1.25"},
    {"id":6,"usuario":"director@muni.gt",    "accion":"Generación de reporte",      "tabla":"reporte",   "fecha":"09/06/2026 11:55","ip":"192.168.1.5"},
]

def log_auditoria(accion, tabla):
    nuevo_id = max(e["id"] for e in AUDITORIA) + 1 if AUDITORIA else 1
    AUDITORIA.append({
        "id": nuevo_id,
        "usuario": session.get("user","sistema"),
        "accion": accion,
        "tabla": tabla,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "ip": request.remote_addr or "127.0.0.1"
    })

def requiere_rol(*roles):
    if "user" not in session: return redirect(url_for("login"))
    if session["role"] not in roles: return redirect(url_for("dashboard"))
    return None

# ── Auth ───────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return redirect(url_for("dashboard") if "user" in session else url_for("login"))

@app.route("/login", methods=["GET","POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email","").strip()
        pwd   = request.form.get("password","").strip()
        user  = USERS.get(email)
        if user and user["password"] == pwd and user.get("activo", True):
            session["user"] = email
            session["role"] = user["role"]
            session["name"] = user["name"]
            return redirect(url_for("dashboard"))
        error = "Correo o contraseña incorrectos, o usuario inactivo."
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ── Dashboard (redirige según rol) ────────────────────────────────────────────
@app.route("/dashboard")
def dashboard():
    if "user" not in session: return redirect(url_for("login"))
    role = session["role"]
    if role == "ciudadano":
        mis = [s for s in SOLICITUDES if s["email"] == session["user"]]
        return render_template("dashboard_ciudadano.html", solicitudes=mis, kpi=KPI)
    elif role == "funcionario":
        todos = [s for s in SOLICITUDES if s["estado"] in ("Pendiente","En Revisión")]
        return render_template("dashboard_funcionario.html", solicitudes=todos, kpi=KPI)
    elif role == "admin":
        users_list = [{"email":k,**v} for k,v in USERS.items()]
        return render_template("dashboard_admin.html", users=users_list, logs=AUDITORIA[-5:])
    else:  # director
        return render_template("dashboard_ejecutivo.html", solicitudes=SOLICITUDES, kpi=KPI, presupuesto=PRESUPUESTO)

# ── CIUDADANO: Trámites ────────────────────────────────────────────────────────
@app.route("/tramites")
def tramites():
    if "user" not in session: return redirect(url_for("login"))
    if session["role"] != "ciudadano": return redirect(url_for("dashboard"))
    return render_template("tramites.html", tipos=TRAMITES_TIPOS)

@app.route("/tramites/nuevo", methods=["GET","POST"])
def tramite_nuevo():
    if "user" not in session: return redirect(url_for("login"))
    if session["role"] != "ciudadano": return redirect(url_for("dashboard"))
    if request.method == "POST":
        tipo_id  = int(request.form.get("tipo_id", 1))
        tipo     = next((t for t in TRAMITES_TIPOS if t["id"] == tipo_id), TRAMITES_TIPOS[0])
        nuevo_id = f"EXP-2026-{str(len(SOLICITUDES)+1).zfill(3)}"
        nueva = {
            "id":       nuevo_id,
            "tipo":     tipo["nombre"],
            "ciudadano":session["name"],
            "email":    session["user"],
            "estado":   "Pendiente",
            "fecha":    datetime.now().strftime("%d/%m/%Y"),
            "monto":    tipo["costo"],
            "pagado":   False,
            "resolucion": ""
        }
        SOLICITUDES.append(nueva)
        log_auditoria(f"Nueva solicitud creada: {nuevo_id}", "solicitud")
        session["ultimo_exp"] = nuevo_id
        return redirect(url_for("tramite_confirmacion"))
    tipo_id = request.args.get("tipo", 1, type=int)
    tipo = next((t for t in TRAMITES_TIPOS if t["id"] == tipo_id), TRAMITES_TIPOS[0])
    return render_template("tramite_nuevo.html", tipo=tipo, tipos=TRAMITES_TIPOS)

@app.route("/tramites/confirmacion")
def tramite_confirmacion():
    if "user" not in session: return redirect(url_for("login"))
    exp_id = session.pop("ultimo_exp", "EXP-2026-???")
    return render_template("tramite_confirmacion.html", exp_id=exp_id)

@app.route("/tramites/mis-solicitudes")
def mis_solicitudes():
    if "user" not in session: return redirect(url_for("login"))
    if session["role"] != "ciudadano": return redirect(url_for("dashboard"))
    mis = [s for s in SOLICITUDES if s["email"] == session["user"]]
    return render_template("mis_solicitudes.html", solicitudes=mis)

@app.route("/tramites/expediente/<exp_id>")
def expediente_detalle(exp_id):
    if "user" not in session: return redirect(url_for("login"))
    sol = next((s for s in SOLICITUDES if s["id"] == exp_id), None)
    if not sol: return redirect(url_for("mis_solicitudes"))
    # Ciudadano solo ve sus propios expedientes
    if session["role"] == "ciudadano" and sol["email"] != session["user"]:
        return redirect(url_for("mis_solicitudes"))
    return render_template("expediente_detalle.html", sol=sol)

# ── CIUDADANO: Pagos ───────────────────────────────────────────────────────────
@app.route("/pagos", methods=["GET","POST"])
def pagos():
    if "user" not in session: return redirect(url_for("login"))
    if session["role"] != "ciudadano": return redirect(url_for("dashboard"))
    if request.method == "POST":
        exp_id = request.form.get("expediente_id")
        sol = next((s for s in SOLICITUDES if s["id"] == exp_id and s["email"] == session["user"]), None)
        if sol:
            sol["pagado"] = True
            session["ultimo_pago"] = {"id": exp_id, "monto": sol["monto"], "tipo": sol["tipo"]}
            log_auditoria(f"Pago procesado: {exp_id}", "pago")
        return redirect(url_for("pago_exitoso"))
    mis_pendientes = [s for s in SOLICITUDES if s["email"] == session["user"] and not s["pagado"] and s["estado"] == "Aprobado"]
    return render_template("pagos.html", pendientes=mis_pendientes)

@app.route("/pagos/exitoso")
def pago_exitoso():
    if "user" not in session: return redirect(url_for("login"))
    pago = session.pop("ultimo_pago", {"id":"---","monto":0,"tipo":"---"})
    return render_template("pago_exitoso.html", pago=pago)

# ── FUNCIONARIO: Aprobar / Rechazar ───────────────────────────────────────────
@app.route("/funcionario/accion", methods=["POST"])
def funcionario_accion():
    if "user" not in session or session["role"] != "funcionario":
        return redirect(url_for("login"))
    exp_id     = request.form.get("exp_id")
    accion     = request.form.get("accion")   # "aprobar" o "rechazar"
    observacion = request.form.get("observacion","Sin observaciones.")
    sol = next((s for s in SOLICITUDES if s["id"] == exp_id), None)
    if sol:
        sol["estado"]     = "Aprobado" if accion == "aprobar" else "Rechazado"
        sol["resolucion"] = observacion
        log_auditoria(f"Expediente {accion}do: {exp_id}", "expediente")
    return redirect(url_for("dashboard"))

# ── ADMIN: Usuarios ────────────────────────────────────────────────────────────
@app.route("/usuarios")
def usuarios():
    r = requiere_rol("admin")
    if r: return r
    users_list = [{"email":k,**v} for k,v in USERS.items()]
    return render_template("usuarios.html", users=users_list)

@app.route("/usuarios/nuevo", methods=["POST"])
def usuario_nuevo():
    r = requiere_rol("admin")
    if r: return r
    email    = request.form.get("email","").strip()
    nombre   = request.form.get("nombre","").strip()
    rol      = request.form.get("rol","ciudadano")
    password = request.form.get("password","1234")
    depto    = request.form.get("depto","General")
    if email and email not in USERS:
        USERS[email] = {"password":password,"role":rol,"name":nombre,"depto":depto,"activo":True}
        log_auditoria(f"Usuario creado: {email} ({rol})", "usuario")
    return redirect(url_for("usuarios"))

@app.route("/usuarios/toggle/<email>")
def usuario_toggle(email):
    r = requiere_rol("admin")
    if r: return r
    if email in USERS and email != session["user"]:
        USERS[email]["activo"] = not USERS[email].get("activo", True)
        estado = "activado" if USERS[email]["activo"] else "desactivado"
        log_auditoria(f"Usuario {estado}: {email}", "usuario")
    return redirect(url_for("usuarios"))

@app.route("/usuarios/cambiar-rol", methods=["POST"])
def cambiar_rol():
    r = requiere_rol("admin")
    if r: return r
    email  = request.form.get("email")
    nuevo_rol = request.form.get("rol")
    if email in USERS and email != session["user"]:
        USERS[email]["role"] = nuevo_rol
        log_auditoria(f"Rol cambiado a {nuevo_rol}: {email}", "usuario")
    return redirect(url_for("usuarios"))

# ── ADMIN + DIRECTOR: Auditoría ────────────────────────────────────────────────
@app.route("/auditoria")
def auditoria():
    r = requiere_rol("admin","director")
    if r: return r
    return render_template("auditoria.html", logs=list(reversed(AUDITORIA)))

# ── DIRECTOR: Reportes y Presupuesto ──────────────────────────────────────────
@app.route("/reportes")
def reportes():
    r = requiere_rol("director")
    if r: return r
    log_auditoria("Generación de reporte", "reporte")
    return render_template("reportes.html", solicitudes=SOLICITUDES, kpi=KPI)

@app.route("/presupuesto")
def presupuesto():
    r = requiere_rol("director")
    if r: return r
    return render_template("presupuesto.html", partidas=PRESUPUESTO, kpi=KPI)

# ── API JSON ───────────────────────────────────────────────────────────────────
@app.route("/api/solicitudes-por-tipo")
def api_por_tipo():
    from collections import Counter
    c = Counter(s["tipo"] for s in SOLICITUDES)
    return jsonify({"labels":list(c.keys()),"data":list(c.values())})

@app.route("/api/solicitudes-por-estado")
def api_por_estado():
    from collections import Counter
    c = Counter(s["estado"] for s in SOLICITUDES)
    return jsonify({"labels":list(c.keys()),"data":list(c.values())})

@app.route("/api/ingresos-mensuales")
def api_ingresos():
    return jsonify({"labels":["Ene","Feb","Mar","Abr","May","Jun"],"data":[142000,165000,178000,155000,192000,187450]})

if __name__ == "__main__":
    app.run(debug=False)

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    role = session["role"]
    if role == "ciudadano":
        mis = [s for s in SOLICITUDES if s["email"] == session["user"]]
        return render_template("dashboard_ciudadano.html", solicitudes=mis, kpi=KPI)
    elif role == "funcionario":
        # TODOS los expedientes, no solo pendientes — el filtro lo hace el JS
        todos = list(SOLICITUDES)
        return render_template("dashboard_funcionario.html", solicitudes=todos, kpi=KPI)
    elif role == "admin":
        users_list = [{"email":k,**v} for k,v in USERS.items()]
        return render_template("dashboard_admin.html", users=users_list, logs=AUDITORIA[-5:])
    else:  # director
        return render_template("dashboard_ejecutivo.html", solicitudes=SOLICITUDES, kpi=KPI, presupuesto=PRESUPUESTO)