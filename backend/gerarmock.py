import json
import random
from datetime import date, timedelta

# ===== CONFIGURAÇÕES =====
TOTAL_MESES = 12  # 12 meses (Mar/2026 a Fev/2027)
LEADS_POR_MES = 80  # média de leads por mês por empresa (ajuste conforme desejar)
SEED = 42  # fixa para reprodução
random.seed(SEED)

MESES = [f"2026-{str(m).zfill(2)}" for m in range(3, 13)] + [f"2027-{str(m).zfill(2)}" for m in range(1, 3)]
# MESES = ['2026-03', '2026-04', ..., '2027-02']

def add_anos(data_str, anos_min, anos_max):
    dias = random.randint(int(anos_min * 365), int(anos_max * 365))
    return add_dias(data_str, dias)

def data_no_mes(mes_str):
    ano, mes = map(int, mes_str.split("-"))
    dia = random.randint(1, 28)
    return date(ano, mes, dia).isoformat()

def add_dias(data_str, dias):
    return (date.fromisoformat(data_str) + timedelta(days=dias)).isoformat()

# =================================================================
# 1. MONTSEGURO
# =================================================================
CANAIS_MKT_MS = ["Google Ads", "Meta Ads", "Indicação", "LinkedIn Ads", "Orgânico", "Outbound"]
OPERADORAS = ["Bradesco Saúde", "SulAmérica", "Amil", "Unimed", "Porto Saúde"]
PORTES = ["MEI", "Pequena empresa", "Média empresa"]
VENDEDORES_MS = ["Ana Ferreira", "Bruno Castro", "Carla Nunes", "Diego Almeida"]

def comissao_efetiva(operadora):
    base = {"SulAmérica":0.15, "Bradesco Saúde":0.14, "Amil":0.13, "Unimed":0.12, "Porto Saúde":0.16}.get(operadora, 0.15)
    return round(base, 2)

mont_lead_id = 1
mont_leads, mont_funil = [], []
for mes in MESES:
    n = random.randint(max(1, LEADS_POR_MES-25), LEADS_POR_MES+25)
    for _ in range(n):
        canal = random.choice(CANAIS_MKT_MS)
        porte = random.choices(PORTES, weights=[0.35,0.45,0.20])[0]
        vidas = {"MEI": random.randint(1,3), "Pequena empresa": random.randint(4,15), "Média empresa": random.randint(16,60)}[porte]
        data_criacao = data_no_mes(mes)
        mont_leads.append({
            "lead_id": mont_lead_id, "data_criacao": data_criacao, "mes_referencia": mes,
            "canal": canal, "porte_empresa": porte, "vidas_estimadas": vidas
        })

        r = random.random()
        premio = round(vidas * random.uniform(280, 520), 2)
        reg = {
            "lead_id": mont_lead_id, "vendedor": random.choice(VENDEDORES_MS),
            "operadora": None, "vidas": vidas, "premio_mensal_estimado": premio,
            "data_cotacao": None, "data_proposta": None, "data_contratacao": None,
            "data_implantacao": None, "status": "Lead sem avanço", "motivo_perda": None,
            "comissao_efetiva": 0.15, "data_qualificacao": None,
        }
        if r < 0.65:
            reg["data_cotacao"] = add_dias(data_criacao, random.randint(1,10))
            reg["data_qualificacao"] = reg["data_cotacao"]
            reg["operadora"] = random.choice(OPERADORAS)
            reg["comissao_efetiva"] = comissao_efetiva(reg["operadora"])
            reg["status"] = "Cotação enviada"
            if random.random() < 0.55:
                reg["data_proposta"] = add_dias(reg["data_cotacao"], random.randint(2,12))
                reg["status"] = "Proposta enviada"
                if random.random() < 0.45:
                    reg["data_contratacao"] = add_dias(reg["data_proposta"], random.randint(3,15))
                    reg["status"] = "Contratado - implantação pendente"
                    if random.random() < 0.80:
                        reg["data_implantacao"] = add_dias(reg["data_contratacao"], random.randint(7,30))
                        reg["status"] = "Implantado"
                else:
                    reg["status"] = "Perdido"
                    reg["motivo_perda"] = random.choice(["Preço","Escolheu concorrente","Fechou com corretora atual","Adiou decisão"])
            else:
                if random.random() < 0.5:
                    reg["status"] = "Perdido"
                    reg["motivo_perda"] = random.choice(["Sem retorno","Preço","Não fechou orçamento interno"])
        else:
            if random.random() < 0.3:
                reg["status"] = "Perdido"
                reg["motivo_perda"] = "Sem qualificação (fora do perfil)"
        mont_funil.append(reg)
        mont_lead_id += 1

# Clientes ativos (apenas implantados)
mont_clientes = []
churn_id = 1
for reg in mont_funil:
    if reg["status"] == "Implantado":
        churn = random.random() < 0.06
        mont_clientes.append({
            "contrato_id": churn_id, "lead_id": reg["lead_id"],
            "operadora": reg["operadora"],  # nunca None aqui
            "vidas_ativas": reg["vidas"],
            "premio_mensal": reg["premio_mensal_estimado"],
            "data_ativacao": reg["data_implantacao"],
            "cancelado": churn,
            "data_cancelamento": add_dias(reg["data_implantacao"], random.randint(30,150)) if churn else None,
        })
        churn_id += 1

mont_marketing = []
for mes in MESES:
    for canal in CANAIS_MKT_MS:
        leads_canal = len([l for l in mont_leads if l["mes_referencia"]==mes and l["canal"]==canal])
        inv = 0 if canal in ("Orgânico","Indicação") else round(random.uniform(1800,9500),2)
        mont_marketing.append({"mes": mes, "canal": canal, "investimento": inv, "leads_gerados": leads_canal})

mont_metas = [{"mes": mes, "empresa": "montseguro",
               "meta_receita_comissao": round(random.uniform(160000,220000),2),
               "meta_novos_contratos": random.randint(28,45)} for mes in MESES]

# =================================================================
# 2. PROP5
# =================================================================
PAISES = ["EUA", "Emirados Árabes", "Irlanda", "Reino Unido", "Canadá", "Portugal"]
MOEDAS = {"EUA":"USD","Emirados Árabes":"AED","Irlanda":"EUR","Reino Unido":"GBP","Canadá":"CAD","Portugal":"EUR"}
VENDEDORES_P5 = ["Gabriela Rocha", "Felipe Souza", "Henrique Lima", "Rafael Mendes", "Fernanda Lima"]

prop_lead_id = 1
prop_leads, prop_oportunidades = [], []
for mes in MESES:
    n = random.randint(max(1, LEADS_POR_MES-20), LEADS_POR_MES+20)
    for _ in range(n):
        pais = random.choice(PAISES)
        canal = random.choice(["Google Ads","Meta Ads","Indicação","Evento/Palestra","Orgânico"])
        data_criacao = data_no_mes(mes)
        prop_leads.append({
            "lead_id": prop_lead_id, "data_criacao": data_criacao, "mes_referencia": mes,
            "canal": canal, "pais_residencia": pais, "moeda": MOEDAS[pais]
        })
        # Oportunidade
        vendedor = random.choice(VENDEDORES_P5)
        valor_est = round(random.uniform(200000, 2500000), 2)
        prob = None
        estagio = random.choices(
            ["Diagnóstico não realizado", "Diagnóstico", "Reunião consultiva", "Proposta enviada", "Fechado", "Perdido"],
            weights=[0.10,0.20,0.25,0.20,0.10,0.15]
        )[0]
        if estagio != "Diagnóstico não realizado":
            data_diag = add_dias(data_criacao, random.randint(2,10))
        else:
            data_diag = None
        if estagio in ("Reunião consultiva","Proposta enviada","Fechado","Perdido"):
            data_reuniao = add_dias(data_diag, random.randint(3,12)) if data_diag else None
        else:
            data_reuniao = None
        if estagio == "Fechado":
            data_fech = add_dias(data_reuniao, random.randint(5,20)) if data_reuniao else None
            valor_fech = round(valor_est * random.uniform(0.85,1.10), 2)
            comissao = round(valor_fech * 0.045, 2)
        else:
            data_fech = None; valor_fech = None; comissao = None
        if estagio in ("Fechado","Proposta enviada"):
            prob = round(random.uniform(0.3,1.0),2)
        elif estagio == "Reunião consultiva":
            prob = round(random.uniform(0.15,0.45),2)
        elif estagio == "Diagnóstico":
            prob = 0.15
        elif estagio == "Perdido":
            prob = 0.0
        prop_oportunidades.append({
            "lead_id": prop_lead_id, "vendedor": vendedor, "valor_estimado": valor_est,
            "probabilidade": prob, "estagio": estagio,
            "data_diagnostico": data_diag, "data_reuniao_consultiva": data_reuniao,
            "data_fechamento": data_fech, "valor_fechado": valor_fech,
            "comissao": comissao, "data_renovacao": None, "chance_renovacao": None,
            "data_qualificacao": data_diag if data_diag else None
        })
        prop_lead_id += 1

# Marketing Prop5
CANAIS_P5 = ["Meta Ads", "Google Ads", "Evento/Palestra", "Indicação", "Orgânico"]
prop_marketing = []
for mes in MESES:
    for canal in CANAIS_P5:
        leads_canal = len([l for l in prop_leads if l["mes_referencia"]==mes and l["canal"]==canal])
        inv = 0 if canal in ("Indicação","Orgânico") else round(random.uniform(3000,20000),2)
        prop_marketing.append({"mes": mes, "canal": canal, "investimento": inv, "leads_gerados": leads_canal})

prop_metas = [{"mes": mes, "empresa": "prop5",
               "meta_comissao": round(random.uniform(80000,140000),2),
               "meta_fechamentos": random.randint(4,9)} for mes in MESES]

# =================================================================
# 3. TECHBRABO
# =================================================================
SOLUCOES_TB = ["Infra/Cloud","Sistema web","Dashboard/BI","Automação","CRM sob medida","API/Integração",
               "Consultoria","Cybersecurity","Software"]
TIPOS_RECEITA = ["Pontual","Recorrente","Híbrido"]
VENDEDORES_TB = ["Karina Duarte","Isabela Martins","João Pedro Alves","Lucas Oliveira","Mariana Costa"]
CANAL_TB = ["Outbound","LinkedIn Ads","Orgânico","Indicação","Cliente do grupo","Evento"]

tb_lead_id = 1
tb_leads, tb_oportunidades = [], []
for mes in MESES:
    n = random.randint(max(1, LEADS_POR_MES-20), LEADS_POR_MES+20)
    for _ in range(n):
        canal = random.choice(CANAL_TB)
        solucao = random.choice(SOLUCOES_TB)
        data_criacao = data_no_mes(mes)
        tb_leads.append({
            "lead_id": tb_lead_id, "data_criacao": data_criacao, "mes_referencia": mes,
            "canal": canal, "tipo_solucao": solucao
        })
        # Oportunidade
        vendedor = random.choice(VENDEDORES_TB)
        tipo_receita = random.choice(TIPOS_RECEITA)
        valor_proposta = round(random.uniform(15000, 350000), 2)
        estagio = random.choices(
            ["Qualificação","Proposta enviada","Negociação","Contrato assinado","Perdido"],
            weights=[0.30,0.25,0.15,0.15,0.15]
        )[0]
        cliente_existente = random.random() < 0.25
        data_proposta = add_dias(data_criacao, random.randint(3,15)) if estagio in ("Proposta enviada","Negociação","Contrato assinado","Perdido") else None
        if estagio == "Contrato assinado":
            data_contrato = add_dias(data_proposta, random.randint(2,20)) if data_proposta else None
            valor_contrato = round(valor_proposta * random.uniform(0.85,1.10), 2)
            mrr = round(random.uniform(500, 25000), 2) if tipo_receita != "Pontual" else None
        else:
            data_contrato = None; valor_contrato = None; mrr = None
        tb_oportunidades.append({
            "lead_id": tb_lead_id, "vendedor": vendedor, "tipo_solucao": solucao,
            "tipo_receita": tipo_receita, "valor_proposta": valor_proposta, "estagio": estagio,
            "data_proposta": data_proposta, "data_contrato": data_contrato,
            "valor_contrato": valor_contrato, "mrr": mrr,
            "cliente_existente": cliente_existente, "data_qualificacao": data_criacao if random.random()<0.3 else None
        })
        tb_lead_id += 1

# Projetos (apenas contratos assinados)
tb_projetos = []
proj_id = 1
for opp in tb_oportunidades:
    if opp["estagio"] == "Contrato assinado" and opp["valor_contrato"]:
        custo = round(opp["valor_contrato"] * random.uniform(0.4,0.7), 2)
        margem = round(opp["valor_contrato"] - custo, 2)
        margem_pct = round((margem / opp["valor_contrato"]) * 100, 1)
        status = random.choice(["Em andamento","Concluído","Atrasado","Cancelado"])
        data_inicio = opp["data_contrato"] or add_dias(data_no_mes(MESES[0]), random.randint(1,30))
        data_entrega_prev = add_dias(data_inicio, random.randint(30,120))
        data_entrega_real = add_dias(data_inicio, random.randint(20,140)) if status == "Concluído" else None
        horas_est = random.randint(50, 1200)
        tb_projetos.append({
            "projeto_id": proj_id, "lead_id": opp["lead_id"],
            "tipo_solucao": opp["tipo_solucao"],
            "valor_contrato": opp["valor_contrato"],
            "custo_estimado": custo,
            "margem": margem,
            "margem_percentual": margem_pct,
            "status": status,
            "data_inicio": data_inicio,
            "data_entrega_prevista": data_entrega_prev,
            "data_entrega_real": data_entrega_real,
            "mrr": opp["mrr"],
            "horas_estimadas": horas_est,
            "custo_hora": 85,
            "data_renovacao": add_anos(data_inicio, 1,1) if random.random()<0.3 else None,
        })
        proj_id += 1

tb_marketing = []
for mes in MESES:
    for canal in CANAL_TB:
        leads_canal = len([l for l in tb_leads if l["mes_referencia"]==mes and l["canal"]==canal])
        inv = 0 if canal in ("Indicação","Cliente do grupo","Orgânico") else round(random.uniform(1500,11000),2)
        tb_marketing.append({"mes": mes, "canal": canal, "investimento": inv, "leads_gerados": leads_canal})

tb_metas = [{"mes": mes, "empresa": "techbrabo",
             "meta_receita_total": round(random.uniform(120000,250000),2),
             "meta_novos_contratos": random.randint(6,12)} for mes in MESES]

# =================================================================
# MONTAR JSON FINAL
# =================================================================
data = {
    "periodo": {"inicio": "2026-03-01", "fim": "2027-02-28", "meses": MESES},
    "montseguro": {
        "leads": mont_leads,
        "funil": mont_funil,
        "clientes_ativos": mont_clientes,
        "marketing": mont_marketing,
        "metas": mont_metas
    },
    "prop5": {
        "leads": prop_leads,
        "oportunidades": prop_oportunidades,
        "marketing": prop_marketing,
        "metas": prop_metas
    },
    "techbrabo": {
        "leads": tb_leads,
        "oportunidades": tb_oportunidades,
        "projetos": tb_projetos,
        "marketing": tb_marketing,
        "metas": tb_metas
    }
}

# Salvar
with open("dataset_completo.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ Dataset gerado com sucesso!")
print(f"Montseguro: {len(mont_leads)} leads, {len(mont_clientes)} clientes ativos")
print(f"Prop5: {len(prop_leads)} leads, {len(prop_oportunidades)} oportunidades")
print(f"TechBrabo: {len(tb_leads)} leads, {len(tb_oportunidades)} oportunidades, {len(tb_projetos)} projetos")
